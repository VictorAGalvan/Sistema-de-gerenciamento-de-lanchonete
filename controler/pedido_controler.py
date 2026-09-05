from dao.pedido_dao import PedidoDAO

class PedidoController:

    def __init__(self):
        self.dao = PedidoDAO()

    def select_pedido(self):
        return self.dao.select()

    def insert_pedido(self, pedido):
        return self.dao.insert(pedido)

    def update_pedido(self, pedido):
        return self.dao.update(pedido)

    def delete_pedido(self, pedido):
        return self.dao.delete(pedido)

    def selectID_pedido(self, id):
        return self.dao.selectID(id)