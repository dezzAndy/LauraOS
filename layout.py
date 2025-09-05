from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from Objetos import ObjProceso

def tabla_lote_actual(lote, numero_lote, lotes_pendientes):
    tabla = Table(title=f"Lote actual #{numero_lote}\nLotes pendientes: {lotes_pendientes - numero_lote}")
    tabla.add_column("Nombre", style="cyan")
    tabla.add_column("TME", justify="center", style="magenta")
    for proceso in lote:
        tabla.add_row(proceso.nombre, str(proceso.tme))
    return Panel(tabla, border_style="green")


def panel_proceso(proceso: ObjProceso):
    return Panel(
        f"""
[bold]ID:[/bold] \t\t{proceso.id}
[bold]Nombre:[/bold] \t{proceso.nombre}
[bold]Operación:[/bold] \t{proceso.operacion.num_a} {proceso.operacion.operador} {proceso.operacion.num_b}
[bold]TME:[/bold] \t\t{proceso.tme}
[bold]Transcurrido:[/bold] \t{proceso.transcurrido}
[bold]Restante:[/bold] \t{proceso.restante}
""",
        title="Proceso en ejecución",
        border_style="yellow",
    )


def tabla_terminados(lista):
    tabla = Table(title="Procesos Terminados")
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Operación", style="magenta")
    tabla.add_column("Resultado", style="green")
    for p in lista:
        op = f"{p.operacion.num_a} {p.operacion.operador} {p.operacion.num_b}"
        tabla.add_row(str(p.id), op, str(p.resultado))
    return Panel(tabla, border_style="red")


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

    layout["header"].update(Panel(f"Contador Global: {global_time}", title="Reloj"))
    layout["lote"].update(tabla_lote_actual(lote_actual, num_lote, lotes_pendientes))
    layout["proceso"].update(panel_proceso(proceso))
    layout["terminados"].update(tabla_terminados(terminados))
    layout["footer"].update(Panel(Align.center("[bold]LauraOS[/bold]", vertical="middle")))

    return layout