import time
import keyboard
from collections import deque
from logo import logo
from clear_screen import clear_screen
from validaciones import *
from Objetos import ObjProceso, ObjOperacion
from rich.live import Live
from rich.console import Console
from layout import *

console = Console()

# --- Banderas y funciones de interrupción  ---
interrupcion_io, interrupcion_error, pausa, crear_nuevo_proceso, mostrar_bcp = False, False, False, False, False

# Funciones para gestionar las interrupciones
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
    mostrar_bcp = False
def gestionar_crear_nuevo(e):
    global crear_nuevo_proceso
    if not pausa: crear_nuevo_proceso = True
def gestionar_mostrar_bcp(e):
    global mostrar_bcp, pausa
    if not mostrar_bcp:
        mostrar_bcp = True
        pausa = True

keyboard.on_press_key("e", gestionar_interrupcion_io, suppress=True)
keyboard.on_press_key("w", gestionar_error, suppress=True)
keyboard.on_press_key("p", gestionar_pausa, suppress=True)
keyboard.on_press_key("c", gestionar_continuar, suppress=True)
keyboard.on_press_key("n", gestionar_crear_nuevo, suppress=True)
keyboard.on_press_key("b", gestionar_mostrar_bcp, suppress=True)


# ============================================================================
#                          --- PROGRAMA PRINCIPAL ---
# ============================================================================
logo()
num_procesos = validar_num_procesos()
QUANTUM = validar_quantum()

# --- Colas y listas ---
cola_nuevos, cola_listos, cola_bloqueados = deque(), deque(), deque()
procesos_terminados, lista_id, todos_los_procesos = [], [], []
proceso_en_ejecucion = None

# --- Creación de procesos ---
clear_screen()
print(f"Creando {num_procesos} procesos iniciales...")
for _ in range(num_procesos):
    id = validar_id(lista_id)
    lista_id.append(id)
    num_a, num_b, operador = validar_operacion()
    tme = validar_tme()
    proceso = ObjProceso(id, ObjOperacion(num_a, num_b, operador), tme)
    cola_nuevos.append(proceso)
    todos_los_procesos.append(proceso)

# --- SIMULACIÓN ---
pc = 0
MAX_PROCESOS_EN_MEMORIA = 4

# --- Carga Inicial ---
num_a_admitir = min(len(cola_nuevos), MAX_PROCESOS_EN_MEMORIA)
for _ in range(num_a_admitir):
    p_admitido = cola_nuevos.popleft()
    p_admitido.tiempo_llegada = 0
    p_admitido.estado = "Listo"
    cola_listos.append(p_admitido)
if cola_listos:
    proceso_en_ejecucion = cola_listos.popleft()
    proceso_en_ejecucion.tiempo_primera_ejecucion = 0
    proceso_en_ejecucion.estado = "Ejecución"
    proceso_en_ejecucion.quantum_transcurrido = 0

with Live(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion, QUANTUM),
          refresh_per_second=4, screen=True, vertical_overflow="visible") as live:

    while cola_nuevos or cola_listos or cola_bloqueados or proceso_en_ejecucion:
        
        # --- Pausa y Vista BCP ---
        if pausa:
            if mostrar_bcp:
                live.stop()
                clear_screen()
                console.print(tabla_bcp(todos_los_procesos, pc))
                console.print("\n[bold yellow]Mostrando BCP. Simulación en Pausa. Presiona 'C' para continuar...[/bold yellow]")
                while mostrar_bcp: time.sleep(0.1)
                clear_screen()
                live.start()
            else:
                while pausa: time.sleep(0.1)

        live.update(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion, QUANTUM))
        time.sleep(1)

        # --- Creación de nuevo proceso ---
        if crear_nuevo_proceso:
            # (El código para crear un nuevo proceso que ya tienes va aquí)
            with live.console.capture():
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
            clear_screen()

        # --- 1. EVENTOS QUE CONSUMEN EL TICK ---
        if proceso_en_ejecucion:
            proceso_en_ejecucion.transcurrido += 1
            proceso_en_ejecucion.restante -= 1
            proceso_en_ejecucion.quantum_transcurrido += 1
        for p_bloqueado in cola_bloqueados:
            p_bloqueado.tiempo_bloqueado_restante -= 1
            p_bloqueado.tiempo_transcurrido_bloqueado += 1

        # --- 2. TRANSICIONES DE ESTADO ---
        # Desbloqueo de procesos
        for p_desbloqueado in [p for p in cola_bloqueados if p.tiempo_bloqueado_restante <= 0]:
            cola_bloqueados.remove(p_desbloqueado)
            p_desbloqueado.estado = "Listo"
            cola_listos.append(p_desbloqueado)

        # Revisión del proceso en ejecución
        if proceso_en_ejecucion:
            p = proceso_en_ejecucion
            # Eventos de mayor prioridad: Interrupciones y finalización
            if interrupcion_io:
                p.estado, p.tiempo_bloqueado_restante, p.tiempo_transcurrido_bloqueado = "Bloqueado", 8, 0
                cola_bloqueados.append(p)
                proceso_en_ejecucion = None
                interrupcion_io = False
            elif interrupcion_error:
                p.estado, p.resultado, p.tiempo_finalizacion = "Terminado", "Error", pc + 1
                procesos_terminados.append(p)
                proceso_en_ejecucion = None
                interrupcion_error = False
            elif p.restante <= 0:
                op = p.operacion
                match op.operador:
                    case '+': p.resultado = op.num_a + op.num_b
                    case '-': p.resultado = op.num_a - op.num_b
                    case '*': p.resultado = op.num_a * op.num_b
                    case '/': p.resultado = round(op.num_a / op.num_b, 2)
                    case '^': p.resultado = pow(op.num_a, op.num_b)
                    case '%': p.resultado = op.num_a % op.num_b
                p.estado, p.tiempo_finalizacion = "Terminado", pc + 1
                procesos_terminados.append(p)
                proceso_en_ejecucion = None
            # Evento de Round-Robin: Quantum expirado
            elif p.quantum_transcurrido >= QUANTUM:
                p.estado = "Listo"
                cola_listos.append(p) # Se va al final de la cola de listos
                proceso_en_ejecucion = None

        # --- 3. PLANIFICACIÓN ---
        # Largo Plazo
        procesos_en_memoria = len(cola_listos) + len(cola_bloqueados) + (1 if proceso_en_ejecucion else 0)
        if procesos_en_memoria < MAX_PROCESOS_EN_MEMORIA and cola_nuevos:
            p_admitido = cola_nuevos.popleft()
            p_admitido.tiempo_llegada = pc + 1
            p_admitido.estado = "Listo"
            cola_listos.append(p_admitido)
        
        # Corto Plazo
        if not proceso_en_ejecucion and cola_listos:
            proceso_en_ejecucion = cola_listos.popleft()
            proceso_en_ejecucion.estado = "Ejecución"
            proceso_en_ejecucion.quantum_transcurrido = 0 # Reinicia el contador de quantum
            if proceso_en_ejecucion.tiempo_primera_ejecucion is None:
                proceso_en_ejecucion.tiempo_primera_ejecucion = pc + 1

        # --- AVANCE DEL RELOJ ---
        pc += 1

# --- FIN ---
clear_screen()
console.print("[bold cyan]Simulación Finalizada. Reporte Final de Procesos (BCP):[/bold cyan]\n")
console.print(tabla_bcp(todos_los_procesos, pc))
input("\nPresiona Enter para salir...")