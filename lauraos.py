# ===============================================================
#          .-.                                           .-.
#         / (_)                          .--.    .-.--.-'   
#        /      .-.  )  (   ).--..-.    /    )`-' (  (_)    
#       /      (  | (    ) /    (  |   /    /      `-.      
#    .-/.    .-.`-'-'`--':/      `-'-'(    /     _    )     
#   (_/ `-._.                          `-.'     (_.--'      
# ===============================================================
# Este programa es una simulación del funcionamiento de un SO por fines educativos.

import math
import time
import keyboard
from logo import logo
from clear_screen import clear_screen
from validaciones import *
from Objetos import ObjProceso
from Objetos import ObjOperacion
from rich.live import Live
from rich.console import Console
from layout import *

console = Console()

# --- Banderas globales para interrupciones ---
interrupcion_io = False
interrupcion_error = False
pausa = False

# --- Funciones para manejar las interrupciones ---
def gestionar_interrupcion_io(e):
    global interrupcion_io
    if not pausa: # Las interrupciones no se registran si el programa está en pausa
        interrupcion_io = True

def gestionar_error(e):
    global interrupcion_error
    if not pausa:
        interrupcion_error = True

def gestionar_pausa(e):
    global pausa
    pausa = True

def gestionar_continuar(e):
    global pausa
    pausa = False

# --- Asignación de teclas a las funciones ---
keyboard.on_press_key("e", gestionar_interrupcion_io, suppress=True)
keyboard.on_press_key("w", gestionar_error, suppress=True)
keyboard.on_press_key("p", gestionar_pausa, suppress=True)
keyboard.on_press_key("c", gestionar_continuar, suppress=True)


# Función de apertura
logo()

input_valido = False
while not input_valido:
    clear_screen()
    num_procesos = validar_num_procesos()
    if num_procesos > 0:
        num_lotes = math.ceil(num_procesos / 4)
        input_valido = True
    else:
        print("Entrada no válida.")
        input("Presiona Enter para continuar...")

lista_lotes = []
lista_id = []
procesos_creados = 0

clear_screen()

for j in range(num_lotes):
    print(f"Vas a ejecutar {num_procesos} procesos en {num_lotes} lotes.")
    lote_procesos = []
    num_procesos_lote = min(4, num_procesos - procesos_creados)
    for i in range(num_procesos_lote):
        print(f"\n===== Lote {j + 1}: Proceso {i + 1} =====")
        id = validar_id(lista_id)
        lista_id.append(id)
        print(f"ID: {id}")
        print("Operación:")
        num_a, num_b, operador = validar_operacion()
        tme = validar_tme()
        print(f"TME: {tme}")
        operacion = ObjOperacion(num_a, num_b, operador)
        proceso = ObjProceso(id, operacion, tme)
        lote_procesos.append(proceso)
        procesos_creados += 1
    lista_lotes.append(lote_procesos)

terminados = []
pc = 0

clear_screen()

with Live(make_layout(pc, lista_lotes[0], 1, lista_lotes[0][0], terminados, num_lotes),
          refresh_per_second=2) as live:

    for num_lote, lote in enumerate(lista_lotes, start=1):
        while lote:
            proceso = lote.pop(0)
            
            # Bandera local para el proceso actual
            proceso_fue_interrumpido = False

            while proceso.restante > 0:
                # --- Lógica de Pausa y Continuar ---
                while pausa:
                    live.update(make_layout(pc, lote, num_lote, proceso, terminados, num_lotes))
                    time.sleep(0.1)

                # --- Lógica de Interrupción por I/O (Tecla E) ---
                if interrupcion_io:
                    lote.append(proceso)
                    proceso_fue_interrumpido = True
                    break

                # --- Lógica de Interrupción por Error (Tecla W) ---
                if interrupcion_error:
                    proceso.resultado = "Error"
                    terminados.append(proceso)
                    proceso_fue_interrumpido = True
                    break

                proceso.transcurrido += 1
                proceso.restante -= 1
                pc += 1
                live.update(make_layout(pc, lote, num_lote, proceso, terminados, num_lotes))
                time.sleep(1)

            # --- Lógica al finalizar un proceso ---
            
            # Limpiamos las banderas globales después de que el ciclo de un proceso termina.
            # Esto previene que la interrupción "se fugue" al siguiente proceso.
            interrupcion_io = False
            interrupcion_error = False

            # Si el proceso NO fue interrumpido, significa que terminó normalmente.
            if not proceso_fue_interrumpido:
                operador = proceso.operacion.operador
                match operador:
                    case '+': proceso.resultado = proceso.operacion.num_a + proceso.operacion.num_b
                    case '-': proceso.resultado = proceso.operacion.num_a - proceso.operacion.num_b
                    case '*': proceso.resultado = proceso.operacion.num_a * proceso.operacion.num_b
                    case '/': proceso.resultado = round(proceso.operacion.num_a / proceso.operacion.num_b, 2)
                    case '^': proceso.resultado = pow(proceso.operacion.num_a, proceso.operacion.num_b)
                    case '%': proceso.resultado = proceso.operacion.num_a % proceso.operacion.num_b
                terminados.append(proceso)

            # Actualizamos la pantalla para reflejar el estado final del proceso
            live.update(make_layout(pc, lote, num_lote, proceso, terminados, num_lotes))

    # Mostramos el último estado
    #console.print(make_layout(pc, lote, num_lote, proceso, terminados, num_lotes))
    
    # Pausa final para que el usuario vea los resultados
    input("Presiona Enter para salir...")