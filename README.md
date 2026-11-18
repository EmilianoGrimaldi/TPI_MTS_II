# Sistema de Gestión de Solicitudes Académicas — TPI Metodología de Sistemas II

> **Universidad:** Universidad Tecnológica Nacional (UTN)  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (TUPaD)  
> **Asignatura:** Metodología de Sistemas II — Comisión 12  
> **Autor:** Grimaldi, Emiliano (Matrícula: 102964)  
> **Estado General Final:** `estado-refactorizado` (Auditoría de Calidad en Verde)

---

## 1. Descripción y Propósito del Trabajo

Este repositorio contiene el desarrollo completo del **Trabajo Práctico Integrador (TPI)** de **Metodología de Sistemas II**, centrado en la evolución profesional de un sistema de software existente: el **Sistema de Gestión de Solicitudes Académicas**.

El objetivo central del proyecto es diagnosticar la **deuda técnica** y los **code smells** de una versión base monolítica (`estado-inicial`), rediseñar su arquitectura aplicando principios **SOLID** y **Clean Code**, ejecutar **refactorings seguros** (`etapa-refactoring`), validar el comportamiento mediante una **suite de 24 pruebas automatizadas bajo el patrón AAA** (`etapa-pruebas`) y auditar la entrega mediante un **Code Review profesional** guiado por Criterios de Aceptación Técnica (`etapa-docs` / `estado-refactorizado`).

---

## 2. Tecnologías y Herramientas Utilizadas

- **Lenguaje:** Python 3.11+ (`typing`, `@dataclass(frozen=True)`, `Enum`, `abc.ABC`).
- **Persistencia:** Almacenamiento estructurado en archivo JSON local (`solicitudes_db.json`).
- **Testing y Cobertura:** Biblioteca estándar `unittest` (con *Stubs* en memoria, *Mocks* de interacción, pruebas de caracterización y de paridad) y `coverage` (*Statement & Branch Coverage*).
- **Análisis Estático y Métricas:** `pylint` (auditoría de estilo y code smells) y `radon` (complejidad ciclomática e índice de mantenibilidad).
- **Control de Versiones:** Git y GitHub con flujo trazable de tags por etapa e higiene de repositorio (`.gitignore` y `.gitattributes`).

---

## 3. Funcionalidades del Sistema

El módulo gestiona cinco operaciones funcionales verificables sobre trámites académicos:

1. **Registrar Solicitud:** Alta del trámite validando invariantes del estudiante y calculando la prioridad automática mediante el patrón *Strategy*.
2. **Cambiar Estado:** Transición controlada entre estados válidos (`PENDIENTE`, `EN_PROCESO`, `RESUELTA`, `RECHAZADA`) protegiendo estados terminales y registrando observaciones.
3. **Asignar Responsable y Área:** Vinculación de un trámite con un responsable y sector académico, transicionando automáticamente el estado a `EN_PROCESO`.
4. **Buscar y Filtrar:** Consulta combinada de solicitudes mediante *Parameter Object* (`FiltroBusquedaSolicitud`) por estado, tipo de trámite o legajo.
5. **Generar Reporte Operativo:** Consolidación y emisión por consola de métricas estadísticas del sistema (totales, desglose por estado y solicitudes de prioridad alta).

---

## 4. Estructura del Repositorio

```text
TPI_MTS_II/
├── .gitignore                                <- Exclusión de archivos temporales, caché (__pycache__) y reportes de cobertura.
├── .gitattributes                            <- Normalización de finales de línea y detección de lenguaje.
├── README.md                                 <- Documentación general, instalación, ejecución y trazabilidad.
├── sistema_solicitudes_base.py               <- Versión inicial funcional con deuda técnica (Tag: estado-inicial).
├── sistema_solicitudes_refactorizado.py      <- Versión final desacoplada con SOLID y Clean Code (Tag: estado-refactorizado).
├── test_sistema_solicitudes.py               <- Suite de 10 pruebas unitarias AAA, Stubs, Mocks y paridad JSON (Tag: etapa-pruebas).
├── test_caracterizacion_base.py              <- Suite de 14 pruebas de caracterización base (CB-01..09) y contratos de error (CI-01..05).
├── solicitudes_db.json                       <- Archivo de persistencia JSON con registros sintéticos.
└── docs/
    ├── diagnostico_deuda_tecnica.md          <- Inventario técnico de los 9 Code Smells detectados (Tag: etapa-diagnostico).
    ├── code_review_checklist.md              <- Checklist TAC, feedback en 3 capas y dictamen en verde (Tag: etapa-docs).
    └── adr_001_arquitectura_solid.md         <- Registro de decisión arquitectónica (ADR-001).