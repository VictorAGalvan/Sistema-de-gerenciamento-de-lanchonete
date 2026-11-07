from controler.ingrediente_controler import IngredienteController
from models.Ingrediente import Ingrediente

class IngredienteView:

    def __init__(self):
        self.controller = IngredienteController()

    def cadastrar(self):
        nome = input("Nome do ingrediente: ")
        quantidade = int(input("Quantidade: "))

        ingrediente = self.controller.insert_ingrediente(
            Ingrediente(id=None, nome=nome, unidade="un", quantidade=quantidade)
        )

        print(f"Ingrediente {ingrediente.nome} cadastrado!")
