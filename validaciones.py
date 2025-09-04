# ================================================
# Válida el numero de procesos:
def validar_num_procesos():
    while True:
        try:
            num_procesos = int(input("Cuantos procesos quieres iniciar?\n>"))
            return num_procesos
        except ValueError:
            print("\nError: Ingresa un número válido\n")

# ================================================
# Válida operación del roceso
def validar_operacion():
    operadores_validos = ["+", "-", "*", "/", "%", "^"]
    while True:
        try:
            num_a       = int(input("    Numero A:                  > "))
            operador    =     input("    Operador (+, -, *, /, %, ^): ")
            num_b       = int(input("    Numero B:                  > "))
            if operador in operadores_validos:
                return num_a, num_b, operador
            else:
                print("\nOperación no válida, solo puedes ingresar los operadores: +, -, *, /, %, ^\n")
        except ValueError:
            print("\nError: Ingresa números válidos\n")
            
# ================================================
# Válida ID
def validar_id(lista_id):
    while True:
        try:
            id = int(input("ID del proceso (No se puede repetir): \n> "))
            if id not in lista_id:
                return id
            else:
                print("\nID no válido, no se puede repetir\n")
        except ValueError:
            print("\nError: Ingresa números válidos\n")
            
# ================================================
# Valida TME
def validar_tme():
    while True:
        try:
            tme = int(input("Tiempo Máximo de Ejecución (TME): "))
            return tme
        except ValueError:
            print("\nError: Ingresa un número válido\n")