# Checklist Técnico de Code Review y Auditoría TAC

> **Proyecto:** Sistema de Gestión de Solicitudes Académicas  
> **Asignatura:** Metodología de Sistemas II (UTN - TUPaD)  
> **Autor / Revisor:** Grimaldi, Emiliano (Matrícula: 102964)  
> **Hito Auditado:** `etapa-docs` / `estado-refactorizado`

---

## 1. Matriz de Criterios de Aceptación Técnica (TAC) y Definition of Done (DoD)

| ID | Categoría TAC | Criterio de Aceptación Técnica Evaluado | Estado Inicial | Estado Final | Evidencia de Verificación |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-01** | **Arquitectura y SOLID** | ¿Cada clase posee una única responsabilidad clara (SRP) y depende de abstracciones inyectadas (DIP)? | ❌ Rechazado | ✅ Aprobado | `ServicioGestionSolicitudes` recibe `RepositorioSolicitudes` y `NotificadorSolicitudes` por constructor. |
| **CR-02** | **Extensibilidad (OCP)** | ¿Las reglas de prioridad y transiciones de estado están abiertas a la extensión sin modificar condicionales rígidos? | ❌ Rechazado | ✅ Aprobado | `EstrategiaPrioridadAcademica` y mapa declarativo en `EstadoSolicitud.puede_transicionar_a()`. |
| **CR-03** | **Clean Code y Nombres** | ¿Los identificadores revelan intención en el lenguaje del dominio sin abreviaturas crípticas ni valores mágicos? | ❌ Rechazado | ✅ Aprobado | Reemplazo de `prio = 1, 2, 3` y `nom_est` por `PrioridadSolicitud`, `EstadoSolicitud` y atributos descriptivos. |
| **CR-04** | **Firmas y Cohesión** | ¿Los métodos tienen un máximo de 3 parámetros y hacen una sola cosa en un único nivel de abstracción? | ❌ Rechazado | ✅ Aprobado | Uso de *Parameter Objects* (`DatosAltaSolicitud`, `FiltroBusquedaSolicitud`) y métodos de 3 a 12 líneas. |
| **CR-05** | **Principio DRY** | ¿El código está libre de bloques duplicados en el acceso a datos y búsqueda por identificador? | ❌ Rechazado | ✅ Aprobado | Búsqueda centralizada en `obtener_por_id()` dentro de las implementaciones del repositorio. |
| **CR-06** | **Manejo de Errores** | ¿Las anomalías se gestionan mediante excepciones de dominio tipadas en lugar de `print` + `return False`? | ❌ Rechazado | ✅ Aprobado | Jerarquía `ErrorDominioSolicitud` (`ErrorValidacionSolicitud`, `ErrorTransicionEstado`, `SolicitudNoEncontradaError`). |
| **CR-07** | **Pruebas (Testing AAA)** | ¿El 100% de la suite unitaria y de regresión pasa en verde con aislamiento (*Stubs/Mocks*) y cobertura > 80%? | ❌ Sin Tests | ✅ Aprobado | 10 tests en `test_sistema_solicitudes.py` ejecutados con `OK` y paridad JSON verificada. |
| **CR-08** | **Estilo y Linting** | ¿El código cumple con PEP 8, tipado estático (`typing`) y complejidad ciclomática en Rango A (`radon`)? | ❌ Rechazado | ✅ Aprobado | Métodos evaluados en Rango A de complejidad ciclomática y libres de variables globales. |
| **CR-09** | **Seguridad y Datos** | ¿Se utilizan exclusivamente datos sintéticos y manejo seguro de recursos mediante gestores de contexto (`with`)? | ⚠️ Parcial | ✅ Aprobado | Datos 100% ficticios y apertura segura con `with open(..., encoding="utf-8")`. |
| **CR-10** | **Gobernanza y Atomicidad** | ¿El repositorio cuenta con `README.md`, carpeta `/docs`, commits atómicos y los tags obligatorios de cada etapa? | ❌ Incompleto | ✅ Aprobado | Historial trazable con tags `estado-inicial`, `etapa-diagnostico`, `etapa-refactoring`, `etapa-pruebas`, `etapa-docs` y `estado-refactorizado`. |

---

## 2. Observaciones de Revisión y Feedback Profesional (Algoritmo en 3 Capas)

### Observación #1: Inmutabilidad en Objetos de Valor y Parámetros
- **Feedback:**
  - **[Capa 1 - Reconocimiento]:** Excelente extracción de los 8 parámetros sueltos de `procesar_alta` hacia las clases `Estudiante` y `DatosAltaSolicitud`.
  - **[Capa 2 - Hecho Objetivo y Propuesta]:** Para evitar mutaciones accidentales durante el flujo de ejecución, se recomienda configurar las `@dataclass` de valor con `frozen=True`.
  - **[Capa 3 - Confianza]:** Esto blinda la integridad de los datos de entrada en todas las capas del dominio.
- **Acción Correctiva:** Aplicado `@dataclass(frozen=True)` en `Estudiante`, `ResponsableArea`, `DatosAltaSolicitud` y `FiltroBusquedaSolicitud`.

### Observación #2: Desacoplamiento de Notificación en `cambiar_estado`
- **Feedback:**
  - **[Capa 1 - Reconocimiento]:** Muy buena implementación del contrato `NotificadorSolicitudes` en el alta del trámite.
  - **[Capa 2 - Hecho Objetivo y Propuesta]:** Para conservar el mensaje de consola `"Estado actualizado a ..."` sin acoplar el servicio a `print()`, se sugiere añadir `notificar_cambio_estado()` a la interfaz y al `NotificadorMock`.
  - **[Capa 3 - Confianza]:** Garantiza paridad externa del 100% y permite auditar la interacción en los tests.
- **Acción Correctiva:** Incorporado `notificar_cambio_estado(solicitud)` en `NotificadorSolicitudes`, `NotificadorEmailConsola` y `NotificadorMock`.

### Observación #3: Aislamiento de Archivos en Prueba de Paridad (`TC-10`)
- **Feedback:**
  - **[Capa 1 - Reconocimiento]:** El test comparativo antes/después demuestra empíricamente la ausencia de regresiones.
  - **[Capa 2 - Hecho Objetivo y Propuesta]:** Se recomienda utilizar `tempfile.TemporaryDirectory()` para que las pruebas no sobrescriban el archivo `solicitudes_db.json` del directorio de trabajo.
  - **[Capa 3 - Confianza]:** Asegura pruebas idempotentes y limpias en cualquier entorno local o de CI.
- **Acción Correctiva:** Implementado `tempfile.TemporaryDirectory()` en `test_paridad_regresion_antes_vs_despues_json`.

---

## 3. Dictamen Técnico Final
- **Resultado:** `APPROVED` (Aprobado con Informe de Calidad en Verde).