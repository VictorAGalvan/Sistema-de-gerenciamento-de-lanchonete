from models import ItensCardapio, Pedido


class ItensPedidos():
    def __init__(self, pedido:Pedido, item_cardapio:ItensCardapio, quantidade:int, observacao:str):
        self.pedido = pedido
        self.item_cardapio = item_cardapio
        self.nome = item_cardapio.nome
        self.preco = item_cardapio.preco
        self.quantidade = quantidade
        self.observacao = observacao


    @property
    def pedido(self):
        return self.__pedido
    @property
    def item_cardapio(self):
        return self.__item_cardapio
    @property
    def nome(self):
        return self.__nome
    @property
    def preco(self):
        return self.__preco
    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def observacao(self):
        return self.__observacao

    @pedido.setter
    def pedido(self, n_pedido):
        self.__pedido = n_pedido   
    @item_cardapio.setter
    def item_cardapio(self, n_item_cardapio):
        self.__item_cardapio = n_item_cardapio
    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @preco.setter
    def preco(self, n_preco):
        self.__preco = n_preco
    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade
    @observacao.setter
    def observacao(self, n_observacao):
        self.__observacao = n_observacao
    