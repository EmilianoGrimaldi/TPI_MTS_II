# Sistema de Gestión de Solicitudes Académicas

> **Asignatura:** Metodología de Sistemas II  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (UTN)  
> **Comisión:** 12  
> **Alumno:** Grimaldi Emiliano (Matrícula: 102964)  
> **Hito Actual:** `etapa-refactoring` (Evolución arquitectónica y Refactoring seguro)

---

## 1. Descripción del Proyecto

Módulo de software diseñado para centralizar la gestión de trámites estudiantiles (equivalencias, certificados de examen, cambios de comisión y revisiones de actas) en una institución universitaria.

El propósito central de este repositorio es evidenciar la **evolución profesional de un sistema existente**: partiendo de un prototipo base funcional pero con alta deuda técnica interna (`estado-inicial`), hasta alcanzar una arquitectura desacoplada, testeable y mantenible mediante refactorings seguros respaldados por principios SOLID y Clean Code (`etapa-refactoring`), garantizando **0% de regresión funcional**.

---

## 2. Tecnologías y Herramientas

- **Lenguaje:** Python 3.11+ (con tipado estático `typing`, enumeraciones `Enum` y `@dataclass`).
- **Persistencia:** Almacenamiento estructurado en archivo JSON local (`solicitudes_db.json`).
- **Análisis Estático y Calidad:** `pylint` (estilo y detección de smells) y `radon` (complejidad ciclomática).
- **Gobernanza Git:** Tags semánticos de evolución (`estado-inicial`, `etapa-diagnostico`, `etapa-refactoring`).

---

## 3. Comparación Arquitectónica: Versión Base vs. Refactorizada

| Aspecto | Versión Base (`sistema_solicitudes_base.py`) | Versión Refactorizada (`sistema_solicitudes_refactorizado.py`) |
| :--- | :--- | :--- |
| **Diseño / Cohesión** | Monolito (`GestorTotalSolicitudes`) con 7 responsabilidades mezcladas. | Arquitectura modular desacoplada cumpliendo **SRP**. |
| **Manejo del Estado** | Variable global mutable (`solicitudes_memoria`) acoplada a disco. | **Cero variables globales**; inyección de dependencias por constructor (**DIP**). |
| **Tipado y Dominio** | Obsesión por primitivos (`dict` plano, strings y números mágicos `1, 2, 3`). | Clases de dominio inmutables (`Estudiante`, `Solicitud`) y `Enum` con comportamiento. |
| **Firmas de Métodos** | Firma frágil con 8 argumentos posicionales en el alta. | **Parameter Object** (`DatosAltaSolicitud`, `FiltroBusquedaSolicitud`). |
| **Reglas de Prioridad** | Condicionales rígidos `if/elif/else` que violan OCP. | Patrón **Strategy** extensible (`EstrategiaPrioridadAcademica`). |
| **Manejo de Errores** | `print(...)` por consola y retorno booleano `return False`. | Jerarquía limpia de **Excepciones de Dominio** (`ErrorValidacionSolicitud`, etc.). |

---

## 4. Estructura del Repositorio

```text
├── README.md                              <- Especificación, instalación y guía del proyecto.
├── sistema_solicitudes_base.py            <- Código fuente original con deuda técnica (estado-inicial).
├── sistema_solicitudes_refactorizado.py   <- Código refactorizado profesional (etapa-refactoring).
├── solicitudes_db.json                    <- Archivo de persistencia física generado automáticamente.
└── docs/
    └── diagnostico_deuda_tecnica.md       <- Inventario técnico de los 9 Code Smells diagnosticados.