from dao.cardapio_dao import CardapioDAO

class CardapioController:

    def __init__(self):
        self.dao = CardapioDAO()

    def select_cardapio(self):
        return self.dao.select()

    def insert_cardapio(self, cardapio):
        return self.dao.insert(cardapio)

    def update_cardapio(self, cardapio):
        return self.dao.update(cardapio)

    def delete_cardapio(self, cardapio):
        return self.dao.delete(cardapio)

    def selectID_cardapio(self, id):
        return self.dao.selectID(id)