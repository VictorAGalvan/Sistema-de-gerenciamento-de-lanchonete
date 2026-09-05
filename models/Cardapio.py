from datetime import date

from .ItensCardapio import ItensCardapio


class Cardapio():
    def __init__(self,id:int, data:date, versao:str, itens:list[ItensCardapio]):
        self.__id = id
        self.__data =data
        self.__versao = versao
        self.__itens = itens
    
    @property
    def data(self):
        return self.__data
    @property
    def versao(self):
        return self.__versao
    @property
    def itens(self):
        return self.__itens
    @property
    def id(self):
        return self.__id
    

    @id.setter
    def id(self, n_id):
        self.__id = n_id

    @data.setter
    def data(self, n_data):
        self.__data = n_data
    @versao.setter
    def versao(self, n_versao):
        self.__versao = n_versao
    @itens.setter
    def itens(self, n_itens):
        self.__itens = n_itens

    def __eq__(self, other):
        if isinstance(other, Cardapio):
            return self.__id == other.__id
        return False