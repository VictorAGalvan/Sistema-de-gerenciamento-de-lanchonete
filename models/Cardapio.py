from datetime import date


class Cardapio():
    def __init__(self, id: int, data: date, versao: str, ativo: bool = False):
        self.__id = id
        self.__data = data
        self.__versao = versao
        self.__ativo = ativo

    @property
    def data(self):
        return self.__data
    @property
    def versao(self):
        return self.__versao
    @property
    def id(self):
        return self.__id
    @property
    def ativo(self):
        return self.__ativo

    @id.setter
    def id(self, n_id):
        self.__id = n_id
    @data.setter
    def data(self, n_data):
        self.__data = n_data
    @versao.setter
    def versao(self, n_versao):
        self.__versao = n_versao
    @ativo.setter
    def ativo(self, n_ativo):
        self.__ativo = n_ativo

    def __eq__(self, outro):
        if isinstance(outro, Cardapio):
            return self.__id == outro.__id
        return False