from models.ItensCardapio import ItensCardapio


class ItensPedido(ItensCardapio):
    def __init__(
        self,
        item_cardapio: ItensCardapio,
        quantidade: int,
        observacao: str = "",
        quantidades_ingredientes: dict = None,
    ):
        super().__init__(
            item_cardapio.id,
            item_cardapio.nome,
            item_cardapio.preco,
            item_cardapio.categoria,
            list(item_cardapio.ingredientes)
        )
        self.__quantidade = quantidade
        self.__observacao = observacao
        self.__quantidades_ingredientes = (
            quantidades_ingredientes
            if quantidades_ingredientes is not None
            else {ingrediente.id: 1 for ingrediente in self.ingredientes}
        )

    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def observacao(self):
        return self.__observacao

    @property
    def quantidades_ingredientes(self):
        return self.__quantidades_ingredientes


    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade
    @observacao.setter
    def observacao(self, n_observacao):
        self.__observacao = n_observacao

    @quantidades_ingredientes.setter
    def quantidades_ingredientes(self, n_quantidades):
        self.__quantidades_ingredientes = dict(n_quantidades)
    