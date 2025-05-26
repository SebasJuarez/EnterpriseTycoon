from jugador import Jugador, IAJugador
from mundo import MundoEmpresarial

def main():
    # jugador_humano = Jugador("Tú", 5000)
    ia_0 = IAJugador("NeuroCorp", 5000, "pasiva")
    ia_1 = IAJugador("CorpX", 5000, "acaparadora")
    ia_2 = IAJugador("MegaTech", 5000, "agresiva")
    juego = MundoEmpresarial([ia_0, ia_1, ia_2])
    for _ in range(5):
        juego.ejecutar_ronda()
        print("\n📊 Estado actual:")
        for j in juego.jugadores:
            print(j)

if __name__ == "__main__":
    main()
