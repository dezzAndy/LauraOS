# Objeto Proceso
class ObjProceso():
    def __init__(self, id, operacion, tme):
        # Datos base del proceso
        self.id = id
        self.operacion = operacion
        self.tme = tme
        self.resultado = None

        # Tiempos de ejecución
        self.transcurrido = 0
        self.restante = tme
        
        # Estado y tiempos para métricas (Punto 9)
        self.estado = "Nuevo"
        self.tiempo_llegada = None
        self.tiempo_finalizacion = None
        self.tiempo_retorno = 0
        self.tiempo_respuesta = None
        self.tiempo_espera = 0
        self.tiempo_servicio = 0
        
        # Atributos para el estado Bloqueado
        self.tiempo_bloqueado_restante = 0
        self.tiempo_primera_ejecucion = None


# Objeto Operación (sin cambios)
class ObjOperacion():
    def __init__(self, num_a, num_b, operador):
        self.num_a = num_a
        self.num_b = num_b
        self.operador = operador