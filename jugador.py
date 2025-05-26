from empresa import Empresa

class Jugador:
    def __init__(self, nombre, dinero):
        self.nombre = nombre
        self.dinero = dinero
        self.empresas = []
        self.saltar_turno = False
        self.bono_ventas = False

    def tomar_turno(self, mercado, jugadores, mundo):
        print(f"\nTurno de {self.nombre}")
        for i, empresa in enumerate(mercado):
            print(f"{i}: {empresa}")
        decision = input("¿Deseas negociar una empresa del mercado? (número o 'v' para vender/pasar): ")
        if decision.lower() == 'v':
            self.mostrar_empresas_para_vender()
            return
        try:
            idx = int(decision)
            if 0 <= idx < len(mercado):
                empresa = mercado[idx]
                if empresa.tipo in self.contar_por_tipo():
                    print("⚠ Puedes obtener una bonificación si compras esta empresa.")
                if self.negociar_compra(empresa):
                    mercado.remove(empresa)
        except:
            print("Entrada inválida.")

    def negociar_compra(self, empresa):
        print(f"\nNegociando con el mercado por {empresa.nombre} (Valor base: ${empresa.valor})")
        intento = 0
        precio_objetivo = empresa.valor
        while intento < 3:
            try:
                oferta = int(input("Haz tu oferta: "))
                if oferta >= precio_objetivo * 0.9:
                    print("¡Oferta aceptada!")
                    self.realizar_compra(empresa, oferta)
                    return True
                elif oferta >= precio_objetivo * 0.7:
                    contraoferta = int((oferta + precio_objetivo) // 2)
                    print(f"Contraoferta: ${contraoferta}")
                    aceptar = input("¿Aceptas la contraoferta? (s/n): ")
                    if aceptar.lower() == 's':
                        self.realizar_compra(empresa, contraoferta)
                        return True
                else:
                    print("Oferta rechazada. Intenta con una mejor.")
                intento += 1
            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")
        print("No se logró un acuerdo.")
        return False

    def realizar_compra(self, empresa, precio, mundo):
        if empresa.esta_disponible() and self.dinero >= precio:
            self.empresas.append(empresa)
            self.dinero -= precio
            empresa.propietario = self
            self.aplicar_bonificacion_inmediata(empresa)

            print(f"Has comprado {empresa.nombre} por ${precio}.")
            if empresa.ventaja:
                print(f"¡Has desbloqueado la ventaja especial: {empresa.ventaja}!")

            # Aplicar efecto si existe y se proporciona el mundo
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

    def mostrar_empresas_para_vender(self):
        if not self.empresas:
            print("No tienes empresas para vender.")
            return
        for i, emp in enumerate(self.empresas):
            print(f"{i}: {emp}")
        try:
            idx = int(input("¿Cuál deseas vender? (número): "))
            precio = int(input("¿Por cuánto deseas venderla?: "))
            emp = self.empresas[idx]
            self.vender_empresa(emp.nombre, precio)
            print(f"Vendiste {emp.nombre} por ${precio}.")
        except:
            print("Entrada inválida.")

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
            print(f"{self.nombre} recibió ${bonificacion} de bonificación inmediata por sinergia de empresas.")

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
                print(f"{self.nombre} compró {empresa.nombre} usando Minimax.")
            elif tipo_accion == 'vender':
                self.empresas.remove(empresa)
                self.dinero += int(empresa.valor * 0.9)
                empresa.propietario = None
                print(f"{self.nombre} vendió {empresa.nombre} por ${int(empresa.valor * 0.9)} usando Minimax.")

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

            # Simular compras
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

            # Simular ventas con restricciones
            for empresa in self.empresas:
                if len(self.empresas) <= 1:
                    continue  # no vender si es la única
                if empresa.ventaja:
                    continue  # no vender si tiene ventaja especial

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
