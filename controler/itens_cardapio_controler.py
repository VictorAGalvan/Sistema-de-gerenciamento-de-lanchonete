from dao.itens_cardapio_dao import ItensCardapioDAO


class ItensCardapioControler:

    def __init__(self):
        self.dao = ItensCardapioDAO()

    def listar_itens_cardapio(self):
        return self.dao.select()

    def listar_por_cardapio(self, id_cardapio):
        return self.dao.select_por_cardapio(id_cardapio)

    def buscar_item_cardapio(self, id_item):
        return self.dao.selectID(id_item)

    def criar_item_cardapio(self, item):
        self.dao.insert(item)
        for ingrediente in item.ingredientes:
            self.dao.insertIngrediente(item.id, ingrediente.id)

    def editar_item_cardapio(self, item):
        self.dao.update(item)
        self.dao.deleteIngredientes(item.id)
        for ingrediente in item.ingredientes:
            self.dao.insertIngrediente(item.id, ingrediente.id)

    def remover_item_cardapio(self, item):
        self.dao.deleteIngredientes(item.id)
        self.dao.delete(item)