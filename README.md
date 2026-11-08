# Sistema de Gestión de Solicitudes Académicas — TPI Metodología de Sistemas II

> **Universidad:** Universidad Tecnológica Nacional (UTN)  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (TUPaD)  
> **Asignatura:** Metodología de Sistemas II — Comisión 12  
> **Integrante (Entrega Individual):** Grimaldi, Emiliano — Matrícula: 102964  
> **Estado General del Código:** `estado-refactorizado` (Calidad en Verde — 0% Regresión)

---

## 1. Descripción del Proyecto

El **Sistema de Gestión de Solicitudes Académicas** es un módulo de software diseñado para centralizar la recepción, clasificación por prioridad, asignación de responsables, transición de estados y generación de reportes de trámites estudiantiles (equivalencias, certificados de examen, cambios de comisión y revisiones de actas).

El propósito de este repositorio es demostrar la **evolución profesional de un sistema existente**: partiendo de una versión base monolítica funcional pero con deuda técnica interna (`estado-inicial`), hasta alcanzar una arquitectura desacoplada, mantenible y extensible mediante **principios SOLID**, **Clean Code**, **Refactoring Seguro**, **pruebas automatizadas bajo el patrón AAA** y **Code Review profesional** (`estado-refactorizado`).

---

## 2. Funcionalidades Verificables (Casos de Uso)

El sistema implementa cinco operaciones funcionales verificables que conservan el 100% de su comportamiento externo entre la versión inicial y la versión refactorizada:

1. **Registrar Solicitud:** Da de alta un trámite validando los datos del estudiante, calculando automáticamente la prioridad (`1-ALTA`, `2-MEDIA`, `3-BAJA`) según el tipo y urgencia, persistiendo en JSON y notificando por consola.
2. **Cambiar Estado de Solicitud:** Permite transicionar entre estados válidos (`PENDIENTE` $\rightarrow$ `EN_PROCESO`, `RESUELTA`, `RECHAZADA`), bloqueando la reapertura de solicitudes cerradas y registrando observaciones.
3. **Asignar Responsable y Área:** Vincula la solicitud con un agente y sector administrativo resolutivo, transicionando automáticamente de `PENDIENTE` a `EN_PROCESO`.
4. **Buscar y Filtrar Solicitudes:** Permite consultar trámites aplicando filtros combinados por estado, tipo de solicitud y legajo del estudiante.
5. **Generar Reporte Básico:** Calcula métricas operativas (total de trámites, desglose por estado y cantidad de prioridad alta) y las emite por consola.

---

## 3. Tecnologías y Herramientas Utilizadas

- **Lenguaje de Programación:** Python 3.11+ (con tipado estático `typing`, estructuras inmutables `@dataclass(frozen=True)`, enumeraciones `Enum` y contratos abstractos `abc.ABC`).
- **Persistencia de Datos:** Almacenamiento estructurado en archivo local (`solicitudes_db.json`) con datos 100% sintéticos.
- **Pruebas y Cobertura:** Biblioteca estándar `unittest` (aplicando patrón AAA, *Stubs* en memoria y *Mocks* de interacción) y `coverage` (*Statement & Branch Coverage* del 86%).
- **Análisis Estático y Calidad:** `pylint` (calificación mejorada a **8.09/10**) y `radon` (complejidad ciclomática reducida a **Rango A**).
- **Control de Versiones:** Git y GitHub con flujo trazable de commits atómicos y tags por etapa.

---

## 4. Estructura del Repositorio

```text
TPI_MTS_II/
├── README.md                                 <- Documentación general, instalación, uso y trazabilidad.
├── sistema_solicitudes_base.py               <- Versión inicial con deuda técnica (Tag: estado-inicial).
├── sistema_solicitudes_refactorizado.py      <- Versión final mejorada con SOLID y Clean Code (Tag: estado-refactorizado).
├── test_sistema_solicitudes.py               <- Suite de 10 pruebas unitarias AAA, Stubs, Mocks y regresión (Tag: etapa-pruebas).
├── solicitudes_db.json                       <- Persistencia estructurada en JSON con datos sintéticos.
└── docs/
    ├── diagnostico_deuda_tecnica.md          <- Inventario técnico de los 9 Code Smells (Tag: etapa-diagnostico).
    ├── code_review_checklist.md              <- Checklist TAC, feedback en 3 capas y dictamen en verde (Tag: etapa-docs).
    └── adr_001_arquitectura_solid.md         <- Registro de decisión arquitectónica (ADR-001).