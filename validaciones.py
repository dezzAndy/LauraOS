import random
from clear_screen import clear_screen
# ================================================
# Válida el numero de procesos:
def validar_num_procesos():
    while True:
        try:
            num_procesos = int(input("Cuantos procesos quieres iniciar?\n> "))
            if num_procesos < 1:
                clear_screen()
                print("Error: Ingresa un número mayor a 0\n")
                continue
            return num_procesos
        except ValueError:
            clear_screen()
            print("Error: Ingresa un número válido\n")

# ================================================
# Válida operación del proceso
# Solicita dos números y genera un operador aleatorio
def validar_operacion():
    operadores_validos = ["+", "-", "*", "/", "%", "^"]
    while True:
        try:
            num_a       = random.randint(0, 100)
            num_b       = random.randint(0, 100)

            # Selección aleatoria de operador dependiendo de los casos válidos
            if num_b == 0:
                operador = random.choice(["+", "-", "*", "^"])
            else:
                operador = random.choice(operadores_validos)
                
            print(f"    Operador (+, -, *, /, %, ^): {operador}")
            
            return num_a, num_b, operador
        
        except ValueError:
            print("\nError: Ingresa números válidos\n")
            
# ================================================
# Válida ID
# Genera un ID secuencial que no se repita
def validar_id(lista_id):
    while True:
        try:
            if len(lista_id) >= 1:
                id = lista_id[-1] + 1
                if id not in lista_id:
                    return id
                else:
                    print("\nID no válido, no se puede repetir\n")
            else:
                id = 1
                if id not in lista_id:
                    return id
                else:
                    print("\nID no válido, no se puede repetir\n")
                
        except ValueError:
            print("\nError: Ingresa números válidos\n")
            
# ================================================
# Valida TME
# Genera un número aleatorio entre 6 y 20
def validar_tme():
    while True:
        try:
            tme = random.randint(6, 20)
            return tme
        except ValueError:
            print("\nError: Ingresa un número válido\n")