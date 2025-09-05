# ===============================================================
#          .-.                                           .-.
#         / (_)                          .--.    .-.--.-'   
#        /      .-.  )  (   ).--..-.    /    )`-' (  (_)    
#       /      (  | (    ) /    (  |   /    /      `-.      
#    .-/.    .-.`-'-'`--':/      `-'-'(    /     _    )     
#   (_/ `-._.                          `-.'     (_.--'      
# ===============================================================
# Este programa es una simulación del funcionamiento de un SO por
# fines educativos.

import os
import math
import time
from logo import logo
from validaciones import *
from Objetos import ObjProceso
from Objetos import ObjOperacion
from rich.live import Live
from rich.console import Console
from layout import *

console = Console()

# Función de apertura
logo()

input_valido = False
while input_valido == False:
    # Pedimos la cantidad de procesos a ejecutar
    os.system('clear')
        
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

os.system("clear")

for j in range(num_lotes):
    
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

terminados = []
global_time = 0

with Live(make_layout(global_time, lista_lotes[0], 1, lista_lotes[0][0], terminados, num_lotes),
          refresh_per_second=2) as live:

    for num_lote, lote in enumerate(lista_lotes, start=1):

        # mientras aún queden procesos en este lote
        while lote:
            proceso = lote.pop(0)  # siempre tomamos el primero pendiente
            
            while proceso.restante > 0:
                proceso.transcurrido += 1
                proceso.restante -= 1
                global_time += 1
                time.sleep(1)

                # actualización en tiempo real
                live.update(make_layout(global_time, lote, num_lote, proceso, terminados, num_lotes))

            # Calcular resultado al terminar
            operador = proceso.operacion.operador
            match operador:
                case '+':
                    proceso.resultado = proceso.operacion.num_a + proceso.operacion.num_b
                case '-':
                    proceso.resultado = proceso.operacion.num_a - proceso.operacion.num_b
                case '*':
                    proceso.resultado = proceso.operacion.num_a * proceso.operacion.num_b
                case '/':
                    proceso.resultado = round(proceso.operacion.num_a / proceso.operacion.num_b, 2)
                case '^':
                    proceso.resultado = pow(proceso.operacion.num_a, proceso.operacion.num_b)
                case '%':
                    proceso.resultado = proceso.operacion.num_a % proceso.operacion.num_b

            # mover el proceso al historial de terminados
            terminados.append(proceso)

            # actualización en tiempo real después de moverlo
            live.update(make_layout(global_time, lote, num_lote, proceso, terminados, num_lotes))

    # al final mostramos el último estado
    ultimo_layout = make_layout(global_time, lote, num_lote, proceso, terminados, num_lotes)
    console.print(ultimo_layout)