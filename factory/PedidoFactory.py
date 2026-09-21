from models.Pedido import Pedido
from models.Cliente import Cliente
from models.PedidoCliente import PedidoCliente
from models.PedidoMesa import PedidoMesa


class PedidoFactory:
    @staticmethod
    def criar_pedido_mesa(id: int, mesa: int, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        return PedidoMesa(id=id, itens_pedidos=itens_pedidos, mesa=mesa)

    @staticmethod
    def criar_pedido_cliente(id: int, cliente: Cliente, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        return PedidoCliente(id=id, itens_pedidos=itens_pedidos, cliente=cliente)