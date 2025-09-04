from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align

def make_layout():
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="lotes"),
        Layout(name="ejecucion"),
        Layout(name="terminados"),
    )

    return layout


def render_layout(global_time, lotes_pendientes, lote_actual, proceso, terminados):
    layout = make_layout()

    # Header: contador global
    layout["header"].update(Panel(f"Contador Global: {global_time}", title="Reloj"))

    # Lote Actual
    layout["lotes"].update(
        Panel(f"{procesos_lote}", title="Lote Actual", border_style="yellow")
    )

    # Lote en ejecución
    tabla_lote = Table(title="Lote en Ejecución")
    tabla_lote.add_column("Nombre")
    tabla_lote.add_column("TME")  # Tiempo Máximo Estimado
    for p in lote_actual:
        tabla_lote.add_row(p["nombre"], str(p["tme"]))
    layout["ejecucion"].update(tabla_lote)

    # Proceso en ejecución
    proceso_panel = Panel(
        f"""
[bold]Nombre:[/bold] \t{proceso['nombre']}
[bold]Operación:[/bold] \t{proceso['operacion']}
[bold]TME:[/bold] \t\t{proceso['tme']}
[bold]Programa #[/bold] \t{proceso['id']}
[bold]Transcurrido:[/bold] \t{proceso['transcurrido']}
[bold]Restante:[/bold] \t{proceso['restante']}
""",
        title="Proceso en Ejecución",
        border_style="green",
    )
    layout["ejecucion"].update(proceso_panel)

    # Procesos terminados
    tabla_terminados = Table(title="Procesos Terminados")
    tabla_terminados.add_column("ID")
    tabla_terminados.add_column("Operación")
    tabla_terminados.add_column("Resultado")
    for t in terminados:
        tabla_terminados.add_row(str(t["id"]), t["operacion"], str(t["resultado"]))
    layout["terminados"].update(tabla_terminados)

    # Footer
    layout["footer"].update(Align.center("[bold]LauraOS[/bold]", vertical="middle"))

    return layout