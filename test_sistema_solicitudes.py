import os
import tempfile
import unittest
from typing import List

import sistema_solicitudes_base as modulo_base
from sistema_solicitudes_refactorizado import (
    DatosAltaSolicitud,
    ErrorTransicionEstado,
    ErrorValidacionSolicitud,
    EstadoSolicitud,
    Estudiante,
    FiltroBusquedaSolicitud,
    NotificadorSolicitudes,
    PrioridadSolicitud,
    RepositorioSolicitudesJSON,
    RepositorioSolicitudesMemoria,
    ResponsableArea,
    ServicioGestionSolicitudes,
    Solicitud,
    SolicitudNoEncontradaError,
    TipoSolicitud,
)


class NotificadorMock(NotificadorSolicitudes):
    """Doble de prueba (Mock) para auditar interacciones de notificacion sin imprimir en consola."""

    def __init__(self) -> None:
        self.altas_notificadas: List[int] = []
        self.cambios_estado_notificados: List[tuple[int, str]] = []

    def notificar_alta(self, solicitud: Solicitud) -> str:
        self.altas_notificadas.append(solicitud.id_solicitud)
        return (
            f"Notificando por EMAIL a {solicitud.estudiante.email}: "
            f"Solicitud {solicitud.id_solicitud} creada con prioridad {solicitud.prioridad.value}"
        )

    def notificar_cambio_estado(self, solicitud: Solicitud) -> str:
        self.cambios_estado_notificados.append(
            (solicitud.id_solicitud, solicitud.estado.value)
        )
        return f"Estado actualizado a {solicitud.estado.value}"


class TestSistemaSolicitudesRefactorizado(unittest.TestCase):
    """Suite de pruebas unitarias y de regresion bajo patron AAA (Arrange, Act, Assert)."""

    def setUp(self) -> None:
        # Arrange comun: Aislamiento total mediante Stub en memoria y Mock de notificaciones
        self.repositorio_stub = RepositorioSolicitudesMemoria()
        self.notificador_mock = NotificadorMock()
        self.servicio = ServicioGestionSolicitudes(
            repositorio=self.repositorio_stub,
            notificador=self.notificador_mock,
        )
        self.estudiante_ana = Estudiante(
            legajo="L-45890",
            nombre_completo="Ana Perez",
            email="ana.perez@tup.utn.edu.ar",
            carrera="TUP",
        )
        self.estudiante_lucas = Estudiante(
            legajo="L-46120",
            nombre_completo="Lucas Gomez",
            email="lucas.gomez@tup.utn.edu.ar",
            carrera="TUP",
        )

    # TC-01: Camino feliz de alta y auditoria de Mock
    def test_alta_solicitud_equivalencia_prioridad_media(self) -> None:
        # Arrange
        datos = DatosAltaSolicitud(
            id_solicitud=101,
            estudiante=self.estudiante_ana,
            tipo=TipoSolicitud.EQUIVALENCIA,
            descripcion="Equivalencia de Programacion I",
            es_urgente=False,
        )

        # Act
        creada = self.servicio.registrar_solicitud(datos)

        # Assert (Igualdad de estado + Auditoria del Mock)
        self.assertEqual(creada.estado, EstadoSolicitud.PENDIENTE)
        self.assertEqual(creada.prioridad, PrioridadSolicitud.MEDIA)
        self.assertEqual(self.notificador_mock.altas_notificadas, [101])

    # TC-02: Cobertura de ramas (Branch Coverage) para prioridad ALTA
    def test_alta_solicitud_urgente_o_acta_prioridad_alta(self) -> None:
        # Arrange
        datos_acta = DatosAltaSolicitud(
            id_solicitud=102,
            estudiante=self.estudiante_lucas,
            tipo=TipoSolicitud.REVISION_ACTA,
            descripcion="Revision de nota final",
            es_urgente=False,
        )
        datos_urgente = DatosAltaSolicitud(
            id_solicitud=103,
            estudiante=self.estudiante_ana,
            tipo=TipoSolicitud.CERTIFICADO,
            descripcion="Certificado laboral urgente",
            es_urgente=True,
        )

        # Act
        sol_acta = self.servicio.registrar_solicitud(datos_acta)
        sol_urgente = self.servicio.registrar_solicitud(datos_urgente)

        # Assert
        self.assertEqual(sol_acta.prioridad, PrioridadSolicitud.ALTA)
        self.assertEqual(sol_urgente.prioridad, PrioridadSolicitud.ALTA)

    # TC-03: Cobertura de ramas para prioridad BAJA
    def test_alta_solicitud_certificado_prioridad_baja(self) -> None:
        # Arrange
        datos = DatosAltaSolicitud(
            id_solicitud=104,
            estudiante=self.estudiante_ana,
            tipo=TipoSolicitud.CERTIFICADO,
            descripcion="Certificado de alumno regular",
            es_urgente=False,
        )

        # Act
        sol = self.servicio.registrar_solicitud(datos)

        # Assert
        self.assertEqual(sol.prioridad, PrioridadSolicitud.BAJA)

    # TC-04: Casos de borde e inyeccion de datos invalidos en Estudiante
    def test_validacion_estudiante_datos_invalidos(self) -> None:
        # Arrange & Act & Assert: Legajo vacio
        with self.assertRaises(ErrorValidacionSolicitud):
            Estudiante("", "Ana Perez", "ana@tup.utn.edu.ar", "TUP")

        # Arrange & Act & Assert: Email sin formato valido
        with self.assertRaises(ErrorValidacionSolicitud):
            Estudiante("L-45890", "Ana Perez", "correo_invalido_sin_arroba", "TUP")

    # TC-05: Regla de negocio de transicion automatica al asignar responsable
    def test_asignar_responsable_transiciona_a_en_proceso(self) -> None:
        # Arrange
        self.servicio.registrar_solicitud(
            DatosAltaSolicitud(101, self.estudiante_ana, TipoSolicitud.EQUIVALENCIA, "Desc")
        )
        responsable = ResponsableArea("Carlos Ruiz", "Secretaria Academica")

        # Act
        actualizada = self.servicio.asignar_responsable(101, responsable)

        # Assert
        self.assertEqual(actualizada.estado, EstadoSolicitud.EN_PROCESO)
        self.assertEqual(actualizada.responsable.nombre_responsable, "Carlos Ruiz")

    # TC-06: Caso de borde - Bloqueo de reapertura de solicitudes cerradas
    def test_bloqueo_cambio_estado_en_solicitud_cerrada(self) -> None:
        # Arrange
        self.servicio.registrar_solicitud(
            DatosAltaSolicitud(102, self.estudiante_lucas, TipoSolicitud.REVISION_ACTA, "Desc")
        )
        self.servicio.cambiar_estado(102, EstadoSolicitud.RESUELTA, "Cerrada OK")

        # Act & Assert
        with self.assertRaises(ErrorTransicionEstado):
            self.servicio.cambiar_estado(102, EstadoSolicitud.EN_PROCESO, "Intento reabrir")

    # TC-07: Caso de borde - Prohibicion de asignar responsable a solicitud rechazada
    def test_bloqueo_asignar_responsable_en_rechazada(self) -> None:
        # Arrange
        self.servicio.registrar_solicitud(
            DatosAltaSolicitud(105, self.estudiante_ana, TipoSolicitud.CAMBIO_COMISION, "Desc")
        )
        self.servicio.cambiar_estado(105, EstadoSolicitud.RECHAZADA, "Fuera de termino")

        # Act & Assert
        with self.assertRaises(ErrorTransicionEstado):
            self.servicio.asignar_responsable(
                105, ResponsableArea("Carlos Ruiz", "Secretaria Academica")
            )

    # TC-08: Caso de borde - Solicitud inexistente
    def test_operacion_sobre_solicitud_inexistente(self) -> None:
        # Act & Assert
        with self.assertRaises(SolicitudNoEncontradaError):
            self.servicio.cambiar_estado(999, EstadoSolicitud.RESUELTA, "No existe")

    # TC-09: Aseveracion sobre colecciones en busqueda filtrada
    def test_busqueda_combinada_con_parameter_object(self) -> None:
        # Arrange
        self.servicio.registrar_solicitud(
            DatosAltaSolicitud(101, self.estudiante_ana, TipoSolicitud.EQUIVALENCIA, "Eq 1")
        )
        self.servicio.registrar_solicitud(
            DatosAltaSolicitud(102, self.estudiante_lucas, TipoSolicitud.REVISION_ACTA, "Acta 1")
        )
        self.servicio.cambiar_estado(102, EstadoSolicitud.RESUELTA, "Listo")

        # Act
        pendientes = self.servicio.buscar_solicitudes(
            FiltroBusquedaSolicitud(
                estado=EstadoSolicitud.PENDIENTE,
                tipo=TipoSolicitud.EQUIVALENCIA,
                legajo_estudiante="L-45890",
            )
        )

        # Assert (Colecciones: longitud y contenido)
        self.assertEqual(len(pendientes), 1)
        self.assertEqual(pendientes[0].id_solicitud, 101)

    # TC-10: Prueba de Paridad y No Regresion (Sistema Base vs. Sistema Refactorizado)
    def test_paridad_regresion_antes_vs_despues_json(self) -> None:
        # Arrange: Archivos temporales independientes para comparar persistencia real
        with tempfile.TemporaryDirectory() as tmp_dir:
            archivo_base = os.path.join(tmp_dir, "db_base.json")
            archivo_refact = os.path.join(tmp_dir, "db_refact.json")

            modulo_base.DB_FILE = archivo_base
            gestor_base = modulo_base.GestorTotalSolicitudes()

            repo_json = RepositorioSolicitudesJSON(archivo_refact)
            servicio_refact = ServicioGestionSolicitudes(repo_json, self.notificador_mock)

            # Act 1: Ejecutar exactamente las mismas 5 operaciones en el Sistema Base
            gestor_base.procesar_alta(
                101, "L-45890", "Ana Perez", "ana.perez@tup.utn.edu.ar",
                "TUP", "EQUIVALENCIA", "Equivalencia de Programacion I", False
            )
            gestor_base.procesar_alta(
                102, "L-46120", "Lucas Gomez", "lucas.gomez@tup.utn.edu.ar",
                "TUP", "REVISION_ACTA", "Nota de examen final no reflejada en acta", True
            )
            gestor_base.asignar_responsable(102, "Carlos Ruiz", "Secretaria Academica")
            gestor_base.cambiar_estado(102, "RESUELTA", "Acta rectificada correctamente")
            pendientes_base = gestor_base.buscar(filtro_estado="PENDIENTE")
            reporte_base = gestor_base.generar_reporte()

            # Act 2: Ejecutar las mismas 5 operaciones en el Sistema Refactorizado
            servicio_refact.registrar_solicitud(
                DatosAltaSolicitud(101, self.estudiante_ana, TipoSolicitud.EQUIVALENCIA,
                                   "Equivalencia de Programacion I", False)
            )
            servicio_refact.registrar_solicitud(
                DatosAltaSolicitud(102, self.estudiante_lucas, TipoSolicitud.REVISION_ACTA,
                                   "Nota de examen final no reflejada en acta", True)
            )
            servicio_refact.asignar_responsable(
                102, ResponsableArea("Carlos Ruiz", "Secretaria Academica")
            )
            servicio_refact.cambiar_estado(
                102, EstadoSolicitud.RESUELTA, "Acta rectificada correctamente"
            )
            pendientes_refact = servicio_refact.buscar_solicitudes(
                FiltroBusquedaSolicitud(estado=EstadoSolicitud.PENDIENTE)
            )
            reporte_refact = servicio_refact.generar_reporte()

            # Assert: Comportamiento externo y persistencia 100% equivalentes
            self.assertEqual(reporte_base, reporte_refact)
            self.assertEqual(len(pendientes_base), len(pendientes_refact))
            self.assertEqual(pendientes_base[0]["id"], pendientes_refact[0].id_solicitud)


if __name__ == "__main__":
    unittest.main(verbosity=2)