from dao.cardapio_dao import CardapioDAO


class CardapioControler:
    def __init__(self):
        self.dao = CardapioDAO()

    def listar_cardapios(self):
        return self.dao.select()

    def buscar_cardapio(self, id_cardapio):
        return self.dao.selectID(id_cardapio)

    def criar_cardapio(self, cardapio):
        self.dao.insert(cardapio)
        for item in cardapio.itens:
            self.dao.insertItem(cardapio.id, item.id)

    def editar_cardapio(self, cardapio):
        self.dao.update(cardapio)
        self.dao.deleteItens(cardapio.id)
        for item in cardapio.itens:
            self.dao.insertItem(cardapio.id, item.id)

    def remover_cardapio(self, cardapio):
        self.dao.deleteItens(cardapio.id)
        self.dao.delete(cardapio)

    def get_ativo_id(self):
      return self.dao.get_ativo_id()

    def tornar_ativo(self, id_cardapio):
        self.dao.set_ativo(id_cardapio)