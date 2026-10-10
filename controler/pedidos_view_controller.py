from controler.pedido_controler import PedidoControler
from models.EstadoPedido import Pronto


class PedidosViewController:
    def __init__(self):
        self.pedidos = PedidoControler()

    def listar_nao_finalizados(self):
        return self.pedidos.listar_nao_finalizados()

    def listar_por_cliente(self, cliente):
        return self.pedidos.listar_por_cliente(cliente.id)

    @staticmethod
    def calcular_total(pedido):
        return sum(item.preco * item.quantidade for item in pedido.itens_pedidos)

    def avancar_pedido(self, pedido):
        if isinstance(pedido.estado, Pronto):
            return "Este pedido já está pronto."
        self.pedidos.avancar_pedido(pedido)
        return None

    @staticmethod
    def ingredientes_e_observacao(item):
        ingredientes = ", ".join(
            f"{item.quantidades_ingredientes.get(ing.id, 1)}x {ing.nome}"
            for ing in item.ingredientes
        ) or "-"
        observacao = item.observacao or "-"
        return ingredientes, observacao
