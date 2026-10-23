


from models.ItensPedido import ItensPedido
from models.Pedido import Pedido


class PedidoMesa(Pedido):
    def __init__(self, id: int, itens_pedidos: list[ItensPedido], mesa: int):
        super().__init__(id, itens_pedidos)
        self.mesa = mesa