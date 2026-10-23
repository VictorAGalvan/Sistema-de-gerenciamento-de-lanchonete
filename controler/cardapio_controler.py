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

    def editar_cardapio(self, cardapio):
        self.dao.update(cardapio)

    def remover_cardapio(self, cardapio):
        self.dao.delete(cardapio)

    def get_ativo_id(self):
        return self.dao.get_ativo_id()

    def get_ativo(self):
        return self.dao.get_ativo()

    def tornar_ativo(self, id_cardapio):
        self.dao.set_ativo(id_cardapio)