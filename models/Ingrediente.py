class Ingrediente():
    def __init__(self,id:int,nome:str,unidade:str,quantidade:float):
        self.__id = id
        self.__nome = nome
        self.__unidade = unidade
        self.__quantidade = quantidade
    @property
    def nome(self): 
        return self.__nome
    @property
    def unidade(self):
        return self.__unidade
    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def id(self):
        return self.__id
    


    @id.setter
    def id(self, n_id):
        self.__id = n_id
    
    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @unidade.setter
    def unidade(self, n_unidade):
        self.__unidade = n_unidade
    @quantidade.setter
    def quantidade(self, n_quantidade):
        self.__quantidade = n_quantidade