import json
import os
from datetime import datetime

# Variables globales y archivo acoplado directamente
DB_FILE = "solicitudes_db.json"
solicitudes_memoria = []

class GestorTotalSolicitudes:
    def cargar_datos(self):
        global solicitudes_memoria
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                solicitudes_memoria = json.load(f)
        else:
            solicitudes_memoria = []

    def guardar_datos(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(solicitudes_memoria, f, indent=4, ensure_ascii=False)

    # Operacion 1: Registrar solicitud (Long Method, Long Parameter List, Magic Values)
    def procesar_alta(self, id_sol, legajo, nom_est, email_est, carrera, tipo, desc, urgente):
        self.cargar_datos()
        if legajo == "" or nom_est == "" or "@" not in email_est:
            print("Error en datos del estudiante")
            return False
        if tipo != "EQUIVALENCIA" and tipo != "CERTIFICADO" and tipo != "CAMBIO_COMISION" and tipo != "REVISION_ACTA":
            print("Error: tipo invalido")
            return False

        # Calculo de prioridad acoplado con condicionales rigidos
        if urgente == True or tipo == "REVISION_ACTA":
            prio = 1 # 1 es Alta
        elif tipo == "EQUIVALENCIA" or tipo == "CAMBIO_COMISION":
            prio = 2 # 2 es Media
        else:
            prio = 3 # 3 es Baja

        nueva = {
            "id": id_sol,
            "legajo": legajo,
            "nombre_estudiante": nom_est,
            "email": email_est,
            "carrera": carrera,
            "tipo": tipo,
            "descripcion": desc,
            "prioridad": prio,
            "estado": "PENDIENTE",
            "responsable": "SIN_ASIGNAR",
            "area": "NINGUNA",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "obs": ""
        }
        solicitudes_memoria.append(nueva)
        self.guardar_datos()
        print(f"Notificando por EMAIL a {email_est}: Solicitud {id_sol} creada con prioridad {prio}")
        return True

    # Operacion 2: Cambiar estado
    def cambiar_estado(self, id_sol, nuevo_est, observacion):
        self.cargar_datos()
        for s in solicitudes_memoria:
            if s["id"] == id_sol:
                if s["estado"] == "RESUELTA" or s["estado"] == "RECHAZADA":
                    print("No se puede cambiar una solicitud cerrada")
                    return False
                if nuevo_est == "EN_PROCESO" or nuevo_est == "RESUELTA" or nuevo_est == "RECHAZADA":
                    s["estado"] = nuevo_est
                    s["obs"] = observacion
                    self.guardar_datos()
                    print(f"Estado actualizado a {nuevo_est}")
                    return True
        return False

    # Operacion 3: Asignar responsable
    def asignar_responsable(self, id_sol, nom_resp, nom_area):
        self.cargar_datos()
        for s in solicitudes_memoria:
            if s["id"] == id_sol:
                if s["estado"] == "RECHAZADA":
                    return False
                s["responsable"] = nom_resp
                s["area"] = nom_area
                if s["estado"] == "PENDIENTE":
                    s["estado"] = "EN_PROCESO"
                self.guardar_datos()
                return True
        return False

    # Operacion 4: Buscar y filtrar solicitudes
    def buscar(self, filtro_estado=None, filtro_tipo=None, filtro_legajo=None):
        self.cargar_datos()
        res = []
        for s in solicitudes_memoria:
            ok = True
            if filtro_estado is not None and s["estado"] != filtro_estado:
                ok = False
            if filtro_tipo is not None and s["tipo"] != filtro_tipo:
                ok = False
            if filtro_legajo is not None and s["legajo"] != filtro_legajo:
                ok = False
            if ok:
                res.append(s)
        return res

    # Operacion 5: Generar reporte basico
    def generar_reporte(self):
        self.cargar_datos()
        tot = len(solicitudes_memoria)
        pend = 0
        proc = 0
        resueltas = 0
        rech = 0
        alta = 0
        for s in solicitudes_memoria:
            if s["estado"] == "PENDIENTE": pend += 1
            elif s["estado"] == "EN_PROCESO": proc += 1
            elif s["estado"] == "RESUELTA": resueltas += 1
            elif s["estado"] == "RECHAZADA": rech += 1
            if s["prioridad"] == 1: alta += 1
        rep = f"=== REPORTE ===\nTotal: {tot} | Pendientes: {pend} | En Proceso: {proc} | Resueltas: {resueltas} | Rechazadas: {rech} | Prioridad Alta: {alta}"
        print(rep)
        return rep


# Funcion de prueba con datos sinteticos para verificar ejecucion por consola
def ejecutar_prueba_consola():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    gestor = GestorTotalSolicitudes()

    # 1. Alta de solicitudes con datos ficticios (Operacion 1)
    gestor.procesar_alta(
        101, "L-45890", "Ana Perez", "ana.perez@tup.utn.edu.ar",
        "TUP", "EQUIVALENCIA", "Equivalencia de Programacion I", False
    )
    gestor.procesar_alta(
        102, "L-46120", "Lucas Gomez", "lucas.gomez@tup.utn.edu.ar",
        "TUP", "REVISION_ACTA", "Nota de examen final no reflejada en acta", True
    )

    # 2. Asignacion de responsable y area (Operacion 3)
    gestor.asignar_responsable(102, "Carlos Ruiz", "Secretaria Academica")

    # 3. Cambio de estado de solicitud (Operacion 2)
    gestor.cambiar_estado(102, "RESUELTA", "Acta rectificada correctamente")

    # 4. Busqueda y filtrado de solicitudes pendientes (Operacion 4)
    pendientes = gestor.buscar(filtro_estado="PENDIENTE")

    # 5. Generacion de reporte basico (Operacion 5)
    gestor.generar_reporte()


if __name__ == "__main__":
    ejecutar_prueba_consola()