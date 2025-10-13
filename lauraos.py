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

# --- Banderas y funciones de interrupción (sin cambios) ---
interrupcion_io = False
interrupcion_error = False
pausa = False

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

keyboard.on_press_key("e", gestionar_interrupcion_io, suppress=True)
keyboard.on_press_key("w", gestionar_error, suppress=True)
keyboard.on_press_key("p", gestionar_pausa, suppress=True)
keyboard.on_press_key("c", gestionar_continuar, suppress=True)

# --- Reporte Final (Ajuste en cálculo de Tiempo de Espera) ---
def mostrar_reporte_final(procesos_terminados):
    clear_screen()
    console.print("[bold cyan]Simulación Finalizada. Reporte de Procesos:[/bold cyan]\n")
    tabla_reporte = Table(title="Tiempos de Procesos")
    columnas = ["ID", "Estado Final", "T. Llegada", "T. Finalización", "T. Retorno", "T. Respuesta", "T. Espera", "T. Servicio"]
    for col in columnas:
        tabla_reporte.add_column(col, justify="center")

    for p in sorted(procesos_terminados, key=lambda x: x.id):
        p.tiempo_retorno = p.tiempo_finalizacion - p.tiempo_llegada
        p.tiempo_servicio = p.transcurrido
        
        # [CORREGIDO] Aseguramos que el tiempo de espera no sea negativo.
        # Esta es la definición correcta: Retorno - Servicio.
        p.tiempo_espera = p.tiempo_retorno - p.tiempo_servicio
        
        if p.tiempo_primera_ejecucion is not None:
            p.tiempo_respuesta = p.tiempo_primera_ejecucion - p.tiempo_llegada
        else:
            p.tiempo_respuesta = -1
        
        estado_final = "Error" if p.resultado == "Error" else "OK"
        tabla_reporte.add_row(
            str(p.id), estado_final, str(p.tiempo_llegada), str(p.tiempo_finalizacion),
            str(p.tiempo_retorno), str(p.tiempo_respuesta), str(p.tiempo_espera), str(p.tiempo_servicio)
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

# --- Creación de procesos ---
clear_screen()
print(f"Creando {num_procesos} procesos...")
# (Este bucle usa tus funciones de validaciones que ya funcionan correctamente)
for i in range(num_procesos):
    id = validar_id(lista_id)
    lista_id.append(id)
    num_a, num_b, operador = validar_operacion()
    tme = validar_tme()
    operacion = ObjOperacion(num_a, num_b, operador)
    proceso = ObjProceso(id, operacion, tme)
    cola_nuevos.append(proceso)

# --- SIMULACIÓN PRINCIPAL ---
pc = 0
MAX_PROCESOS_EN_MEMORIA = 4

# --- CARGA INICIAL ANTES DE QUE EL RELOJ COMIENCE ---
num_a_admitir = min(len(cola_nuevos), MAX_PROCESOS_EN_MEMORIA)
for _ in range(num_a_admitir):
    proceso_admitido = cola_nuevos.popleft()
    proceso_admitido.tiempo_llegada = 0
    cola_listos.append(proceso_admitido)
if cola_listos:
    proceso_en_ejecucion = cola_listos.popleft()
    proceso_en_ejecucion.tiempo_primera_ejecucion = 0

with Live(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion), 
          refresh_per_second=4, screen=True, vertical_overflow="visible") as live:

    while cola_nuevos or cola_listos or cola_bloqueados or proceso_en_ejecucion:
        
        live.update(make_layout(pc, cola_nuevos, cola_listos, cola_bloqueados, procesos_terminados, proceso_en_ejecucion))
        time.sleep(1)

        while pausa:
            time.sleep(0.1)

        # 1. EVENTOS QUE CONSUMEN EL TICK ACTUAL (pc)
        # -----------------------------------------------------------------
        if proceso_en_ejecucion:
            proceso_en_ejecucion.transcurrido += 1
            proceso_en_ejecucion.restante -= 1

        for proceso in cola_bloqueados:
            proceso.tiempo_bloqueado_restante -= 1

        # 2. TRANSICIONES DE ESTADO (Consecuencias de los eventos)
        # -----------------------------------------------------------------
        # Se revisa la cola de bloqueados PRIMERO
        procesos_desbloqueados = []
        for proceso in cola_bloqueados:
            if proceso.tiempo_bloqueado_restante <= 0:
                procesos_desbloqueados.append(proceso)
        for proceso in procesos_desbloqueados:
            cola_bloqueados.remove(proceso)
            cola_listos.append(proceso)

        # Se revisa el proceso en ejecución
        if proceso_en_ejecucion:
            # Interrupción por I/O (E)
            if interrupcion_io:
                proceso_en_ejecucion.tiempo_bloqueado_restante = 8
                cola_bloqueados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_io = False
            # Interrupción por Error (W)
            elif interrupcion_error:
                proceso_en_ejecucion.resultado = "Error"
                proceso_en_ejecucion.tiempo_finalizacion = pc + 1
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                interrupcion_error = False
            # El proceso termina normalmente
            elif proceso_en_ejecucion.restante <= 0:
                op = proceso_en_ejecucion.operacion
                match op.operador:
                    case '+': proceso_en_ejecucion.resultado = op.num_a + op.num_b
                    case '-': proceso_en_ejecucion.resultado = op.num_a - op.num_b
                    case '*': proceso_en_ejecucion.resultado = op.num_a * op.num_b
                    case '/': proceso_en_ejecucion.resultado = round(op.num_a / op.num_b, 2)
                    case '^': proceso_en_ejecucion.resultado = pow(op.num_a, op.num_b)
                    case '%': proceso_en_ejecucion.resultado = op.num_a % op.num_b
                proceso_en_ejecucion.tiempo_finalizacion = pc + 1
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None

        # 3. PLANIFICACIÓN (Decisiones para el siguiente tick)
        # -----------------------------------------------------------------
        # Planificador a Largo Plazo
        procesos_en_memoria = len(cola_listos) + len(cola_bloqueados) + (1 if proceso_en_ejecucion else 0)
        if procesos_en_memoria < MAX_PROCESOS_EN_MEMORIA and cola_nuevos:
            proceso_admitido = cola_nuevos.popleft()
            proceso_admitido.tiempo_llegada = pc + 1
            cola_listos.append(proceso_admitido)
        
        # Planificador a Corto Plazo
        if not proceso_en_ejecucion and cola_listos:
            proceso_en_ejecucion = cola_listos.popleft()
            if proceso_en_ejecucion.tiempo_primera_ejecucion is None:
                proceso_en_ejecucion.tiempo_primera_ejecucion = pc + 1

        # 4. AVANCE DEL RELOJ
        # -----------------------------------------------------------------
        pc += 1

# --- FIN DE LA SIMULACIÓN ---
mostrar_reporte_final(procesos_terminados)
input("\nPresiona Enter para salir...")