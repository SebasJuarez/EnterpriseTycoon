class Empresa:
    def __init__(self, nombre, tipo, valor, nivel, ventaja=None, propietario=None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.nivel = nivel
        self.ventaja = ventaja
        self.propietario = propietario

    def esta_disponible(self):
        return self.propietario is None

    def __str__(self):
        desc = f"{self.nombre} ({self.tipo}) - Valor: ${self.valor}"
        if self.ventaja:
            desc += f" | Ventaja: {self.ventaja}"
        return desc
