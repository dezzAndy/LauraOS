# Objeto Proceso
class ObjProceso():
    def __init__(self, id, nombre, operación, tme):
        self.id         = id
        self.nombre     = nombre
        self.operacion  = operación
        self.tme        = tme
        self.transcurrido = 0
        self.restante     = tme
        self.resultado    = None

# Objeto Operación
class ObjOperacion():
    def __init__(self, num_a, num_b, operador):
        self.num_a      = num_a
        self.num_b      = num_b
        self.operador   = operador