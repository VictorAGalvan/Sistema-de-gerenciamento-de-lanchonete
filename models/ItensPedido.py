from models.ItensCardapio import ItensCardapio


class ItensPedido(ItensCardapio):
    def __init__(self, item_cardapio: ItensCardapio, quantidade: int, observacao: str = ""):
        super().__init__(
            item_cardapio.id,
            item_cardapio.nome,
            item_cardapio.preco,
            item_cardapio.categoria,
            list(item_cardapio.igredientes)
        )
        self.__quantidade = quantidade
        self.__observacao = observacao

    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def observacao(self):
        return self.__observacao


    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade
    @observacao.setter
    def observacao(self, n_observacao):
        self.__observacao = n_observacao
    