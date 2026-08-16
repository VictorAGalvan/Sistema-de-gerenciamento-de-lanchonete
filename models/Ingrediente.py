class Ingrediente():
    def __init__(self,nome,unidade,quantidade):
        self.nome = nome
        self.unidade = unidade
        self.quantidade = quantidade
    @property
    def nome(self): 
        return self.__nome
    @property
    def unidade(self):
        return self.__unidade
    @property
    def quantidade(self):
        return self.__quantidade

    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @unidade.setter
    def unidade(self, n_unidade):
        self.__unidade = n_unidade
    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade