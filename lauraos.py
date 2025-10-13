import math
import time
import keyboard
import random
from collections import deque
from logo import logo
from clear_screen import clear_screen
from validaciones import *
from Objetos import ObjProceso, ObjOperacion
from rich.live import Live
from rich.console import Console
from rich.table import Table
from layout import *

console = Console()

# --- Banderas para interrupciones ---
interrupcion_io = False
interrupcion_error = False
pausa = False
# [NUEVO] Banderas para 'N' y 'B'
crear_nuevo_proceso = False
mostrar_bcp = False

# --- Funciones para manejar las interrupciones ---
def gestionar_interrupcion_io(e):
    global interrupcion_io
    if not pausa: interrupcion_io = True

def gestionar_error(e):
    global interrupcion_error
    if not pausa: interrupcion_error = True

def gestionar_pausa(e):
    global pausa
    pausa = True

def gestionar_continuar(e):
    global pausa, mostrar_bcp
    pausa = False
    mostrar_bcp = False # 'C' también sale de la vista BCP

def gestionar_crear_nuevo(e):
    global crear_nuevo_proceso
    if not pausa: crear_nuevo_proceso = True

def gestionar_mostrar_bcp(e):
    global mostrar_bcp, pausa
    # 'B' activa la vista BCP y pausa la simulación
    if not mostrar_bcp:
        mostrar_bcp = True
        pausa = True

# --- Asignación de teclas ---
keyboard.on_press_key("e", gestionar_interrupcion_io, suppress=True)
keyboard.on_press_key("w", gestionar_error, suppress=True)
keyboard.on_press_key("p", gestionar_pausa, suppress=True)
keyboard.on_press_key("c", gestionar_continuar, suppress=True)
keyboard.on_press_key("n", gestionar_crear_nuevo, suppress=True)
keyboard.on_press_key("b", gestionar_mostrar_bcp, suppress=True)


# =============================================================================
# --- PROGRAMA PRINCIPAL ---
# =============================================================================
logo()
num_procesos = validar_num_procesos()

# --- Colas de Estados ---
cola_nuevos = deque()
cola_listos = deque()
cola_bloqueados = deque()
procesos_terminados = []
proceso_en_ejecucion = None
lista_id = []
todos_los_procesos = [] # Lista maestra para el BCP

# --- Creación de procesos ---
clear_screen()
print(f"Creando {num_procesos} procesos iniciales...")
for _ in range(num_procesos):
    id = validar_id(lista_id)
    lista_id.append(id)
    num_a, num_b, operador = validar_operacion()
    tme = validar_tme()
    operacion = ObjOperacion(num_a, num_b, operador)
    proceso = ObjProceso(id, operacion, tme)
    cola_nuevos.append(proceso)
    todos_los_procesos.append(proceso)

# --- SIMULACIÓN PRINCIPAL ---
pc = 0
MAX_PROCESOS_EN_MEMORIA = 4

# --- CARGA INICIAL ANTES DE QUE EL RELOJ COMIENCE ---
num_a_admitir = min(len(cola_nuevos), MAX_PROCESOS_EN_MEMORIA)
for _ in range(num_a_admitir):
    proceso_admitido = cola_nuevos.popleft()
    proceso_admitido.tiempo_llegada = 0
    proceso_admitido.estado = "Listo"
    cola_listos.append(proceso_admitido)
if cola_listos:
    proceso_en_ejecucion = cola_listos.popleft()
    proceso_en_ejecucion.tiempo_primera_ejecucion = 0
    proceso_en_ejecucion.estado = "Ejecución"

with Live(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion), 
          refresh_per_second=4, screen=True, vertical_overflow="visible") as live:

    while cola_nuevos or cola_listos or cola_bloqueados or proceso_en_ejecucion:
        
        # --- PAUSA Y VISTA BCP ---
        if pausa:
            # Si la pausa fue por la tecla 'B', mostramos la tabla BCP
            if mostrar_bcp:
                live.stop() # Detenemos el live display para imprimir la tabla estática
                clear_screen()
                console.print(tabla_bcp(todos_los_procesos, pc))
                console.print("\n[bold yellow]Mostrando BCP. Simulación en Pausa. Presiona 'C' para continuar...[/bold yellow]")
                # Esperamos a que la tecla 'C' ponga mostrar_bcp y pausa en False
                while mostrar_bcp:
                    time.sleep(0.1)
                clear_screen()
                live.start() # Reanudamos el live display
            else: # Pausa normal con 'P'
                while pausa:
                    time.sleep(0.1)
        
        live.update(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion))
        time.sleep(1)

        # --- LÓGICA PARA CREAR NUEVO PROCESO (TECLA 'N') ---
        if crear_nuevo_proceso:
            with live.console.capture(): # Capturamos el input para no romper el layout
                clear_screen()
                print("--- Creando Nuevo Proceso en Tiempo de Ejecución ---")
                id = validar_id(lista_id)
                lista_id.append(id)
                num_a, num_b, operador = validar_operacion()
                tme = validar_tme()
            nuevo_proceso = ObjProceso(id, ObjOperacion(num_a, num_b, operador), tme)
            cola_nuevos.append(nuevo_proceso)
            todos_los_procesos.append(nuevo_proceso)
            crear_nuevo_proceso = False
            clear_screen() # Limpiamos la pantalla después de la captura

        # --- 1. EVENTOS QUE CONSUMEN EL TICK ACTUAL (pc) ---
        if proceso_en_ejecucion:
            proceso_en_ejecucion.transcurrido += 1
            proceso_en_ejecucion.restante -= 1
        for proceso in cola_bloqueados:
            proceso.tiempo_bloqueado_restante -= 1
            proceso.tiempo_transcurrido_bloqueado += 1

        # --- 2. TRANSICIONES DE ESTADO ---
        procesos_desbloqueados = []
        for proceso in cola_bloqueados:
            if proceso.tiempo_bloqueado_restante <= 0:
                procesos_desbloqueados.append(proceso)
        for proceso in procesos_desbloqueados:
            cola_bloqueados.remove(proceso)
            proceso.estado = "Listo"
            cola_listos.append(proceso)

        if proceso_en_ejecucion:
            if interrupcion_io:
                proceso_en_ejecucion.tiempo_bloqueado_restante = 8
                proceso_en_ejecucion.tiempo_transcurrido_bloqueado = 0
                proceso_en_ejecucion.estado = "Bloqueado"
                cola_bloqueados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_io = False
            elif interrupcion_error:
                proceso_en_ejecucion.resultado = "Error"
                proceso_en_ejecucion.tiempo_finalizacion = pc + 1
                proceso_en_ejecucion.estado = "Terminado"
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_error = False
            elif proceso_en_ejecucion.restante <= 0:
                op = proceso_en_ejecucion.operacion
                match op.operador:
                    # (cálculo de resultado)
                    case '+': proceso_en_ejecucion.resultado = op.num_a + op.num_b
                    case '-': proceso_en_ejecucion.resultado = op.num_a - op.num_b
                    case '*': proceso_en_ejecucion.resultado = op.num_a * op.num_b
                    case '/': proceso_en_ejecucion.resultado = round(op.num_a / op.num_b, 2)
                    case '^': proceso_en_ejecucion.resultado = pow(op.num_a, op.num_b)
                    case '%': proceso_en_ejecucion.resultado = op.num_a % op.num_b
                proceso_en_ejecucion.tiempo_finalizacion = pc + 1
                proceso_en_ejecucion.estado = "Terminado"
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None

        # --- 3. PLANIFICACIÓN ---
        procesos_en_memoria = len(cola_listos) + len(cola_bloqueados) + (1 if proceso_en_ejecucion else 0)
        if procesos_en_memoria < MAX_PROCESOS_EN_MEMORIA and cola_nuevos:
            proceso_admitido = cola_nuevos.popleft()
            proceso_admitido.tiempo_llegada = pc + 1
            proceso_admitido.estado = "Listo"
            cola_listos.append(proceso_admitido)
        
        if not proceso_en_ejecucion and cola_listos:
            proceso_en_ejecucion = cola_listos.popleft()
            proceso_en_ejecucion.estado = "Ejecución"
            if proceso_en_ejecucion.tiempo_primera_ejecucion is None:
                proceso_en_ejecucion.tiempo_primera_ejecucion = pc + 1

        # --- 4. AVANCE DEL RELOJ ---
        pc += 1

# --- FIN DE LA SIMULACIÓN ---
clear_screen()
console.print("[bold cyan]Simulación Finalizada. Reporte Final de Procesos (BCP):[/bold cyan]\n")
# Mostrar la tabla BCP al finalizar
console.print(tabla_bcp(todos_los_procesos, pc))
input("\nPresiona Enter para salir...")