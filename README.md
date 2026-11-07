# Sistema de Gestión de Solicitudes Académicas (Versión Base)

> **Materia:** Metodología de Sistemas II  
> **Carrera:** Tecnicatura Universitaria en Programación a Distancia (UTN)  
> **Comisión:** 12  
> **Alumno:** Grimaldi Emiliano (Matrícula: 102964)  
> **Tag de Versión:** `estado-inicial`

---

## 1. Descripción del Proyecto

El **Sistema de Gestión de Solicitudes Académicas** es un módulo desarrollado para centralizar la recepción, clasificación, asignación y seguimiento de trámites estudiantiles (tales como certificados de examen, equivalencias de materias, cambios de comisión y revisiones de actas).

El proyecto se presenta como un prototipo funcional en su versión base (`estado-inicial`), diseñado con el objetivo de someter su estructura interna a un diagnóstico de calidad, auditoría de deuda técnica y posterior refactorización segura sin alterar su comportamiento observable.

---

## 2. Tecnologías Utilizadas

- **Lenguaje:** Python 3.11+
- **Persistencia:** Almacenamiento estructurado en archivo plano local (`solicitudes_db.json`)
- **Control de Versiones:** Git y GitHub con flujo de tags para hitos de evaluación (`estado-inicial`)

---

## 3. Funcionalidades del Sistema Base

El módulo implementa las siguientes operaciones verificables:

1. **Registrar Solicitud (`procesar_alta`):** Da de alta un nuevo trámite validando datos básicos del estudiante y asignando una prioridad operativa inicial.
2. **Cambiar Estado (`cambiar_estado`):** Permite realizar la transición entre estados válidos (`PENDIENTE`, `EN_PROCESO`, `RESUELTA`, `RECHAZADA`) e incorporar observaciones.
3. **Asignar Responsable y Área (`asignar_responsable`):** Vincula la solicitud activa a un agente administrativo o sector resolutivo.
4. **Buscar y Filtrar (`buscar`):** Permite consultar solicitudes filtrando por estado, tipo de trámite o legajo del estudiante.
5. **Generar Reporte Operativo (`generar_reporte`):** Consolida métricas del estado del sistema (totales, pendientes, resueltas y solicitudes de prioridad alta).

---

## 4. Requisitos Previos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/EmilianoGrimaldi/TPI_MTS_II.git](https://github.com/EmilianoGrimaldi/TPI_MTS_II.git)
   cd TPI_MTS_II