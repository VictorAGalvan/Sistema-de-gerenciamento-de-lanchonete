from datetime import date

from ItensCardapio import ItensCardapio


class Cardapio():
    def __init__(self, data:date, versao:str, itens:list[ItensCardapio]):
        self.data =data
        self.versao = versao
        self.itens = itens
    
    @property
    def data(self):
        return self.__data
    @property
    def versao(self):
        return self.__versao
    @property
    def itens(self):
        return self.__itens


    @data.setter
    def data(self, n_data):
        self.__data = n_data
    @versao.setter
    def versao(self, n_versao):
        self.__versao = n_versao
    @itens.setter
    def itens(self, n_itens):
        self.__itens = n_itens