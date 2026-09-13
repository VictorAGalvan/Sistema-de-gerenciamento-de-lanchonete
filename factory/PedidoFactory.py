from models.Pedido import Pedido
from models.Cliente import Cliente
from models.EstadoPedido import Recebido
from models.PedidoCliente import PedidoCliente
from models.PedidoMesa import PedidoMesa
from dao.cliente_dao import ClienteDAO
class PedidoFactory:
    @staticmethod
    def criar_pedido_mesa(mesa: int, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        pedido = PedidoMesa(id=ClienteDAO().pegar_maior_id()+1,itens_pedidos=itens_pedidos, mesa=mesa)
        
        return pedido

    @staticmethod
    def criar_pedido_cliente(cliente: Cliente, itens_pedidos: list) -> Pedido:
        if not itens_pedidos:
            raise Exception("Pedido precisa ter ao menos um item")
        pedido = PedidoCliente(id=ClienteDAO().pegar_maior_id()+1,itens_pedidos=itens_pedidos, cliente=cliente)

        return pedido