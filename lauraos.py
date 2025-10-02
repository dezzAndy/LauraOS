import math
import time
import keyboard
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

# --- Funciones para manejar las interrupciones (sin cambios) ---
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
    global pausa
    pausa = False

# --- Asignación de teclas ---
keyboard.on_press_key("e", gestionar_interrupcion_io, suppress=True)
keyboard.on_press_key("w", gestionar_error, suppress=True)
keyboard.on_press_key("p", gestionar_pausa, suppress=True)
keyboard.on_press_key("c", gestionar_continuar, suppress=True)


# --- Reporte Final (Punto 11) ---
def mostrar_reporte_final(procesos_terminados):
    clear_screen()
    console.print("[bold cyan]Simulación Finalizada. Reporte de Procesos:[/bold cyan]\n")
    
    tabla_reporte = Table(title="Tiempos de Procesos")
    columnas = ["ID", "Estado Final", "T. Llegada", "T. Finalización", "T. Retorno", "T. Respuesta", "T. Espera", "T. Servicio"]
    for col in columnas:
        tabla_reporte.add_column(col, justify="center")

    for p in sorted(procesos_terminados, key=lambda x: x.id):
        # Cálculos finales
        p.tiempo_retorno = p.tiempo_finalizacion - p.tiempo_llegada
        p.tiempo_servicio = p.transcurrido
        p.tiempo_espera = p.tiempo_retorno - p.tiempo_servicio
        if p.tiempo_primera_ejecucion is not None:
            p.tiempo_respuesta = p.tiempo_primera_ejecucion - p.tiempo_llegada
        else: # El proceso nunca se ejecutó (caso raro)
            p.tiempo_respuesta = -1
        
        estado_final = "Error" if p.resultado == "Error" else "OK"
        
        tabla_reporte.add_row(
            str(p.id),
            estado_final,
            str(p.tiempo_llegada),
            str(p.tiempo_finalizacion),
            str(p.tiempo_retorno),
            str(p.tiempo_respuesta),
            str(p.tiempo_espera),
            str(p.tiempo_servicio)
        )
    console.print(tabla_reporte)

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

# --- Creación de procesos iniciales ---
clear_screen()
print(f"Creando {num_procesos} procesos...")
for i in range(num_procesos):
    id = validar_id(lista_id)
    lista_id.append(id)
    
    # Operación y TME aleatorios (Punto 6)
    num_a = random.randint(0, 100)
    num_b = random.randint(0, 100)
    if num_b == 0:
        operador = random.choice(["+", "-", "*", "^"])
    else:
        operador = random.choice(["+", "-", "*", "/", "%", "^"])
    tme = random.randint(6, 20)

    operacion = ObjOperacion(num_a, num_b, operador)
    proceso = ObjProceso(id, operacion, tme)
    cola_nuevos.append(proceso)

# --- SIMULACIÓN PRINCIPAL ---
pc = 0 # Reloj Global
MAX_PROCESOS_EN_MEMORIA = 4

with Live(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion), 
          refresh_per_second=4, screen=True) as live:

    # El bucle principal se ejecuta mientras haya procesos en cualquier estado activo
    while cola_nuevos or cola_listos or cola_bloqueados or proceso_en_ejecucion:
        
        # --- Lógica de Pausa y Continuar ---
        while pausa:
            time.sleep(0.1)

        # --- 1. GESTIONAR COLA DE BLOQUEADOS ---
        # Se usa una copia para poder modificar la cola original mientras se itera
        for proceso in list(cola_bloqueados):
            proceso.tiempo_bloqueado_restante -= 1
            if proceso.tiempo_bloqueado_restante <= 0:
                cola_bloqueados.remove(proceso)
                cola_listos.append(proceso)

        # --- 2. GESTIONAR PROCESO EN EJECUCIÓN ---
        if proceso_en_ejecucion:
            # INTERRUPCIÓN POR I/O (Tecla E)
            if interrupcion_io:
                proceso_en_ejecucion.tiempo_bloqueado_restante = 8 # Pasa a bloqueado por 8 ticks
                cola_bloqueados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_io = False
            # INTERRUPCIÓN POR ERROR (Tecla W)
            elif interrupcion_error:
                proceso_en_ejecucion.resultado = "Error"
                proceso_en_ejecucion.tiempo_finalizacion = pc
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_error = False
            # EJECUCIÓN NORMAL
            else:
                proceso_en_ejecucion.transcurrido += 1
                proceso_en_ejecucion.restante -= 1
                # Si el proceso termina su TME
                if proceso_en_ejecucion.restante <= 0:
                    op = proceso_en_ejecucion.operacion
                    match op.operador:
                        case '+': proceso_en_ejecucion.resultado = op.num_a + op.num_b
                        case '-': proceso_en_ejecucion.resultado = op.num_a - op.num_b
                        case '*': proceso_en_ejecucion.resultado = op.num_a * op.num_b
                        case '/': proceso_en_ejecucion.resultado = round(op.num_a / op.num_b, 2)
                        case '^': proceso_en_ejecucion.resultado = pow(op.num_a, op.num_b)
                        case '%': proceso_en_ejecucion.resultado = op.num_a % op.num_b
                    proceso_en_ejecucion.tiempo_finalizacion = pc
                    procesos_terminados.append(proceso_en_ejecucion)
                    proceso_en_ejecucion = None
        
        # --- 3. GESTIONAR COLA DE LISTOS (Planificador a Corto Plazo - FCFS) ---
        if not proceso_en_ejecucion and cola_listos:
            proceso_en_ejecucion = cola_listos.popleft()
            # Si es la primera vez que se ejecuta, registramos el tiempo de respuesta
            if proceso_en_ejecucion.tiempo_primera_ejecucion is None:
                proceso_en_ejecucion.tiempo_primera_ejecucion = pc

        # --- 4. GESTIONAR COLA DE NUEVOS (Planificador a Largo Plazo) ---
        procesos_en_memoria = len(cola_listos) + len(cola_bloqueados) + (1 if proceso_en_ejecucion else 0)
        if procesos_en_memoria < MAX_PROCESOS_EN_MEMORIA and cola_nuevos:
            proceso_admitido = cola_nuevos.popleft()
            proceso_admitido.tiempo_llegada = pc # El tiempo de llegada es cuando entra a Listos
            cola_listos.append(proceso_admitido)

        # --- Actualización y Siguiente Tick ---
        live.update(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion))
        time.sleep(1)
        pc += 1

# --- FIN DE LA SIMULACIÓN ---
mostrar_reporte_final(procesos_terminados)
input("\nPresiona Enter para salir...")