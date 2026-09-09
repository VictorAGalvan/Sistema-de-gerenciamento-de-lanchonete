from dao.cardapio_dao import CardapioDAO

class ItensCardapioControler:
    
    def __init__(self):
        self.dao = CardapioDAO()

    def listar_itens_cardapio(self):
        return self.dao.select()
    def buscar_item_cardapio(self, id_item):
        return self.dao.selectID(id_item)
    def adicionar_item_cardapio(self, item):
        return self.dao.insert(item)
    def atualizar_item_cardapio(self, id_item, item):
        return self.dao.update  (id_item, item)
    def remover_item_cardapio(self, id_item):
        return self.dao.delete(id_item)