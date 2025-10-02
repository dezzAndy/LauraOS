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
    tabla.add_column("Transcurrido", style="yellow")
    
    for p in cola_listos:
        tabla.add_row(str(p.id), str(p.tme), str(p.transcurrido))
    
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
    tabla.add_column("Tiempo Restante", style="red")

    for p in cola_bloqueados:
        tabla.add_row(str(p.id), str(p.tiempo_bloqueado_restante))
        
    return Panel(tabla, title="[bold green]d.[/] Cola de Bloqueados")

# e. Muestra la tabla de procesos Terminados
def tabla_terminados(terminados):
    tabla = Table(box=None)
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Operación", style="magenta")
    tabla.add_column("Resultado", style="green")

    for p in terminados:
        op = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        tabla.add_row(str(p.id), op, str(p.resultado))
        
    return Panel(tabla, title="[bold red]e.[/] Procesos Terminados")

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
    
    layout["left_col"].split(
        panel_nuevos(nuevos),
        tabla_listos(listos)
    )

    layout["right_col"].split(
        panel_ejecucion(en_ejecucion),
        Layout(name="bottom_row", ratio=2)
    )
    
    layout["bottom_row"].split_row(
        tabla_bloqueados(bloqueados),
        tabla_terminados(terminados)
    )

    layout["header"].update(Panel(f"Contador Global: {pc}", title="[bold cyan]f.[/] Reloj"))
    layout["footer"].update(Panel(Align.center("[bold]LauraOS v3.0[/bold]", vertical="middle")))

    return layout