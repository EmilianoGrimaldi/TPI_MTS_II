# Cambios intencionales de comportamiento (Base → Refactorizado)

> Etapa 6 – Pruebas y verificación. Evidencia ejecutable: `docs/evidencias/comparacion_comportamiento.txt`
> y `test_caracterizacion_base.py` (clases `TestCaracterizacionBase` y `TestCambiosIntencionales`).

## 1. Qué se preserva (comportamiento externo "feliz")

Para los flujos válidos de las 5 operaciones, la versión refactorizada produce lo mismo que la base:

- Misma salida de consola del demo (`docs/evidencias/demo_base.txt` vs `demo_refactorizado.txt`: `diff` sin diferencias).
- Mismo texto de reporte y mismos campos en `solicitudes_db.json` (test `TC-10`, paridad antes/después).
- Misma regla de prioridad (ALTA si urgente o `REVISION_ACTA`; MEDIA para `EQUIVALENCIA`/`CAMBIO_COMISION`; BAJA el resto).
- Misma regla de cierre: una solicitud `RESUELTA`/`RECHAZADA` no se reabre.

## 2. Qué cambia a propósito (contrato de errores y validación)

| # | Escenario | Base (`estado-inicial`) | Refactorizado | Justificación |
|---|-----------|-------------------------|---------------|---------------|
| 1 | Datos de alta inválidos (legajo vacío, email sin `@`) | `print` + `return False` | `ErrorValidacionSolicitud` | Clean Code: no mezclar UI con control de errores (CS-09). |
| 2 | Email `a@b` (dominio sin punto) | Se acepta | `ErrorValidacionSolicitud` | Invariante más estricta, ubicada en la entidad `Estudiante` (Move Method, CS-07). |
| 3 | Legajo con solo espacios | Se acepta | `ErrorValidacionSolicitud` | Se valida con `strip()`; el base solo comparaba con `""`. |
| 4 | `id` inexistente (cambiar estado / asignar) | `return False` silencioso | `SolicitudNoEncontradaError` | El fallo ya no se confunde con "operación rechazada". |
| 5 | `EN_PROCESO → EN_PROCESO` | Se permite | `ErrorTransicionEstado` | Transición sin efecto; el mapa declarativo de transiciones solo admite pasos reales (OCP). |
| 6 | Cambio a un estado no permitido (p. ej. `PENDIENTE`) | `return False` silencioso | `ErrorTransicionEstado` | Error explícito y tipado. |
| 7 | Cambiar estado de solicitud cerrada | `print` + `return False` | `ErrorTransicionEstado` | Misma regla de negocio, mejor contrato. |
| 8 | Responsable/área vacíos | Se acepta | `ErrorValidacionSolicitud` | Invariante en `ResponsableArea`. |
| 9 | Valor de retorno de las operaciones | `True` / `False` | La `Solicitud` actualizada | Permite encadenar y verificar sin releer disco. |

## 3. Comportamiento que NO se modificó (deuda reconocida)

- `asignar_responsable` sobre una solicitud `RESUELTA` se sigue permitiendo (igual que en la base). Solo se bloquea sobre `RECHAZADA`.
- No se valida unicidad del `id`: dos altas con el mismo id se aceptan en ambas versiones.
- Un tipo inválido (`"BECA"`) ahora falla con `ValueError` al construir `TipoSolicitud("BECA")`, es decir, **fuera** de la jerarquía `ErrorDominioSolicitud`. Mejora pendiente: capturarlo en la capa de entrada y relanzarlo como `ErrorValidacionSolicitud`.

## 4. Conclusión

La afirmación correcta no es "0 % de diferencias", sino: **el comportamiento válido se conserva (verificado por paridad), y los
cambios en el manejo de errores y en la validación son deliberados, están justificados y cubiertos por tests.**
