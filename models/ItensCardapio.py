from models.Ingrediente import Ingrediente


class ItensCardapio():
    def __init__(self, id: int, nome: str, preco: float, categoria: str, ingredientes: list[Ingrediente], id_cardapio: int = None):
        self.__id = id
        self.__nome = nome
        self.__preco = preco
        self.__categoria = categoria
        self.__ingredientes = ingredientes
        self.__id_cardapio = id_cardapio


    @property
    def id(self):
        return self.__id

    @property
    def ingredientes(self):
        return self.__ingredientes
    
    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @property
    def categoria(self):
        return self.__categoria

    @property
    def id_cardapio(self):
        return self.__id_cardapio


    @id.setter
    def id(self, n_id):
        self.__id = n_id
    @ingredientes.setter
    def ingredientes(self, n_ingredientes):
        self.__ingredientes = n_ingredientes
    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @preco.setter
    def preco(self, n_preco):
        self.__preco = n_preco
    @categoria.setter
    def categoria(self, n_categoria):
        self.__categoria = n_categoria
    @id_cardapio.setter
    def id_cardapio(self, n_id_cardapio):
        self.__id_cardapio = n_id_cardapio

    def __eq__(self, outro):
        if isinstance(outro, ItensCardapio):
            return self.__id == outro.__id
        return False

    def __hash__(self):
        return hash(self.__id)