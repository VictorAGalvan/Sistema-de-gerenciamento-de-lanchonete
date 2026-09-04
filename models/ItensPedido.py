from models import ItensCardapio, Pedido


class ItensPedido(ItensCardapio):
    def __init__(self, pedido:Pedido, item_cardapio:ItensCardapio, quantidade:int, observacao:str,nome:str, preco:float, categoria:str):
        super().__init__(None, nome, preco, categoria)
        self.pedido = pedido
        self.item_cardapio = item_cardapio
        self.quantidade = quantidade
        self.observacao = observacao


    @property
    def pedido(self):
        return self.__pedido
    @property
    def item_cardapio(self):
        return self.__item_cardapio
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
    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade
    @observacao.setter
    def observacao(self, n_observacao):
        self.__observacao = n_observacao
    