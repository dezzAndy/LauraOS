from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from Objetos import ObjProceso

# a. Muestra el número de procesos en la cola de Nuevos 
def panel_nuevos(cola_nuevos):
    num_nuevos = len(cola_nuevos)
    return Panel(f"[bold cyan]{num_nuevos}[/]", title="[bold green]a.[/] Procesos Nuevos")

# b. Muestra la cola de procesos Listos
def tabla_listos(cola_listos):
    tabla = Table(box=None)
    tabla.add_column("ID", style="cyan")
    tabla.add_column("TME", style="magenta")
    # Mostrar Tiempo Restante
    tabla.add_column("T. Restante", style="yellow")
    
    for p in cola_listos:
        tabla.add_row(str(p.id), str(p.tme), str(p.restante))
    
    return Panel(tabla, title="[bold green]b.[/] Cola de Listos")

# c. Muestra el proceso actualmente en Ejecución 
def panel_ejecucion(proceso: ObjProceso):
    if not proceso:
        return Panel("[bold red]Ninguno[/]", title="[bold yellow]c.[/] Proceso en Ejecución")
    
    return Panel(
        f"""[bold]ID:[/bold] \t\t{proceso.id}
[bold]Operación:[/bold] \t{proceso.operacion.num_a} {proceso.operacion.operador} {proceso.operacion.num_b}
[bold]TME:[/bold] \t\t{proceso.tme}
[bold]Transcurrido:[/bold] \t{proceso.transcurrido}
[bold]Restante:[/bold] \t{proceso.restante}""",
        title="[bold yellow]c.[/] Proceso en Ejecución",
        border_style="yellow",
    )

# d. Muestra la cola de procesos Bloqueados
def tabla_bloqueados(cola_bloqueados):
    tabla = Table(box=None)
    tabla.add_column("ID", style="cyan")
    # [MODIFICADO] Req. 5.d.ii: Mostrar Tiempo Transcurrido en Bloqueado
    tabla.add_column("T. Transcurrido", style="red")

    for p in cola_bloqueados:
        tabla.add_row(str(p.id), str(p.tiempo_transcurrido_bloqueado))
        
    return Panel(tabla, title="[bold green]d.[/] Cola de Bloqueados")

# e. Muestra la tabla de procesos Terminados (sin cambios)
def tabla_terminados(terminados):
    tabla = Table(box=None)
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Operación", style="magenta")
    tabla.add_column("Resultado", style="green")

    for p in terminados:
        op = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        tabla.add_row(str(p.id), op, str(p.resultado))
        
    return Panel(tabla, title="[bold red]e.[/] Procesos Terminados")

# [NUEVO] Función para generar la Tabla de Control de Procesos (BCP)
def tabla_bcp(todos_los_procesos, pc):
    tabla = Table(title="Tabla de Control de Procesos (BCP)")
    headers = [
        "ID", "Estado", "Operación", "Resultado", "T. Llegada", "T. Finalización", 
        "T. Retorno", "T. Espera", "T. Servicio", "T. Restante CPU", "T. Respuesta"
    ]
    for header in headers:
        tabla.add_column(header, justify="center")

    for p in sorted(todos_los_procesos, key=lambda x: x.id):
        # Preparación de datos para la tabla
        estado_str = p.estado
        if p.estado == "Bloqueado":
            estado_str = f"Bloqueado ({p.tiempo_bloqueado_restante}s)"
        elif p.estado == "Terminado":
            estado_str = f"Terminado ({'Error' if p.resultado == 'Error' else 'OK'})"

        op_str = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        resultado_str = str(p.resultado) if p.resultado is not None else "N/A"
        
        # Cálculos de tiempo "al momento"
        llegada = str(p.tiempo_llegada) if p.tiempo_llegada is not None else "N/A"
        finalizacion = str(p.tiempo_finalizacion) if p.tiempo_finalizacion is not None else "N/A"
        
        # Tiempo de Servicio (al momento)
        servicio_actual = p.transcurrido
        
        # Tiempo de Retorno (al momento o final)
        if p.tiempo_finalizacion is not None:
            retorno_actual = p.tiempo_finalizacion - p.tiempo_llegada
        elif p.tiempo_llegada is not None:
            retorno_actual = pc - p.tiempo_llegada
        else:
            retorno_actual = "N/A"
        
        # Tiempo de Espera (al momento o final)
        if isinstance(retorno_actual, int):
            espera_actual = retorno_actual - servicio_actual
        else:
            espera_actual = "N/A"

        respuesta = str(p.tiempo_primera_ejecucion - p.tiempo_llegada) if p.tiempo_primera_ejecucion is not None else "N/A"

        tabla.add_row(
            str(p.id), estado_str, op_str, resultado_str, llegada, finalizacion,
            str(retorno_actual), str(espera_actual), str(servicio_actual), str(p.restante), respuesta
        )
    return tabla

# LAYOUT PRINCIPAL 
def make_layout(pc, nuevos, listos, bloqueados, terminados, en_ejecucion):
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
    layout["left_col"].split(panel_nuevos(nuevos), tabla_listos(listos))
    layout["right_col"].split(
        panel_ejecucion(en_ejecucion),
        Layout(name="bottom_row", ratio=2)
    )
    layout["bottom_row"].split_row(tabla_bloqueados(bloqueados), tabla_terminados(terminados))
    layout["header"].update(Panel(f"Contador Global: {pc}", title="[bold cyan]f.[/] Reloj"))
    layout["footer"].update(Panel(Align.center("[bold]LauraOS v4.0[/bold]", vertical="middle")))
    return layout