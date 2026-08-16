class EstadoPedido():
    def avancar(self, pedido):
        pass
class Recebido(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = NaFila()
        
    def __str__(self):
            return "Recebido"
class NaFila(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = EmPreparo()
    def __str__(self):
            return "Na Fila"
    
class EmPreparo(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = Pronto()

    def __str__(self):
        return "Em Preparo"
    
class Pronto(EstadoPedido):
    def avancar(self, pedido):
        raise Exception("O pedido já está pronto e não pode avançar para outro estado.")
    def __str__(self):
        return "Pronto"