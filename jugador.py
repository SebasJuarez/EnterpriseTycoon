from empresa import Empresa

class Jugador:
    def __init__(self, nombre, dinero):
        self.nombre = nombre
        self.dinero = dinero
        self.empresas = []
        self.saltar_turno = False
        self.bono_ventas = False

    def tomar_turno(self, mercado, jugadores, mundo):
        # El turno del jugador humano será manejado desde la interfaz gráfica.
        pass

    def realizar_compra(self, empresa, precio, mundo):
        if empresa.esta_disponible() and self.dinero >= precio:
            self.empresas.append(empresa)
            self.dinero -= precio
            empresa.propietario = self
            self.aplicar_bonificacion_inmediata(empresa)

            # Aplicar efecto si existe
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
        _, mejor_accion = self.minimax(mercado, jugadores, depth=2, maximizing_player=True, alpha=float('-inf'), beta=float('inf'))
        if mejor_accion:
            tipo_accion, empresa = mejor_accion
            if tipo_accion == 'comprar':
                self.realizar_compra(empresa, empresa.valor, mundo)
                mercado.remove(empresa)
            elif tipo_accion == 'vender':
                self.empresas.remove(empresa)
                self.dinero += int(empresa.valor * 0.9)
                empresa.propietario = None

    def evaluar_estado(self, empresas, jugadores):
        valor = self.dinero + sum(e.valor for e in self.empresas)
        tipos = self.contar_por_tipo()
        bonificacion = sum((n - 1) * 500 for n in tipos.values() if n > 1)
        return valor + bonificacion

    def minimax(self, mercado, jugadores, depth, maximizing_player, alpha, beta):
        if depth == 0 or not mercado:
            return self.evaluar_estado(mercado, jugadores), None

        if maximizing_player:
            max_eval = float('-inf')
            best_choice = None

            for empresa in mercado:
                if self.dinero >= empresa.valor:
                    simulador = IAJugador(self.nombre, self.dinero - empresa.valor, self.estrategia)
                    simulador.empresas = self.empresas + [empresa]
                    eval_score, _ = simulador.minimax(
                        [e for e in mercado if e != empresa], jugadores, depth - 1, False, alpha, beta
                    )
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_choice = ('comprar', empresa)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

            for empresa in self.empresas:
                if len(self.empresas) <= 1 or empresa.ventaja:
                    continue
                venta_valor = int(empresa.valor * 0.9)
                simulador = IAJugador(self.nombre, self.dinero + venta_valor, self.estrategia)
                simulador.empresas = [e for e in self.empresas if e != empresa]
                eval_score, _ = simulador.minimax(mercado, jugadores, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_choice = ('vender', empresa)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return max_eval, best_choice

        else:
            min_eval = float('inf')
            for empresa in mercado:
                if self.dinero >= empresa.valor:
                    simulador = IAJugador(self.nombre, self.dinero - empresa.valor, self.estrategia)
                    simulador.empresas = self.empresas + [empresa]
                    eval_score, _ = simulador.minimax(
                        [e for e in mercado if e != empresa], jugadores, depth - 1, True, alpha, beta
                    )
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval, None
