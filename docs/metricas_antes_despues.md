# Métricas antes / después (datos reales, ver `docs/evidencias/`)

| Métrica | Base | Refactorizado | Lectura |
|---------|------|---------------|---------|
| Calificación pylint | 7.50 / 10 | 8.09 / 10 | Mejora moderada; quedan advertencias de docstrings. |
| Complejidad ciclomática promedio (radon cc) | **B (5.89)** | **A (2.47)** | Mejora clara en el promedio. |
| Método más complejo | `procesar_alta` = **C (12)** | `generar_resumen` = **C (11)** | El peor caso se desplazó al reporte; sigue pendiente simplificarlo (p. ej. con `collections.Counter`). |
| Métodos/clases en B o C | 5 de 9 bloques | 6 de 58 bloques | La complejidad se reparte en muchas piezas pequeñas. |
| Parámetros de `procesar_alta` / `registrar_solicitud` | 8 | 1 (Parameter Object) | SRP/Clean Code. |
| Estado global mutable | Sí (`solicitudes_memoria`) | No | DIP: dependencias inyectadas. |
| Tests automatizados | 0 | 10 + 14 (caracterización y cambios) | Todos en verde. |
| Cobertura (refactorizado) | n/a | 86 % (branch) | Supera el 80 % de la DoD. |
| Líneas (LOC) | 158 | 460 | Más código por más clases: es el *trade-off* aceptado (ADR-001). |
| Índice de mantenibilidad (radon mi) | A (48.14) | A (33.28) | Baja por tamaño, pero se mantiene en rango A. No se presenta como mejora. |

> Corrección respecto de versiones previas de la documentación: la complejidad **no** es Rango A "en todos los métodos";
> es Rango A en promedio, con 6 bloques en B/C.
