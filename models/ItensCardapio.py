class ItensCardapio():
    def __init__(self,id:int, nome:str,preco:float,categoria:str, igredientes:list[str]):
        self.__id = id
        self.__nome = nome
        self.__preco = preco
        self.__categoria = categoria
        self.__igredientes = igredientes


    @property
    def id(self):
        return self.__id

    @property
    def igredientes(self):
        return self.__igredientes
    
    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @property
    def categoria(self):
        return self.__categoria


    @id.setter
    def id(self, n_id):
        self.__id = n_id
    @igredientes.setter
    def igredientes(self, n_igredientes):
        self.__igredientes = n_igredientes
    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @preco.setter
    def preco(self, n_preco):
        self.__preco = n_preco
    @categoria.setter
    def categoria(self, n_categoria):
        self.__categoria = n_categoria