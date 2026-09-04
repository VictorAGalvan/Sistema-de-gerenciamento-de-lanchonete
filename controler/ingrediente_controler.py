from dao.ingrediente_dao import IngredienteDAO
from models.Ingrediente import Ingrediente


class Ingrediente_Controler:
    def __init__(self):
        self.dao = IngredienteDAO()

    def cadastrar(self, nome, quantidade):

        ingrediente = Ingrediente(nome=nome, quantidade=quantidade)

        return self.dao.inserir(ingrediente)

    def listar(self):

        return self.dao.listar()

    def excluir(self, id):

        self.dao.excluir(id)
