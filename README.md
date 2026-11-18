# Sistema de Gestión de Solicitudes Académicas — TPI Metodología de Sistemas II

> **Universidad:** Universidad Tecnológica Nacional (UTN)  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (TUPaD)  
> **Asignatura:** Metodología de Sistemas II — Comisión 12  
> **Docente Titular / Cátedra:** Metodología de Sistemas II  
> **Autor:** Grimaldi, Emiliano (Matrícula: 102964)  
> **Modalidad:** Entrega individual con justificación académica y laboral (ver Sección 11)  
> **Repositorio Oficial:** [https://github.com/EmilianoGrimaldi/TPI_MTS_II](https://github.com/EmilianoGrimaldi/TPI_MTS_II)  
> **Estado General Final:** `estado-refactorizado` / `estadorefactorizado` (Auditoría Técnica en Verde — 24/24 Tests OK)

---

## 1. Descripción y Propósito del Trabajo

Este repositorio contiene la entrega integral del **Trabajo Práctico Integrador (TPI)** para la cátedra de **Metodología de Sistemas II**, enfocado en la **evolución profesional de un sistema de software existente: calidad interna, reducción de deuda técnica, refactoring seguro y revisión técnica profesional**.

El foco de la evaluación no consiste en agregar funcionalidad por mera acumulación, sino en demostrar capacidad ingenieril para:
1. **Diagnosticar la brecha entre calidad externa e interna:** Contrastar un software funcional desde la perspectiva del usuario (Caja Negra) contra una estructura interna monolítica y acoplada (Caja Blanca).
2. **Reconocer y catalogar Deuda Técnica y Code Smells:** Identificar y priorizar debilidades arquitectónicas en el código base con métricas objetivas.
3. **Aplicar Principios SOLID y Clean Code:** Rediseñar el dominio desacoplando persistencia, reglas de negocio y canales de comunicación.
4. **Ejecutar Refactorings Seguros:** Aplicar transformaciones preservando el comportamiento observable válido mediante dobles de prueba y pruebas de caracterización.
5. **Auditar con Code Review Profesional:** Aplicar un checklist técnico estricto (TAC), registrar feedback profesional y documentar decisiones arquitectónicas (ADR-001).

---

## 2. Tecnologías y Herramientas Utilizadas

- **Lenguaje Base:** Python 3.11+ (aprovechando `typing`, `@dataclass(frozen=True)`, `Enum`, `abc.ABC`).
- **Persistencia de Datos:** Almacenamiento estructurado en archivo JSON local (`solicitudes_db.json`) con datos 100 % sintéticos y anonimizados.
- **Testing y Automatización:**
  - Biblioteca estándar `unittest` bajo el patrón **AAA (Arrange, Act, Assert)**.
  - Implementación de dobles de prueba: *Stub* en memoria (`RepositorioSolicitudesMemoria`) y *Mock* de interacción (`NotificadorMock`).
  - Pruebas de caracterización de código legado y pruebas de cambios intencionales de contrato.
- **Análisis Estático y Cobertura:**
  - `coverage` (medición estricta de *Statement Coverage* y *Branch Coverage*).
  - `pylint` (auditoría estática de estilo, legibilidad, variables globales y complejidad léxica).
  - `radon` (complejidad ciclomática *CC*, métricas en bruto *RAW* e índice de mantenibilidad *MI*).
- **Control de Versiones y Gobernanza:** Git y GitHub con flujo de tags por etapa, `.gitignore` y `.gitattributes`.

---

## 3. Funcionalidades del Dominio Académico

El módulo gestiona cinco casos de uso funcionales verificables sobre trámites universitarios (equivalencias, certificados de examen, cambios de comisión y revisiones de acta):

1. **Registrar Solicitud (Alta):** Alta de trámite validando invariantes del estudiante (legajo, nombre, correo válido), clasificación por tipo y cálculo dinámico de prioridad mediante el patrón *Strategy*.
2. **Cambiar Estado:** Transición controlada entre estados válidos (`PENDIENTE` → `EN_PROCESO` → `RESUELTA` / `RECHAZADA`), blindando estados terminales contra reaperturas indebidas y registrando observaciones.
3. **Asignar Responsable y Área:** Vinculación de un agente administrativo y su secretaría a la solicitud, transicionando automáticamente a `EN_PROCESO` y bloqueando asignaciones sobre trámites rechazados.
4. **Buscar y Filtrar Solicitudes:** Consulta multicriterio mediante un *Parameter Object* inmutable (`FiltroBusquedaSolicitud`) filtrando de forma combinada por estado, tipo de trámite y legajo estudiantil.
5. **Generar Reporte Operativo:** Cálculo y emisión formateada por consola de estadísticas consolidadas del sistema (total de solicitudes, desglose por cada estado y volumen de prioridad alta).

---

## 4. Estructura del Repositorio

```text
TPI_MTS_II/
├── .gitattributes                            <- Normalización de finales de línea LF y detección de lenguaje.
├── .gitignore                                <- Exclusión de caché (__pycache__), artefactos temporales y .coverage.
├── README.md                                 <- Guía integral del proyecto, instalación, ejecución y trazabilidad.
├── sistema_solicitudes_base.py               <- Versión inicial funcional con deuda técnica y God Object (Tag: estado-inicial).
├── sistema_solicitudes_refactorizado.py      <- Versión final profesional desacoplada con SOLID y Clean Code (Tag: estado-refactorizado).
├── test_sistema_solicitudes.py               <- Suite de 10 pruebas unitarias AAA, Stubs en memoria, Mocks y paridad JSON.
├── test_caracterizacion_base.py              <- Suite de 14 pruebas: 9 de caracterización base (CB) y 5 de contratos de error (CI).
├── solicitudes_db.json                       <- Persistencia JSON local con datos sintéticos de muestra.
└── docs/                                     <- Documentación técnica y registros de ingeniería de software.
    ├── adr_001_arquitectura_solid.md         <- Registro de Decisión Arquitectónica (ADR-001: Desacoplamiento DIP y Strategy).
    ├── diagnostico_deuda_tecnica.md          <- Matriz técnica de los 9 Code Smells catalogados (Etapa 3).
    ├── refactorings_antes_despues.md         <- Catálogo comparativo de los 5 refactorings seguros aplicados (Etapa 5).
    ├── code_review_checklist.md              <- Checklist TAC (CR-01..10), feedback en 3 capas y dictamen final (Etapa 7).
    ├── cambios_intencionales_comportamiento.md<- Análisis riguroso de preservación de flujo feliz vs. excepciones Fail-Fast.
    └── metricas_antes_despues.md             <- Tablas comparativas de Pylint, Radon CC, Radon MI y Coverage.
```

---

## 5. Requisitos y Entorno de Ejecución

### Requisitos Previos
- **Python 3.11 o superior** instalado en el sistema (`python --version`).
- **Git** instalado para verificación de ramas y tags (`git --version`).

### Instalación de Dependencias Analíticas
El núcleo del sistema y la suite de pruebas utilizan la biblioteca estándar de Python (`unittest`, `dataclasses`, `enum`, `abc`, `json`, `os`, `tempfile`).  
Para ejecutar las herramientas analíticas de cobertura y calidad estática requeridas por la cátedra, instale:

```bash
pip install coverage radon pylint
```

*(Opcional: se recomienda utilizar un entorno virtual estándar `python -m venv .venv` y activarlo previamente).*

---

## 6. Guía de Ejecución y Demostración

### 6.1. Ejecución del Sistema Base (Versión Legada — `estado-inicial`)
Ejecuta la versión monolítica inicial demostrando su funcionamiento visible (calidad externa) y persistencia en `solicitudes_db.json`:

```bash
python sistema_solicitudes_base.py
```

### 6.2. Ejecución del Sistema Refactorizado (Versión Final — `estado-refactorizado`)
Ejecuta la versión desacoplada basada en servicios de aplicación, contratos abstractos, invariantes protegidas y formateo limpio:

```bash
python sistema_solicitudes_refactorizado.py
```

> **Verificación de Paridad:** La salida emitida por consola y el esquema del archivo JSON generado son 100 % compatibles entre ambas versiones en su flujo de negocio regular.

---

## 7. Suite de Pruebas Automatizadas y Cobertura (Patrón AAA)

El proyecto cuenta con **24 pruebas automatizadas** organizadas bajo la metodología **AAA (Arrange, Act, Assert)**:

- **`test_sistema_solicitudes.py` (10 pruebas unitarias):**
  - Casos felices de alta según tipo y cálculo de prioridad (TC-01..03).
  - Blindaje ante datos inválidos de estudiante (TC-04).
  - Transición de estado a `EN_PROCESO` al asignar responsable (TC-05).
  - Bloqueo de cambios de estado sobre solicitudes cerradas o rechazadas (TC-06 y TC-07).
  - Tratamiento de solicitudes inexistentes con excepciones tipadas (TC-08).
  - Búsqueda combinada con *Parameter Object* (TC-09).
  - **Prueba de paridad de regresión antes/después** con entorno temporal aislado `tempfile.TemporaryDirectory` (TC-10).
- **`test_caracterizacion_base.py` (14 pruebas complementarias):**
  - 9 pruebas de caracterización base (CB-01..09) que fijan el comportamiento observable del código legado.
  - 5 pruebas de cambios intencionales de contrato (CI-01..05) que validan el paso de retornos booleanos silenciosos (`False`) a excepciones de dominio (`ErrorValidacionSolicitud`, `ErrorTransicionEstado`).

### Ejecución de los Tests
Para correr la suite completa en modo detallado:

```bash
python -m unittest -v test_caracterizacion_base test_sistema_solicitudes
```

*Resultado esperado:*
```text
Ran 24 tests in 0.315s
OK
```

### Medición de Cobertura de Código (Branch & Statement Coverage)
Para medir la cobertura real de ramas y sentencias sobre ambos módulos y las suites:

```bash
coverage run --branch -m unittest test_caracterizacion_base test_sistema_solicitudes
coverage report -m
```

*Reporte consolidado obtenido:*
```text
Name                                   Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------------
sistema_solicitudes_base.py              102     12     48      6    87%   ...
sistema_solicitudes_refactorizado.py     238     23     40      6    89%   ...
test_caracterizacion_base.py             111      1      2      1    98%   ...
test_sistema_solicitudes.py               96      1      2      1    98%   ...
----------------------------------------------------------------------------------
TOTAL                                    547     37     92     14    91%
```
> **Cumplimiento:** Cobertura de ramas del **89 % en el módulo refactorizado** y **91 % total**, superando con holgura el umbral estándar del 80 % definido en el TAC.

---

## 8. Auditoría Estática y Métricas de Calidad (Antes vs. Después)

### 8.1. Calificación de Código con Pylint
```bash
pylint sistema_solicitudes_base.py
# -> Calificación: 7.50 / 10 (Alertas críticas: W0603 global, R0913 exceso de parámetros)

pylint sistema_solicitudes_refactorizado.py
# -> Calificación: 8.09 / 10 (Elimina estado global y firmas largas; código limpio y tipado)
```

### 8.2. Complejidad Ciclomática con Radon (`radon cc`)
```bash
radon cc -s -a sistema_solicitudes_base.py
# -> Promedio: B (5.89). Método procesar_alta en Rango C (12).

radon cc -s -a sistema_solicitudes_refactorizado.py
# -> Promedio: A (2.47). Reducción drástica; 89.7 % de los bloques en Rango A (1 a 4).
```

### 8.3. Índice de Mantenibilidad con Radon (`radon mi`)
```bash
radon mi sistema_solicitudes_base.py          # -> A (48.14)
radon mi sistema_solicitudes_refactorizado.py   # -> A (33.28)
```

### 8.4. Cuadro Comparativo Consolidado

| Indicador / Métrica | Versión Base (`estado-inicial`) | Versión Refactorizada (`estado-refactorizado`) | Interpretación Técnica |
| :--- | :---: | :---: | :--- |
| **Calificación Pylint** | `7.50 / 10` | `8.09 / 10` | Erradicación de `global` y firmas largas; código estructurado. |
| **Complejidad Promedio (Radon CC)** | `B (5.89)` | `A (2.47)` | Reducción de más del 58 % en la complejidad promedio. |
| **Bloque más complejo** | `procesar_alta: C (12)` | `generar_resumen: C (11)` | La lógica de negocio bajó a A (1); el reporte queda para mejora futura. |
| **Bloques en Rango B o C** | 5 de 9 (55.5 %) | 6 de 58 (10.3 %) | Descomposición en métodos cohesivos y funciones breves. |
| **Parámetros en el Alta** | 8 argumentos posicionales | 1 (`DatosAltaSolicitud`) | Aplicación estricta de *Introduce Parameter Object*. |
| **Estado Global Mutable** | Sí (`solicitudes_memoria`) | **No (0 variables globales)** | Cumplimiento estricto de DIP; persistencia desacoplada. |
| **Tests Automatizados** | 0 pruebas | **24 pruebas (100 % OK)** | Suite completa bajo patrón AAA con Stubs y Mocks. |
| **Cobertura de Ramas** | N/A | **89 % (91 % total)** | Supera el umbral industrial del 80 % exigido en el TAC. |

---

## 9. Trazabilidad Git y Tags Obligatorios

El repositorio implementa un historial de commits ordenado y semántico que permite auditar cada etapa solicitada por la cátedra:

| Tag de Git | Commit | Etapa del TPI | Hito Técnico Verificable |
| :--- | :---: | :---: | :--- |
| `estado-inicial` | `089c161` | Etapa 1 | Entrega del sistema base funcional con deuda técnica y God Object. |
| `etapa-diagnostico` | `5e8cacc` | Etapas 2 y 3 | Diagnóstico de calidad y matriz formal de 9 Code Smells en `docs/`. |
| `etapa-refactoring` | `2ff8cfc` | Etapas 4 y 5 | Aplicación de SOLID, Clean Code y los 5 refactorings seguros documentados. |
| `etapa-pruebas` | `b243949` | Etapa 6 | Suite de pruebas unitarias AAA, pruebas de paridad y medición de cobertura. |
| `etapa-docs` | `120e884` | Etapa 7 | Checklist TAC de Code Review, ADR-001 y cierre documental. |
| `estadorefactorizado` / `estado-refactorizado` | `120e884` | Etapa 8 | Estado final consolidado con suite en verde (24/24 OK) y auditoría aprobada. |

> **Nota de compatibilidad:** Conforme a la consigna textual de la página 3 (`estadorefactorizado` sin guion) y la nomenclatura habitual de etiquetas (`estado-refactorizado` con guion), se publicaron **ambos tags** apuntando al commit final `120e884`.

Para inspeccionar cualquier estado histórico del código:
```bash
git checkout estado-inicial        # Código base antes del refactoring
git checkout etapa-refactoring     # Momento de aplicación de patrones SOLID
git checkout estado-refactorizado  # Versión final consolidada
```

---

## 10. Documentación Complementaria en `/docs`

Para un análisis técnico en profundidad, consulte los documentos complementarios en la carpeta [`docs/`](docs/):

1. **[ADR-001: Arquitectura SOLID y Desacoplamiento DIP](docs/adr_001_arquitectura_solid.md):** Decisión formal de diseño, contexto, alternativas evaluadas y consecuencias.
2. **[Diagnóstico de Deuda Técnica y Code Smells](docs/diagnostico_deuda_tecnica.md):** Detalle de los 9 smells (CS-01 a CS-09) con impacto estructural y riesgos.
3. **[Catálogo de Refactorings Antes vs. Después](docs/refactorings_antes_despues.md):** Transformaciones de código línea por línea para R1 (Parameter Object), R2 (Extract Method), R3 (Move Method), R4 (Strategy) y R5 (Extract Class/DIP).
4. **[Checklist de Code Review Profesional](docs/code_review_checklist.md):** 10 Criterios de Aceptación Técnica (TAC), feedback en 3 capas y acciones correctivas aplicadas.
5. **[Cambios Intencionales de Comportamiento](docs/cambios_intencionales_comportamiento.md):** Justificación de la preservación del camino feliz vs. adopción de excepciones Fail-Fast.
6. **[Métricas Detalladas Antes vs. Después](docs/metricas_antes_despues.md):** Reportes analíticos de Pylint, Radon y Coverage.

---

## 11. Modalidad de Entrega, Autoría y Defensa

- **Modalidad:** Individual justificada conforme a la Sección 1 de la consigna oficial.
- **Justificación:** Por incompatibilidad de horarios laborales y cursada asincrónica a distancia para coordinar entregas sincrónicas grupales, se optó por el desarrollo individual integral.
- **Autor y Responsable Técnico:** Emiliano Grimaldi (Matrícula: 102964 — Comisión 12).  
  El autor asumió de forma integral el 100 % del relevamiento del sistema base, diagnóstico de deuda técnica, diseño arquitectónico SOLID, programación de refactorings, desarrollo de la suite de 24 pruebas, documentación técnica y defensa en video.

---

## 12. Declaración de Uso de Inteligencia Artificial

En estricto cumplimiento de la **Sección 7 de la consigna oficial**:
- **Herramientas utilizadas:** Google Gemini y Claude (Anthropic).
- **Finalidad:** Apoyo para la exploración de alternativas de diseño SOLID, asistencia en la estructuración de plantillas Markdown para la carpeta `/docs` y depuración cruzada de casos de borde en pruebas unitarias.
- **Grado de intervención y autoría:** Asistencia y copiloto técnico. La totalidad del código fuente, las pruebas unitarias y los comandos fueron ejecutados, probados localmente, validados mediante herramientas analíticas (`unittest`, `coverage`, `pylint`, `radon`) y comprendidos en su totalidad por el autor. Se utilizaron exclusivamente datos 100 % sintéticos y anonimizados.
