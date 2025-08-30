class Empresa:
    def __init__(self, nombre, tipo, valor, nivel, ventaja=None, propietario=None, efecto=None):
        self.nombre = nombre
        self.tipo = tipo 
        self.valor = valor
        self.nivel = nivel
        self.ventaja = ventaja 
        self.propietario = propietario
        self.efecto = efecto 

    def esta_disponible(self):
        return self.propietario is None

    def aplicar_efecto(self, jugador, mundo):
        if not self.efecto:
            return

        if self.efecto == "bono_liquidez":
            jugador.dinero += 1000
            print(f"{jugador.nombre} recibe $1000 por efecto de {self.nombre}.")

        elif self.efecto == "pierde_turno":
            jugador.saltar_turno = True
            print(f"{jugador.nombre} perderá el próximo turno por efecto de {self.nombre}.")

        elif self.efecto == "castigo_dinero_2r":
            mundo.agendar_castigo(jugador, 2, 500)
            print(f"{jugador.nombre} recibirá una multa de $500 en 2 rondas por {self.nombre}.")

        elif self.efecto == "bono_por_ventas":
            jugador.bono_ventas = True
            print(f"{jugador.nombre} obtiene un bono en futuras ventas gracias a {self.nombre}.")

    def __str__(self):
        desc = f"{self.nombre} ({self.tipo}) - Valor: ${self.valor}"
        if self.ventaja:
            desc += f" | Ventaja: {self.ventaja}"
        return desc
