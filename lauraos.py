# ----------------------------
#           LauraOS
# ----------------------------
# Este programa es una simulación
# del funcionamiento de un SO por
# fines educativos

import os
import math
import time
from logo import logo
from validaciones import *
from Objetos import ObjProceso
from Objetos import ObjOperacion
from rich.live import Live
from layout import *

logo()

input_valido = False
while input_valido == False:
    # Pedimos la cantidad de procesos a ejecutar
    os.system('cls')
        
    num_procesos = validar_num_procesos()

    # Cada lote está compuesto por 4 procesos 
    if num_procesos > 0:
        num_lotes = math.ceil(num_procesos/4)
        input_valido = True
    else:
        # Repite el ciclo para inputs no válidos
        print("Entrada no válida.")
        input("Presiona Enter para continuar...")
        input_valido = False

lista_lotes         = []
lista_id            = []
procesos_creados    = 0

for j in range(num_lotes):
    os.system("cls")
    
    if num_lotes > 1:
        print(f"Vas a ejecutar {num_procesos} procesos.")
        print(f"Los procesos se han separado en {num_lotes} lotes.")
    else:
        print(f"Vas a ejecutar {num_procesos} proceso.")
        print(f"Se ejecutarán en {num_lotes} lote.")

    lote_procesos = []
    num_procesos_lote = min(4, num_procesos - procesos_creados)
    for i in range(num_procesos_lote):
        print(f"\n===== Lote {j + 1}: Proceso {i + 1} =====")
        
        # ID:
        id = validar_id(lista_id)
        lista_id.append(id)
        
        # Nombre:
        nombre = input("Nombre del propietario del proceso: ")

        # Operación:
        print("Operación:")    
        num_a, num_b, operador = validar_operacion()
        
        # TME:
        tme = validar_tme()
        
        operacion   = ObjOperacion(num_a, num_b, operador)
        proceso     = ObjProceso(id, nombre, operacion, tme)
        lote_procesos.append(proceso)
        procesos_creados += 1
    lista_lotes.append(lote_procesos)
    
procesos_pendientes = procesos_creados

with Live(render_layout(0, 2, lote_demo, proceso_demo, terminados_demo), refresh_per_second=2) as live:
    for tiempo in range(6):
        proceso_demo["transcurrido"] = tiempo
        proceso_demo["restante"] = proceso_demo["tme"] - tiempo
        if proceso_demo["restante"] == 0:
            terminados_demo.append(
                {"id": proceso_demo["id"], "operacion": proceso_demo["operacion"], "resultado": 8}
            )
        live.update(render_layout(tiempo, 1, lote_demo, proceso_demo, terminados_demo))
        time.sleep(1)