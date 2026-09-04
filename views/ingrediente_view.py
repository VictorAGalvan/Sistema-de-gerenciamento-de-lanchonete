from controllers.IngredienteController import IngredienteController


class IngredienteView:

    def __init__(self):
        self.controller = IngredienteController()

    def cadastrar(self):
        nome = input("Nome do ingrediente: ")
        quantidade = int(input("Quantidade: "))

        ingrediente = self.controller.cadastrar(nome, quantidade)

        print(f"Ingrediente {ingrediente.nome} cadastrado!")
