# ----------------------------
#           LauraOS
# Este programa es una simulación
# del funcionamiento de un SO

# To do: Hacer una pantalla de presentación

import os
import math
from logo import logo

logo()

input_valido = False
while input_valido == False:
    # Pedimos la cantidad de procesos a ejecutar
    os.system('cls')
    num_procesos = int(input("Cuantos procesos quieres iniciar?\n>"))
    print(f"Vas a ejecutar {num_procesos} procesos.")

    # Cada lote está compuesto por 4 procesos

    # Definir los lotes en objetos y contarlos.
    if num_procesos > 0:
        num_lotes = math.ceil(num_procesos/4)
        if num_lotes > 1:
            print(f"Los procesos se han separado en {num_lotes} lotes.")
        else:
            print(f"Se ejecutarán en {num_lotes} lote.")
        input_valido = True
    else:
        # Repite el ciclo
        print("Entrada no válida.")
        input_valido = False

# Definición de la clase Lote
