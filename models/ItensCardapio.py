class ItensCardapio():
    def __init__(self,nome:str,preco:float,categoria:str):
        self.nome = nome
        self.preco = preco
        self.categoria = categoria

    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @property
    def categoria(self):
        return self.__categoria

    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @preco.setter
    def preco(self, n_preco):
        self.__preco = n_preco
    @categoria.setter
    def categoria(self, n_categoria):
        self.__categoria = n_categoria