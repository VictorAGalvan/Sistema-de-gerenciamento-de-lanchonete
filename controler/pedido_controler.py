from dao.pedido_dao import PedidoDAO


class PedidoControler:
    def __init__(self):
        self.dao = PedidoDAO()

    def listar_pedidos(self):
        return self.dao.select()

    def buscar_pedido(self, id_pedido):
        return self.dao.selectID(id_pedido)

    def criar_pedido(self, pedido):
        self.dao.insert(pedido)
        for item_pedido in pedido.itens_pedidos:
            self.dao.insertItemPedido(pedido.id, item_pedido.id)

    def avancar_pedido(self, pedido):
        pedido.estado.avancar(pedido)
        self.dao.update(pedido)
        
    def listar_nao_finalizados(self):
      return self.dao.select_nao_finalizados()

    def listar_por_cliente(self, id_cliente):
        return self.dao.select_por_cliente(id_cliente)
