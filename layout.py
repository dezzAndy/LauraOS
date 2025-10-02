from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from Objetos import ObjProceso

def tabla_lote_actual(lote, numero_lote, lotes_pendientes):
    # Calculamos los lotes restantes
    lotes_restantes = max(0, lotes_pendientes - numero_lote)
    tabla = Table(title="Procesos en Espera", caption=f"(Lote #{numero_lote})\nLotes pendientes: {lotes_restantes}")
    
    tabla.add_column("ID", style="cyan")
    tabla.add_column("TME", justify="center", style="magenta")
    tabla.add_column("Transcurrido", justify="center", style="yellow")

    for proceso in lote:
        # Si un proceso fue interrumpido (E) y regresó a la cola, mostrará su tiempo.
        # Si es nuevo, mostrará 0.
        tabla.add_row(
            str(proceso.id), 
            str(proceso.tme), 
            str(proceso.transcurrido), 
            end_section=True
        )
    return Panel(tabla, border_style="green", title="[bold green]a.[/] Procesos en Espera")


def panel_proceso(proceso: ObjProceso):
    return Panel(
        f"""
[bold]ID:[/bold] \t\t{proceso.id}
[bold]Operación:[/bold] \t{proceso.operacion.num_a} {proceso.operacion.operador} {proceso.operacion.num_b}
[bold]TME:[/bold] \t\t{proceso.tme}
[bold]Transcurrido:[/bold] \t{proceso.transcurrido}
[bold]Restante:[/bold] \t{proceso.restante}
""",
        
        title="[bold yellow]c.[/] Proceso en Ejecución",
        border_style="yellow",
    )


def tabla_terminados(lista):
    tabla = Table()
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Operación", style="magenta")
    tabla.add_column("Resultado", style="green")
    for p in lista:
        op = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        tabla.add_row(str(p.id), op, str(p.resultado))
    
    return Panel(tabla, border_style="red", title="[bold red]d.[/] Trabajos Terminados")


# ======================
#  LAYOUT PRINCIPAL
# ======================
def make_layout(global_time, lote_actual, num_lote, proceso, terminados, lotes_pendientes: int):
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="lote"),
        Layout(name="proceso"),
        Layout(name="terminados"),
    )

    # Actualizamos los paneles con la información correspondiente
    layout["header"].update(Panel(f"Contador Global: {global_time}", title="[bold cyan]Reloj[/]"))
    layout["lote"].update(tabla_lote_actual(lote_actual, num_lote, lotes_pendientes))
    layout["proceso"].update(panel_proceso(proceso))
    layout["terminados"].update(tabla_terminados(terminados))
    layout["footer"].update(Panel(Align.center("[bold]LauraOS[/bold]", vertical="middle")))

    return layout