class Cliente():
    def __init__(self, nome:str, cpf:str, telefone:str):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    @property
    def nome(self):
        return self.__nome
    @property
    def cpf(self): 
        return self.__cpf
    @property
    def telefone(self):
        return self.__telefone


    @nome.setter
    def nome(self, n_nome):
        self.__nome = n_nome
    @cpf.setter
    def cpf(self, n_cpf):
        self.__cpf = n_cpf
    @telefone.setter
    def telefone(self, n_telefone):
        self.__telefone = n_telefone