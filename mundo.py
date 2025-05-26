import random
from empresa import Empresa

class MundoEmpresarial:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.empresas_disponibles = []
        self.ronda = 1

        # Catálogo completo
        self.catalogo_empresas = [
            Empresa("Google", "tecnologia", 3000, 1, "Dominio en publicidad"),
            Empresa("Pfizer", "salud", 2800, 1, "Acceso a patentes exclusivas"),
            Empresa("Netflix", "medios", 2500, 1, "Popularidad global"),
            Empresa("Goldman Sachs", "finanzas", 2700, 1, "Red de inversión privilegiada"),
            Empresa("Meta", "tecnologia", 3200, 2, "Integración de plataformas"),
            Empresa("Roche", "salud", 2900, 2, "Dominio en biotecnología"),
            Empresa("SpaceX", "tecnologia", 3500, 2, "Acceso a tecnología espacial"),
            Empresa("Twitter", "medios", 1500, 1, None),
            Empresa("BlackRock", "finanzas", 3800, 3, "Manipulación de mercado"),
            Empresa("Epic Games", "entretenimiento", 2200, 1, "Monetización agresiva"),
            Empresa("Shell", "energia", 3000, 2, "Acceso global de infraestructura"),
            Empresa("Tesla", "tecnologia", 3300, 2, "Innovación disruptiva"),
            Empresa("WeWork", "inmobiliario", 1000, 1, "Liquidez inmediata (pierde turno)"),
            Empresa("Theranos", "salud", 800, 1, "Pierde $500 tras 2 rondas"),
            Empresa("ByteDance", "tecnologia", 2800, 2, "Dominio en redes sociales"),
            Empresa("Reddit", "medios", 1800, 1, None),
            Empresa("OpenAI", "tecnologia", 3600, 3, "Ventaja en algoritmos"),
        ]

        # Solo las empresas que aún no han sido ofrecidas
        self.catalogo_disponible = self.catalogo_empresas.copy()

    def generar_empresas(self):
        random.shuffle(self.catalogo_disponible)
        nuevas = []

        while self.catalogo_disponible and len(nuevas) < 3:
            empresa = self.catalogo_disponible.pop(0)
            if empresa.esta_disponible():
                nuevas.append(empresa)

        self.empresas_disponibles.extend(nuevas)

    def ejecutar_ronda(self):
        print(f"\n--- Ronda {self.ronda} ---")
        self.generar_empresas()
        for jugador in self.jugadores:
            jugador.tomar_turno(self.empresas_disponibles, self.jugadores)

        # Quitar empresas que fueron compradas de la lista pública
        self.empresas_disponibles = [e for e in self.empresas_disponibles if e.esta_disponible()]
        self.ronda += 1
