# Catálogo de Refactorings Seguros (Comparación Antes vs. Después)

> **Proyecto:** Sistema de Gestión de Solicitudes Académicas  
> **Asignatura:** Metodología de Sistemas II (UTN - TUPaD) — Comisión 12  
> **Autor:** Grimaldi, Emiliano (Matrícula: 102964)  
> **Hito Git:** `etapa-refactoring` (Commit `2ff8cfc`) → `estado-refactorizado`

---

## 1. Marco de Aplicación

Siguiendo la definición de **Martin Fowler**, cada refactoring aplicado transforma la estructura interna del código para mejorar su legibilidad, cohesión y mantenibilidad sin alterar negativamente su comportamiento externo observable.

En cumplimiento con la **Etapa 5** de la consigna oficial (que exige al menos 4 refactorings documentados incluyendo *Extract Method*, *Move Method* e *Introduce Parameter Object*), se aplicaron **5 refactorings estructurales** verificados mediante una suite de **24 pruebas automatizadas** (`10` unitarias AAA + `9` de caracterización + `5` de contrato de errores).

| ID | Técnica de Refactoring | Code Smells Mitigados | Principios SOLID / Clean Code | Pruebas que lo Verifican |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | **Introduce Parameter Object** | `CS-05` (Long Parameter List), `CS-03` | Clean Code (Firmas limpias e inmutabilidad) | `TC-01..03`, `TC-09` |
| **R2** | **Extract Method** | `CS-04` (Long Method), `CS-08` (DRY) | SRP, Nivel único de abstracción | `TC-01..03`, `TC-10` |
| **R3** | **Move Method** | `CS-07` (Feature Envy), `CS-03`, `CS-09` | Alta cohesión, encapsulamiento de invariantes | `TC-04..07`, `CI-01..05` |
| **R4** | **Replace Conditional with Strategy & State Rules** | `CS-06` (Condicionales rígidos), `CS-03` | OCP (Abierto/Cerrado), Patrón *Strategy* | `TC-01..03`, `TC-06`, `CI-03` |
| **R5** | **Extract Class & Dependency Inversion** | `CS-01` (God Object), `CS-02` (Estado global), `CS-08` | SRP, DIP, LSP, ISP, Principio DRY | Suite completa (`24/24`), `TC-10` |

---

## 2. Desarrollo Detallado: Antes vs. Después

### Refactoring 1 (R1): Introduce Parameter Object (Introducción de Objeto de Parámetros)

- **Code Smell que resuelve:** `CS-05: Long Parameter List` (8 parámetros posicionales en `procesar_alta`, L. 23) y parámetros opcionales dispersos en `buscar` (L. 92).
- **Motivación técnica:** Cuando un conjunto de datos viaja junto de forma recurrente, reemplazar la lista extensa de argumentos por un objeto inmutable (`@dataclass(frozen=True)`) reduce la complejidad de las firmas, evita invertir argumentos `str` por error y explicita el contrato de entrada.

#### ANTES (`sistema_solicitudes_base.py` — Líneas 23 y 92)
```python
# Firma fragil con 8 argumentos posicionales sueltos
def procesar_alta(self, id_sol, legajo, nom_est, email_est, carrera, tipo, desc, urgente):
    ...

# Firma con multiples parametros opcionales sueltos
def buscar(self, filtro_estado=None, filtro_tipo=None, filtro_legajo=None):
    ...