from datetime import date, datetime

from controler.cardapio_controler import CardapioControler
from controler.ingrediente_controler import IngredienteController
from controler.itens_cardapio_controler import ItensCardapioControler
from models.Cardapio import Cardapio
from models.ItensCardapio import ItensCardapio


class CardapioAdminController:
    def __init__(self):
        self.cardapios = CardapioControler()
        self.itens = ItensCardapioControler()
        self.ingredientes = IngredienteController()

    def listar_cardapios(self):
        return self.cardapios.listar_cardapios(), self.cardapios.get_ativo_id()

    def tornar_ativo(self, cardapio):
        self.cardapios.tornar_ativo(cardapio.id)

    def listar_itens(self, cardapio):
        if cardapio.id is None:
            return []
        return self.itens.listar_por_cardapio(cardapio.id)

    def listar_ingredientes(self):
        return self.ingredientes.select_ingrediente()

    @staticmethod
    def novo_cardapio():
        return Cardapio(id=None, data=date.today(), versao="")

    @staticmethod
    def pode_adicionar_itens(cardapio):
        return cardapio.id is not None

    def salvar_cardapio(self, cardapio, eh_novo, texto_data, versao):
        try:
            nova_data = datetime.strptime(texto_data, "%d/%m/%Y").date()
        except ValueError:
            return "Data inválida. Use dd/mm/aaaa."

        cardapio.data = nova_data
        cardapio.versao = versao
        if eh_novo:
            self.cardapios.criar_cardapio(cardapio)
        else:
            self.cardapios.editar_cardapio(cardapio)
        return None

    def remover_item(self, item):
        self.itens.remover_item_cardapio(item)

    def criar_item(self, cardapio, nome, texto_preco, categoria, ingredientes):
        try:
            preco = float(texto_preco)
        except ValueError:
            return "Preço inválido."

        item = ItensCardapio(
            id=None,
            nome=nome,
            preco=preco,
            categoria=categoria,
            ingredientes=ingredientes,
            id_cardapio=cardapio.id,
        )
        self.itens.criar_item_cardapio(item)
        return None

    def salvar_item(self, item, nome, texto_preco, categoria):
        try:
            preco = float(texto_preco)
        except ValueError:
            return "Preço inválido."

        item.nome = nome
        item.preco = preco
        item.categoria = categoria
        self.itens.editar_item_cardapio(item)
        return None
