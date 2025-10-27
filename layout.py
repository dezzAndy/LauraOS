from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from Objetos import ObjProceso

# Muestra el número de procesos nuevos y el Quantum
def panel_nuevos_y_quantum(cola_nuevos, quantum):
    num_nuevos = len(cola_nuevos)
    return Panel(f"[bold cyan]Procesos Nuevos: {num_nuevos}\n[bold magenta]Quantum: {quantum}", 
                 title="[bold green]a, b.[/] Sistema")

# Muestra la cola de listos
def tabla_listos(cola_listos):
    tabla = Table(box=None, title="[bold green]c.[/] Cola de Listos")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("TME", style="magenta")
    # [MODIFICADO] Req. 6.c.iii: Mostrar Tiempo Transcurrido
    tabla.add_column("T. Transcurrido", style="yellow")
    
    for p in cola_listos:
        tabla.add_row(str(p.id), str(p.tme), str(p.transcurrido))
    
    return Panel(tabla)

# Muestra el proceso en ejecución
def panel_ejecucion(proceso: ObjProceso, quantum):
    if not proceso:
        return Panel("[bold red]Ninguno[/]", title="[bold yellow]d.[/] Proceso en Ejecución")
    
    # [MODIFICADO] Req. 6.d.iv: Mostrar tiempo transcurrido del quantum
    return Panel(
        f"""[bold]ID:[/bold] \t\t{proceso.id}
[bold]Operación:[/bold] \t{proceso.operacion.num_a} {proceso.operacion.operador} {proceso.operacion.num_b}
[bold]TME:[/bold] \t\t{proceso.tme}
[bold]T. Transcurrido:[/bold] {proceso.transcurrido}
[bold]T. Restante:[/bold] \t{proceso.restante}
[bold]Quantum Restante:[/bold] {quantum - proceso.quantum_transcurrido}""",
        title="[bold yellow]d.[/] Proceso en Ejecución",
        border_style="yellow",
    )

# Muestra la cola de bloqueados (sin cambios)
def tabla_bloqueados(cola_bloqueados):
    tabla = Table(box=None, title="[bold green]e.[/] Cola de Bloqueados")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("T. Transcurrido", style="red")
    for p in cola_bloqueados:
        tabla.add_row(str(p.id), str(p.tiempo_transcurrido_bloqueado))
    return Panel(tabla)

# Muestra los terminados (sin cambios)
def tabla_terminados(terminados):
    tabla = Table(box=None, title="[bold red]f.[/] Procesos Terminados")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Operación", style="magenta")
    tabla.add_column("Resultado", style="green")
    for p in terminados:
        op = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        tabla.add_row(str(p.id), op, str(p.resultado))
    return Panel(tabla)

# Tabla BCP (sin cambios)
def tabla_bcp(todos_los_procesos, pc):
    # (El código de la función tabla_bcp que ya tienes va aquí, no necesita cambios)
    tabla = Table(title="Tabla de Control de Procesos (BCP)")
    headers = ["ID", "Estado", "Operación", "Resultado", "T. Llegada", "T. Finalización", "T. Retorno", "T. Espera", "T. Servicio", "T. Restante CPU", "T. Respuesta"]
    for header in headers:
        tabla.add_column(header, justify="center")
    for p in sorted(todos_los_procesos, key=lambda x: x.id):
        estado_str = p.estado
        if p.estado == "Bloqueado": estado_str = f"Bloqueado ({p.tiempo_bloqueado_restante}s)"
        elif p.estado == "Terminado": estado_str = f"Terminado ({'Error' if p.resultado == 'Error' else 'OK'})"
        op_str = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        resultado_str = str(p.resultado) if p.resultado is not None else "N/A"
        llegada = str(p.tiempo_llegada) if p.tiempo_llegada is not None else "N/A"
        finalizacion = str(p.tiempo_finalizacion) if p.tiempo_finalizacion is not None else "N/A"
        servicio_actual = p.transcurrido
        if p.estado == "Terminado":
            retorno_actual = p.tiempo_finalizacion - p.tiempo_llegada
            espera_actual = retorno_actual - servicio_actual
        else:
            retorno_actual = "N/A"
            if p.tiempo_llegada is not None:
                tiempo_total_en_sistema = pc - p.tiempo_llegada
                espera_actual = tiempo_total_en_sistema - servicio_actual
            else:
                espera_actual = "N/A"
        respuesta = str(p.tiempo_primera_ejecucion - p.tiempo_llegada) if p.tiempo_primera_ejecucion is not None else "N/A"
        tabla.add_row(str(p.id), estado_str, op_str, resultado_str, llegada, finalizacion, str(retorno_actual), str(espera_actual), str(servicio_actual), str(p.restante), respuesta)
    return tabla

# LAYOUT PRINCIPAL
def make_layout(pc, nuevos, listos, bloqueados, terminados, en_ejecucion, quantum):
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="left_col", ratio=1),
        Layout(name="right_col", ratio=2),
    )
    layout["left_col"].split(panel_nuevos_y_quantum(nuevos, quantum), tabla_listos(listos))
    layout["right_col"].split(
        panel_ejecucion(en_ejecucion, quantum),
        Layout(name="bottom_row", ratio=2)
    )
    layout["bottom_row"].split_row(tabla_bloqueados(bloqueados), tabla_terminados(terminados))
    layout["header"].update(Panel(f"Contador Global: {pc}", title="[bold cyan]g.[/] Reloj"))
    layout["footer"].update(Panel(Align.center("[bold]LauraOS v5.0 - Round Robin[/bold]", vertical="middle")))
    return layout