from dao.itens_pedido_dao import ItensPedidoDAO


class ItensPedidoControler:
    def __init__(self):
        self.dao = ItensPedidoDAO()

    def listar_itens_pedido(self):
        return self.dao.select()

    def buscar_item_pedido(self, id_item):
        return self.dao.selectID(id_item)

    def criar_item_pedido(self, item):
        self.dao.insert(item)
        for ingrediente in item.ingredientes:
            self.dao.insertIngrediente(item.id, ingrediente.id)

    def editar_item_pedido(self, item):
        self.dao.update(item)
        self.dao.deleteIngredientes(item.id)
        for ingrediente in item.ingredientes:
            self.dao.insertIngrediente(item.id, ingrediente.id)

    def remover_item_pedido(self, item):
        self.dao.deleteIngredientes(item.id)
        self.dao.delete(item)