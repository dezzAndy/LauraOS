import random
# ================================================
# Válida el numero de procesos:
def validar_num_procesos():
    while True:
        try:
            num_procesos = int(input("Cuantos procesos quieres iniciar?\n> "))
            return num_procesos
        except ValueError:
            print("\nError: Ingresa un número válido\n")

# ================================================
# Válida operación del proceso
# Solicita dos números y genera un operador aleatorio
def validar_operacion():
    operadores_validos = ["+", "-", "*", "/", "%", "^"]
    while True:
        try:
            num_a       = int(input("    Numero A:                  > "))
            num_b       = int(input("    Numero B:                  > "))
            
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