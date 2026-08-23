from Pedido import Pedido
from Cliente import Cliente
from EstadoPedido import Recebido

class PedidoFactory:
    @staticmethod
    def criar_pedido_mesa(mesa: int, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        pedido = Pedido(itens_pedidos=itens_pedidos, mesa=mesa)
        pedido.estado = Recebido()
        return pedido

    @staticmethod
    def criar_pedido_cliente(cliente: Cliente, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        pedido = Pedido(itens_pedidos=itens_pedidos, cliente=cliente)
        pedido.estado = Recebido()
        return pedido