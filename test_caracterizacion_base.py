import contextlib
import io
import os
import tempfile
import unittest

import sistema_solicitudes_base as base
from sistema_solicitudes_refactorizado import (
    DatosAltaSolicitud,
    ErrorTransicionEstado,
    ErrorValidacionSolicitud,
    EstadoSolicitud,
    Estudiante,
    NotificadorEmailConsola,
    PrioridadSolicitud,
    RepositorioSolicitudesMemoria,
    ResponsableArea,
    ServicioGestionSolicitudes,
    SolicitudNoEncontradaError,
    TipoSolicitud,
)


class TestCaracterizacionBase(unittest.TestCase):
    """Pruebas de caracterizacion sobre la version inicial (CB-01 a CB-09)."""

    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self.ruta_db = os.path.join(self._temp_dir.name, "test_base_db.json")
        base.DB_FILE = self.ruta_db
        base.solicitudes_memoria = []
        self.gestor = base.GestorTotalSolicitudes()

    def tearDown(self) -> None:
        self._temp_dir.cleanup()

    # CB-01: Alta valida devuelve True y persiste en el archivo JSON
    def test_cb01_alta_valida_devuelve_true_y_persiste(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            resultado = self.gestor.procesar_alta(
                101, "L-45890", "Ana Perez", "ana.perez@tup.utn.edu.ar",
                "TUP", "EQUIVALENCIA", "Equivalencia de Programacion I", False
            )
        self.assertTrue(resultado)
        self.assertTrue(os.path.exists(self.ruta_db))
        self.assertEqual(len(base.solicitudes_memoria), 1)
        self.assertEqual(base.solicitudes_memoria[0]["estado"], "PENDIENTE")

    # CB-02: Calculo de prioridad 1 (Alta), 2 (Media) y 3 (Baja) segun tipo y urgencia
    def test_cb02_prioridad_segun_tipo_y_urgencia(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.gestor.procesar_alta(1, "L-1", "A", "a@b.com", "TUP", "REVISION_ACTA", "D", False)
            self.gestor.procesar_alta(2, "L-2", "B", "b@b.com", "TUP", "CERTIFICADO", "D", True)
            self.gestor.procesar_alta(3, "L-3", "C", "c@b.com", "TUP", "EQUIVALENCIA", "D", False)
            self.gestor.procesar_alta(4, "L-4", "D", "d@b.com", "TUP", "CERTIFICADO", "D", False)

        prioridades = {s["id"]: s["prioridad"] for s in base.solicitudes_memoria}
        self.assertEqual(prioridades[1], 1)
        self.assertEqual(prioridades[2], 1)
        self.assertEqual(prioridades[3], 2)
        self.assertEqual(prioridades[4], 3)

    # CB-03: Errores de datos del estudiante se informan con print y return False
    def test_cb03_errores_se_informan_con_false_y_print(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            ok = self.gestor.procesar_alta(
                10, "", "Ana Perez", "correo_sin_arroba", "TUP", "CERTIFICADO", "Desc", False
            )
        self.assertFalse(ok)
        self.assertIn("Error en datos del estudiante", buffer.getvalue())

    # CB-04: Tipo de solicitud invalido devuelve False e imprime error
    def test_cb04_tipo_invalido_devuelve_false(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            ok = self.gestor.procesar_alta(
                11, "L-100", "Ana Perez", "ana@tup.utn.edu.ar", "TUP", "BECA", "Desc", False
            )
        self.assertFalse(ok)
        self.assertIn("Error: tipo invalido", buffer.getvalue())

    # CB-05: Una solicitud en estado RESUELTA o RECHAZADA no permite cambios de estado
    def test_cb05_estado_cerrado_no_se_puede_cambiar(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.gestor.procesar_alta(20, "L-1", "Ana", "a@b.com", "TUP", "CERTIFICADO", "D", False)
            self.gestor.cambiar_estado(20, "RESUELTA", "Finalizada")
            reapertura = self.gestor.cambiar_estado(20, "EN_PROCESO", "Reabrir")
        self.assertFalse(reapertura)

    # CB-06: Asignar responsable cambia automaticamente de PENDIENTE a EN_PROCESO
    def test_cb06_asignar_pasa_pendiente_a_en_proceso(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.gestor.procesar_alta(30, "L-1", "Ana", "a@b.com", "TUP", "EQUIVALENCIA", "D", False)
            ok = self.gestor.asignar_responsable(30, "Carlos Ruiz", "Secretaria Academica")
        self.assertTrue(ok)
        self.assertEqual(base.solicitudes_memoria[0]["estado"], "EN_PROCESO")
        self.assertEqual(base.solicitudes_memoria[0]["responsable"], "Carlos Ruiz")

    # CB-07: Busqueda con filtros combinados por estado, tipo y legajo
    def test_cb07_filtros_combinados(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.gestor.procesar_alta(40, "L-1", "Ana", "a@b.com", "TUP", "EQUIVALENCIA", "D", False)
            self.gestor.procesar_alta(41, "L-2", "Luis", "l@b.com", "TUP", "CERTIFICADO", "D", False)
        filtradas = self.gestor.buscar(
            filtro_estado="PENDIENTE", filtro_tipo="EQUIVALENCIA", filtro_legajo="L-1"
        )
        self.assertEqual(len(filtradas), 1)
        self.assertEqual(filtradas[0]["id"], 40)

    # CB-08: El reporte basico contiene el desglose exacto de totales
    def test_cb08_reporte_contiene_totales(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.gestor.procesar_alta(50, "L-1", "Ana", "a@b.com", "TUP", "REVISION_ACTA", "D", True)
            reporte = self.gestor.generar_reporte()
        self.assertIn("Total: 1 | Pendientes: 1", reporte)
        self.assertIn("Prioridad Alta: 1", reporte)

    # CB-09: Defecto conocido en base - ID inexistente devuelve False silenciosamente
    def test_cb09_defecto_conocido_id_inexistente_devuelve_false_en_silencio(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            ok_estado = self.gestor.cambiar_estado(999, "RESUELTA", "Obs")
            ok_asignar = self.gestor.asignar_responsable(999, "Resp", "Area")
        self.assertFalse(ok_estado)
        self.assertFalse(ok_asignar)
        self.assertEqual(buffer.getvalue(), "")


class TestCambiosIntencionales(unittest.TestCase):
    """Pruebas de contrato que verifican las mejoras intencionales (CI-01 a CI-05)."""

    def setUp(self) -> None:
        self.repositorio = RepositorioSolicitudesMemoria()
        self.notificador = NotificadorEmailConsola()
        self.servicio = ServicioGestionSolicitudes(self.repositorio, self.notificador)
        self.estudiante = Estudiante("L-45890", "Ana Perez", "ana.perez@tup.utn.edu.ar", "TUP")

    # CI-01: Los errores de validacion y negocio lanzan excepciones de dominio en lugar de return False
    def test_ci01_errores_son_excepciones_de_dominio(self) -> None:
        with self.assertRaises(ErrorValidacionSolicitud):
            Estudiante("", "Ana Perez", "ana@tup.utn.edu.ar", "TUP")
        with self.assertRaises(ErrorValidacionSolicitud):
            ResponsableArea("", "")

    # CI-02: Operar sobre un ID inexistente lanza SolicitudNoEncontradaError
    def test_ci02_id_inexistente_lanza_excepcion_tipada(self) -> None:
        with self.assertRaises(SolicitudNoEncontradaError):
            self.servicio.cambiar_estado(999, EstadoSolicitud.RESUELTA, "No existe")
        with self.assertRaises(SolicitudNoEncontradaError):
            self.servicio.asignar_responsable(999, ResponsableArea("Carlos", "Secretaria"))

    # CI-03: La transicion redundante EN_PROCESO -> EN_PROCESO se bloquea con ErrorTransicionEstado
    def test_ci03_en_proceso_a_en_proceso_ya_no_esta_permitido(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.servicio.registrar_solicitud(
                DatosAltaSolicitud(101, self.estudiante, TipoSolicitud.EQUIVALENCIA, "Desc")
            )
            self.servicio.cambiar_estado(101, EstadoSolicitud.EN_PROCESO, "En curso")
            with self.assertRaises(ErrorTransicionEstado):
                self.servicio.cambiar_estado(101, EstadoSolicitud.EN_PROCESO, "Repetido")

    # CI-04: Validacion de email mas estricta (rechaza 'a@b' sin punto en el dominio)
    def test_ci04_validacion_de_email_mas_estricta(self) -> None:
        with self.assertRaises(ErrorValidacionSolicitud):
            Estudiante("L-45890", "Ana Perez", "a@b", "TUP")

    # CI-05: El legajo o nombre compuesto solo por espacios en blanco se rechaza con strip()
    def test_ci05_legajo_solo_espacios_se_rechaza(self) -> None:
        with self.assertRaises(ErrorValidacionSolicitud):
            Estudiante("   ", "Ana Perez", "ana.perez@tup.utn.edu.ar", "TUP")


if __name__ == "__main__":
    unittest.main(verbosity=2)