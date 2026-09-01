class Cliente():
    def __init__(self, id:int, nome:str, cpf:str, telefone:str):
        self.__id = id
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone

    @property
    def nome(self):
        return self.__nome
    @property
    def cpf(self): 
        return self.__cpf
    @property
    def telefone(self):
        return self.__telefone
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, n_id):
        self.__id = n_id
    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @cpf.setter
    def cpf(self, n_cpf):
        self.__cpf = n_cpf
    @telefone.setter
    def telefone(self, n_telefone):
        self.__telefone = n_telefone