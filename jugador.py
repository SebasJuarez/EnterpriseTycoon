from empresa import Empresa

class Jugador:
    def __init__(self, nombre, dinero):
        self.nombre = nombre
        self.dinero = dinero
        self.empresas = []
        self.saltar_turno = False
        self.bono_ventas = False

    def tomar_turno(self, mercado, jugadores, mundo):
        pass

    def realizar_compra(self, empresa, precio, mundo):
        if empresa.esta_disponible() and self.dinero >= precio:
            self.empresas.append(empresa)
            self.dinero -= precio
            empresa.propietario = self
            self.aplicar_bonificacion_inmediata(empresa)

            if hasattr(empresa, "aplicar_efecto") and mundo:
                empresa.aplicar_efecto(self, mundo)

    def vender_empresa(self, empresa_nombre, precio):
        for empresa in self.empresas:
            if empresa.nombre == empresa_nombre:
                self.empresas.remove(empresa)
                self.dinero += precio
                empresa.propietario = None
                return True
        return False

    def valor_total(self):
        return self.dinero + sum(e.valor for e in self.empresas)

    def contar_por_tipo(self):
        tipos = {}
        for empresa in self.empresas:
            tipos[empresa.tipo] = tipos.get(empresa.tipo, 0) + 1
        return tipos

    def aplicar_bonificacion_inmediata(self, nueva_empresa):
        conteo = self.contar_por_tipo()
        if conteo[nueva_empresa.tipo] > 1:
            bonificacion = 500 * (conteo[nueva_empresa.tipo] - 1)
            self.dinero += bonificacion

    def __str__(self):
        return f"{self.nombre} - Dinero: ${self.dinero} - Empresas: {[e.nombre for e in self.empresas]}"


class IAJugador(Jugador):
    def __init__(self, nombre, dinero, estrategia):
        super().__init__(nombre, dinero)
        self.estrategia = estrategia

    def __str__(self):
        return f"{self.nombre} (IA) - Dinero: ${self.dinero} - Empresas: {[e.nombre for e in self.empresas]}"

    def tomar_turno(self, mercado, jugadores, mundo):
        _, mejor_accion = self.minimax_global(mercado, jugadores, jugadores.index(self), depth=2, alpha=float('-inf'), beta=float('inf'))
        if mejor_accion:
            tipo_accion, empresa = mejor_accion
            if tipo_accion == 'comprar':
                self.realizar_compra(empresa, empresa.valor, mundo)
                mercado.remove(empresa)
            elif tipo_accion == 'vender':
                self.empresas.remove(empresa)
                self.dinero += int(empresa.valor * 0.9)
                empresa.propietario = None

    def evaluar_estado_global(self, jugadores):
        for j in jugadores:
            if j.nombre == self.nombre:
                valor = j.dinero + sum(e.valor for e in j.empresas)
                tipos = j.contar_por_tipo()
                bonificacion = sum((n - 1) * 500 for n in tipos.values() if n > 1)
                return valor + bonificacion
        return 0


    def minimax_global(self, mercado, jugadores, index, depth, alpha, beta):
        if depth == 0 or not mercado:
            return self.evaluar_estado_global(jugadores), None

        jugador_actual = jugadores[index]

        acciones_posibles = []

        for empresa in mercado:
            if jugador_actual.dinero >= empresa.valor:
                acciones_posibles.append(('comprar', empresa))

        for empresa in jugador_actual.empresas:
            if len(jugador_actual.empresas) > 1 and not empresa.ventaja:
                acciones_posibles.append(('vender', empresa))

        mejor_accion = None

        if isinstance(jugador_actual, IAJugador):
            if jugador_actual.nombre == self.nombre:
                max_eval = float('-inf')
                for accion, empresa in acciones_posibles:
                    copia_jugadores, copia_mercado = simular_accion(jugadores, mercado, index, accion, empresa)
                    eval_score, _ = self.minimax_global(copia_mercado, copia_jugadores, (index + 1) % len(jugadores), depth - 1, alpha, beta)
                    if eval_score > max_eval:
                        max_eval = eval_score
                        mejor_accion = (accion, empresa)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
                return max_eval, mejor_accion
            else:
                min_eval = float('inf')
                for accion, empresa in acciones_posibles:
                    copia_jugadores, copia_mercado = simular_accion(jugadores, mercado, index, accion, empresa)
                    eval_score, _ = self.minimax_global(copia_mercado, copia_jugadores, (index + 1) % len(jugadores), depth - 1, alpha, beta)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
                return min_eval, None
        else:
            return self.minimax_global(mercado, jugadores, (index + 1) % len(jugadores), depth, alpha, beta)

def simular_accion(jugadores, mercado, index, accion, empresa):
    import copy
    jugadores_copia = copy.deepcopy(jugadores)
    mercado_copia = copy.deepcopy(mercado)
    jugador = jugadores_copia[index]

    if accion == "comprar":
        jugador.dinero -= empresa.valor
        jugador.empresas.append(empresa)
        mercado_copia = [e for e in mercado_copia if e.nombre != empresa.nombre]
    elif accion == "vender":
        jugador.dinero += int(empresa.valor * 0.9)
        jugador.empresas = [e for e in jugador.empresas if e.nombre != empresa.nombre]

    return jugadores_copia, mercado_copia