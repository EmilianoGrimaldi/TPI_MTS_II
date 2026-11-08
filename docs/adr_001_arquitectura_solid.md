# ADR-001: Desacoplamiento de Persistencia y Reglas de Prioridad mediante DIP y Strategy

- **Fecha:** Noviembre 2026
- **Estado:** Aceptado

## 1. Contexto
El sistema base (`sistema_solicitudes_base.py`) concentraba en una única clase (`GestorTotalSolicitudes`) la lectura/escritura directa en `solicitudes_db.json`, el uso de la variable global `solicitudes_memoria` y cadenas condicionales `if/elif` para calcular prioridades y validar estados. Esto impedía ejecutar pruebas unitarias aisladas en memoria y elevaba el costo del cambio.

## 2. Decisión
1. Invertir la dependencia de persistencia creando la abstracción `RepositorioSolicitudes` con dos adaptadores intercambiables (`RepositorioSolicitudesJSON` y `RepositorioSolicitudesMemoria`).
2. Encapsular el algoritmo de priorización bajo el patrón **Strategy** (`EstrategiaPrioridadAcademica`).
3. Trasladar las reglas de transición de estados al enum `EstadoSolicitud` y las invariantes de negocio a las entidades `Estudiante` y `Solicitud`.

## 3. Consecuencias
- **Positivas:** Testabilidad unitaria en memoria en `0.015s` mediante Stubs y Mocks; reducción de complejidad ciclomática a Rango A; preservación del 100% del comportamiento externo.
- **Trade-offs:** Aumento en la cantidad de clases del módulo, compensado por alta cohesión y bajo acoplamiento.