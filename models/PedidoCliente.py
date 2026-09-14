

from models.Cliente import Cliente
from models.ItensPedido import ItensPedido
from models.Pedido import Pedido


class PedidoCliente(Pedido):
    def __init__(self, id: int, itens_pedidos: list[ItensPedido], cliente: Cliente):
        super().__init__(id, itens_pedidos)
        self.cliente = cliente