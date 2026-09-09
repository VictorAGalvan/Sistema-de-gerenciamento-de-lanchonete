from dao.itens_pedido_dao import ItensPedidoDAO

class ItensPedidoControler:

    def __init__(self):
        self.dao = ItensPedidoDAO()

    def listar_itens_pedido(self):
        return self.dao.select()

    def buscar_item_pedido(self, id_item):
        return self.dao.selectID(id_item)

    def adicionar_item_pedido(self, item):
        return self.dao.insert(item)

    def atualizar_item_pedido(self, id_item, item):
        return self.dao.update(id_item, item)

    def remover_item_pedido(self, id_item):
        return self.dao.delete(id_item)