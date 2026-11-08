from __future__ import annotations
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


# =====================================================================
# 1. EXCEPCIONES DE DOMINIO (Clean Code: Manejo explicito de errores)
# =====================================================================
class ErrorDominioSolicitud(Exception):
    """Excepcion base para errores de negocio en la gestion de solicitudes."""


class ErrorValidacionSolicitud(ErrorDominioSolicitud):
    """Se lanza cuando los datos de entrada de un estudiante o tramite son invalidos."""


class ErrorTransicionEstado(ErrorDominioSolicitud):
    """Se lanza cuando se intenta una operacion o cambio de estado no permitido."""


class SolicitudNoEncontradaError(ErrorDominioSolicitud):
    """Se lanza cuando no existe una solicitud con el identificador buscado."""


# =====================================================================
# 2. ENUMERACIONES CON COMPORTAMIENTO (Eliminacion de Magic Values)
# =====================================================================
class TipoSolicitud(Enum):
    EQUIVALENCIA = "EQUIVALENCIA"
    CERTIFICADO = "CERTIFICADO"
    CAMBIO_COMISION = "CAMBIO_COMISION"
    REVISION_ACTA = "REVISION_ACTA"


class PrioridadSolicitud(Enum):
    ALTA = 1
    MEDIA = 2
    BAJA = 3


class EstadoSolicitud(Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"

    def puede_transicionar_a(self, nuevo_estado: EstadoSolicitud) -> bool:
        transiciones_validas = {
            EstadoSolicitud.PENDIENTE: {
                EstadoSolicitud.EN_PROCESO,
                EstadoSolicitud.RESUELTA,
                EstadoSolicitud.RECHAZADA,
            },
            EstadoSolicitud.EN_PROCESO: {
                EstadoSolicitud.RESUELTA,
                EstadoSolicitud.RECHAZADA,
            },
            EstadoSolicitud.RESUELTA: set(),
            EstadoSolicitud.RECHAZADA: set(),
        }
        return nuevo_estado in transiciones_validas[self]


# =====================================================================
# 3. ENTIDADES DE DOMINIO Y OBJETOS DE PARAMETROS (Move Method & Parameter Object)
# =====================================================================
@dataclass(frozen=True)
class Estudiante:
    legajo: str
    nombre_completo: str
    email: str
    carrera: str

    def __post_init__(self) -> None:
        if not self.legajo or not self.legajo.strip():
            raise ErrorValidacionSolicitud("El legajo del estudiante no puede estar vacio.")
        if not self.nombre_completo or not self.nombre_completo.strip():
            raise ErrorValidacionSolicitud("El nombre del estudiante no puede estar vacio.")
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ErrorValidacionSolicitud(f"El correo '{self.email}' es invalido.")


@dataclass(frozen=True)
class ResponsableArea:
    nombre_responsable: str
    nombre_area: str

    def __post_init__(self) -> None:
        if not self.nombre_responsable.strip() or not self.nombre_area.strip():
            raise ErrorValidacionSolicitud("El responsable y el area son obligatorios.")


@dataclass(frozen=True)
class DatosAltaSolicitud:
    """Parameter Object para simplificar la firma del alta de solicitudes."""
    id_solicitud: int
    estudiante: Estudiante
    tipo: TipoSolicitud
    descripcion: str
    es_urgente: bool = False


@dataclass(frozen=True)
class FiltroBusquedaSolicitud:
    """Parameter Object para criterios de busqueda y filtrado."""
    estado: Optional[EstadoSolicitud] = None
    tipo: Optional[TipoSolicitud] = None
    legajo_estudiante: Optional[str] = None

    def cumple(self, solicitud: Solicitud) -> bool:
        if self.estado is not None and solicitud.estado != self.estado:
            return False
        if self.tipo is not None and solicitud.tipo != self.tipo:
            return False
        if self.legajo_estudiante is not None and solicitud.estudiante.legajo != self.legajo_estudiante:
            return False
        return True


@dataclass
class Solicitud:
    id_solicitud: int
    estudiante: Estudiante
    tipo: TipoSolicitud
    descripcion: str
    prioridad: PrioridadSolicitud
    estado: EstadoSolicitud = EstadoSolicitud.PENDIENTE
    responsable: Optional[ResponsableArea] = None
    fecha_creacion: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    observacion: str = ""

    def asignar_responsable(self, responsable: ResponsableArea) -> None:
        if self.estado == EstadoSolicitud.RECHAZADA:
            raise ErrorTransicionEstado("No se puede asignar responsable a una solicitud rechazada.")
        self.responsable = responsable
        if self.estado == EstadoSolicitud.PENDIENTE:
            self.estado = EstadoSolicitud.EN_PROCESO

    def cambiar_estado(self, nuevo_estado: EstadoSolicitud, observacion: str = "") -> None:
        if not self.estado.puede_transicionar_a(nuevo_estado):
            raise ErrorTransicionEstado(
                f"No se puede cambiar una solicitud desde {self.estado.value} a {nuevo_estado.value}."
            )
        self.estado = nuevo_estado
        self.observacion = observacion

    def a_diccionario(self) -> Dict[str, object]:
        return {
            "id": self.id_solicitud,
            "legajo": self.estudiante.legajo,
            "nombre_estudiante": self.estudiante.nombre_completo,
            "email": self.estudiante.email,
            "carrera": self.estudiante.carrera,
            "tipo": self.tipo.value,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad.value,
            "estado": self.estado.value,
            "responsable": self.responsable.nombre_responsable if self.responsable else "SIN_ASIGNAR",
            "area": self.responsable.nombre_area if self.responsable else "NINGUNA",
            "fecha": self.fecha_creacion,
            "obs": self.observacion,
        }

    @classmethod
    def desde_diccionario(cls, data: Dict[str, object]) -> Solicitud:
        estudiante = Estudiante(
            legajo=str(data["legajo"]),
            nombre_completo=str(data["nombre_estudiante"]),
            email=str(data["email"]),
            carrera=str(data["carrera"]),
        )
        nom_resp = str(data.get("responsable", "SIN_ASIGNAR"))
        nom_area = str(data.get("area", "NINGUNA"))
        responsable = (
            ResponsableArea(nom_resp, nom_area)
            if nom_resp != "SIN_ASIGNAR"
            else None
        )
        return cls(
            id_solicitud=int(data["id"]),
            estudiante=estudiante,
            tipo=TipoSolicitud(str(data["tipo"])),
            descripcion=str(data["descripcion"]),
            prioridad=PrioridadSolicitud(int(data["prioridad"])),
            estado=EstadoSolicitud(str(data["estado"])),
            responsable=responsable,
            fecha_creacion=str(data["fecha"]),
            observacion=str(data.get("obs", "")),
        )


# =====================================================================
# 4. POLITICA DE PRIORIDAD (OCP & Patron Strategy)
# =====================================================================
class EstrategiaPrioridad(ABC):
    @abstractmethod
    def calcular_prioridad(self, tipo: TipoSolicitud, es_urgente: bool) -> PrioridadSolicitud:
        pass


class EstrategiaPrioridadAcademica(EstrategiaPrioridad):
    _PRIORIDAD_BASE_POR_TIPO: Dict[TipoSolicitud, PrioridadSolicitud] = {
        TipoSolicitud.REVISION_ACTA: PrioridadSolicitud.ALTA,
        TipoSolicitud.EQUIVALENCIA: PrioridadSolicitud.MEDIA,
        TipoSolicitud.CAMBIO_COMISION: PrioridadSolicitud.MEDIA,
        TipoSolicitud.CERTIFICADO: PrioridadSolicitud.BAJA,
    }

    def calcular_prioridad(self, tipo: TipoSolicitud, es_urgente: bool) -> PrioridadSolicitud:
        if es_urgente:
            return PrioridadSolicitud.ALTA
        return self._PRIORIDAD_BASE_POR_TIPO.get(tipo, PrioridadSolicitud.BAJA)


# =====================================================================
# 5. CONTRATOS E INFRAESTRUCTURA (DIP, ISP, LSP)
# =====================================================================
class RepositorioSolicitudes(ABC):
    @abstractmethod
    def guardar(self, solicitud: Solicitud) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id_solicitud: int) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[Solicitud]:
        pass


class RepositorioSolicitudesMemoria(RepositorioSolicitudes):
    """Implementacion en memoria ideal para pruebas unitarias rapidas (LSP)."""
    def __init__(self) -> None:
        self._almacenamiento: Dict[int, Solicitud] = {}

    def guardar(self, solicitud: Solicitud) -> None:
        self._almacenamiento[solicitud.id_solicitud] = solicitud

    def obtener_por_id(self, id_solicitud: int) -> Optional[Solicitud]:
        return self._almacenamiento.get(id_solicitud)

    def listar_todas(self) -> List[Solicitud]:
        return list(self._almacenamiento.values())


class RepositorioSolicitudesJSON(RepositorioSolicitudes):
    """Wrapper de persistencia en archivo JSON desacoplado del dominio."""
    def __init__(self, ruta_archivo: str = "solicitudes_db.json") -> None:
        self._ruta_archivo = ruta_archivo

    def _leer_registros(self) -> List[Solicitud]:
        if not os.path.exists(self._ruta_archivo):
            return []
        with open(self._ruta_archivo, "r", encoding="utf-8") as archivo:
            datos_crudos = json.load(archivo)
            return [Solicitud.desde_diccionario(item) for item in datos_crudos]

    def _escribir_registros(self, solicitudes: List[Solicitud]) -> None:
        datos_serializados = [s.a_diccionario() for s in solicitudes]
        with open(self._ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_serializados, archivo, indent=4, ensure_ascii=False)

    def guardar(self, solicitud: Solicitud) -> None:
        solicitudes = self._leer_registros()
        actualizada = False
        for indice, existente in enumerate(solicitudes):
            if existente.id_solicitud == solicitud.id_solicitud:
                solicitudes[indice] = solicitud
                actualizada = True
                break
        if not actualizada:
            solicitudes.append(solicitud)
        self._escribir_registros(solicitudes)

    def obtener_por_id(self, id_solicitud: int) -> Optional[Solicitud]:
        for solicitud in self._leer_registros():
            if solicitud.id_solicitud == id_solicitud:
                return solicitud
        return None

    def listar_todas(self) -> List[Solicitud]:
        return self._leer_registros()


class NotificadorSolicitudes(ABC):
    @abstractmethod
    def notificar_alta(self, solicitud: Solicitud) -> str:
        pass

    @abstractmethod
    def notificar_cambio_estado(self, solicitud: Solicitud) -> str:
        pass


class NotificadorEmailConsola(NotificadorSolicitudes):
    def notificar_alta(self, solicitud: Solicitud) -> str:
        mensaje = (
            f"Notificando por EMAIL a {solicitud.estudiante.email}: "
            f"Solicitud {solicitud.id_solicitud} creada con prioridad {solicitud.prioridad.value}"
        )
        print(mensaje)
        return mensaje

    def notificar_cambio_estado(self, solicitud: Solicitud) -> str:
        mensaje = f"Estado actualizado a {solicitud.estado.value}"
        print(mensaje)
        return mensaje


# =====================================================================
# 6. GENERADOR DE REPORTES Y SERVICIO DE APLICACION (SRP & Extract Method)
# =====================================================================
class GeneradorReporteSolicitudes:
    @staticmethod
    def generar_resumen(solicitudes: List[Solicitud]) -> str:
        total = len(solicitudes)
        pendientes = sum(1 for s in solicitudes if s.estado == EstadoSolicitud.PENDIENTE)
        en_proceso = sum(1 for s in solicitudes if s.estado == EstadoSolicitud.EN_PROCESO)
        resueltas = sum(1 for s in solicitudes if s.estado == EstadoSolicitud.RESUELTA)
        rechazadas = sum(1 for s in solicitudes if s.estado == EstadoSolicitud.RECHAZADA)
        prioridad_alta = sum(1 for s in solicitudes if s.prioridad == PrioridadSolicitud.ALTA)

        reporte = (
            f"=== REPORTE ===\n"
            f"Total: {total} | Pendientes: {pendientes} | En Proceso: {en_proceso} | "
            f"Resueltas: {resueltas} | Rechazadas: {rechazadas} | Prioridad Alta: {prioridad_alta}"
        )
        print(reporte)
        return reporte


class ServicioGestionSolicitudes:
    def __init__(
        self,
        repositorio: RepositorioSolicitudes,
        notificador: NotificadorSolicitudes,
        estrategia_prioridad: Optional[EstrategiaPrioridad] = None,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador
        self._estrategia_prioridad = estrategia_prioridad or EstrategiaPrioridadAcademica()

    # Operacion 1: Registrar solicitud (Con Parameter Object y Extract Method)
    def registrar_solicitud(self, datos_alta: DatosAltaSolicitud) -> Solicitud:
        nueva_solicitud = self._construir_solicitud_inicial(datos_alta)
        self._repositorio.guardar(nueva_solicitud)
        self._notificador.notificar_alta(nueva_solicitud)
        return nueva_solicitud

    def _construir_solicitud_inicial(self, datos_alta: DatosAltaSolicitud) -> Solicitud:
        prioridad = self._estrategia_prioridad.calcular_prioridad(
            datos_alta.tipo, datos_alta.es_urgente
        )
        return Solicitud(
            id_solicitud=datos_alta.id_solicitud,
            estudiante=datos_alta.estudiante,
            tipo=datos_alta.tipo,
            descripcion=datos_alta.descripcion,
            prioridad=prioridad,
        )

    # Operacion 2: Cambiar estado (Delega en la entidad Solicitud - Move Method)
    def cambiar_estado(
        self, id_solicitud: int, nuevo_estado: EstadoSolicitud, observacion: str = ""
    ) -> Solicitud:
        solicitud = self._obtener_solicitud_existente(id_solicitud)
        solicitud.cambiar_estado(nuevo_estado, observacion)
        self._repositorio.guardar(solicitud)
        self._notificador.notificar_cambio_estado(solicitud)
        return solicitud

    # Operacion 3: Asignar responsable (Delega en la entidad Solicitud - Move Method)
    def asignar_responsable(
        self, id_solicitud: int, responsable: ResponsableArea
    ) -> Solicitud:
        solicitud = self._obtener_solicitud_existente(id_solicitud)
        solicitud.asignar_responsable(responsable)
        self._repositorio.guardar(solicitud)
        return solicitud

    # Operacion 4: Buscar y filtrar solicitudes (Con Parameter Object)
    def buscar_solicitudes(self, filtro: FiltroBusquedaSolicitud) -> List[Solicitud]:
        todas = self._repositorio.listar_todas()
        return [solicitud for solicitud in todas if filtro.cumple(solicitud)]

    # Operacion 5: Generar reporte basico (Delega en GeneradorReporteSolicitudes - SRP)
    def generar_reporte(self) -> str:
        solicitudes = self._repositorio.listar_todas()
        return GeneradorReporteSolicitudes.generar_resumen(solicitudes)

    def _obtener_solicitud_existente(self, id_solicitud: int) -> Solicitud:
        solicitud = self._repositorio.obtener_por_id(id_solicitud)
        if solicitud is None:
            raise SolicitudNoEncontradaError(
                f"No se encontro la solicitud con ID {id_solicitud}."
            )
        return solicitud


# =====================================================================
# 7. EJECUCION DE PRUEBA DE CONSOLA (Verificacion de comportamiento externo)
# =====================================================================
def ejecutar_prueba_consola() -> None:
    archivo_db = "solicitudes_db.json"
    if os.path.exists(archivo_db):
        os.remove(archivo_db)

    repositorio = RepositorioSolicitudesJSON(archivo_db)
    notificador = NotificadorEmailConsola()
    servicio = ServicioGestionSolicitudes(repositorio, notificador)

    # 1. Alta de solicitudes con los mismos datos sinteticos (Operacion 1)
    servicio.registrar_solicitud(
        DatosAltaSolicitud(
            id_solicitud=101,
            estudiante=Estudiante("L-45890", "Ana Perez", "ana.perez@tup.utn.edu.ar", "TUP"),
            tipo=TipoSolicitud.EQUIVALENCIA,
            descripcion="Equivalencia de Programacion I",
            es_urgente=False,
        )
    )
    servicio.registrar_solicitud(
        DatosAltaSolicitud(
            id_solicitud=102,
            estudiante=Estudiante("L-46120", "Lucas Gomez", "lucas.gomez@tup.utn.edu.ar", "TUP"),
            tipo=TipoSolicitud.REVISION_ACTA,
            descripcion="Nota de examen final no reflejada en acta",
            es_urgente=True,
        )
    )

    # 2. Asignacion de responsable y area (Operacion 3)
    servicio.asignar_responsable(
        102, ResponsableArea("Carlos Ruiz", "Secretaria Academica")
    )

    # 3. Cambio de estado de solicitud (Operacion 2)
    servicio.cambiar_estado(
        102, EstadoSolicitud.RESUELTA, "Acta rectificada correctamente"
    )

    # 4. Busqueda y filtrado de solicitudes pendientes (Operacion 4)
    pendientes = servicio.buscar_solicitudes(
        FiltroBusquedaSolicitud(estado=EstadoSolicitud.PENDIENTE)
    )

    # 5. Generacion de reporte basico (Operacion 5)
    servicio.generar_reporte()


if __name__ == "__main__":
    ejecutar_prueba_consola()