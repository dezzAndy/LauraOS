# ----------------------------
#           LauraOS
# Este programa es una simulación
# del funcionamiento de un SO

# To do: Hacer una pantalla de presentación

input_valido = False
while input_valido != False:
    # Pedimos la cantidad de procesos a ejecutar
    num_procesos = int(input("Cuantos procesos quieres iniciar?\n>"))
    print(f"Vas a ejecutar {num_procesos} procesos.")

    # Cada lote está compuesto por 4 procesos

    # Definir los lotes en objetos y contarlos.
    if num_procesos != 0:
        num_lotes = num_procesos/4
    else:
        # Repite el ciclo
        input_valido = False
