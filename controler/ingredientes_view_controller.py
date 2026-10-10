from sqlalchemy.exc import IntegrityError

from controler.ingrediente_controler import IngredienteController
from models.Ingrediente import Ingrediente


class IngredientesViewController:
    def __init__(self):
        self.ingredientes = IngredienteController()

    def listar(self):
        return self.ingredientes.select_ingrediente()

    @staticmethod
    def validar_dados(nome, unidade, texto_quantidade):
        nome = nome.strip()
        unidade = unidade.strip()
        texto_quantidade = texto_quantidade.strip().replace(",", ".")

        if not nome or not unidade or not texto_quantidade:
            return None, "Preencha nome, unidade e quantidade."
        try:
            quantidade = int(texto_quantidade)
        except ValueError:
            return None, "A quantidade em estoque deve ser um número inteiro."
        if quantidade < 0:
            return None, "A quantidade em estoque não pode ser negativa."
        return (nome, unidade, quantidade), None

    def adicionar(self, dados):
        nome, unidade, quantidade = dados
        self.ingredientes.insert_ingrediente(
            Ingrediente(id=None, nome=nome, unidade=unidade, quantidade=quantidade)
        )

    def salvar(self, ingrediente, nome, unidade):
        ingrediente.nome = nome
        ingrediente.unidade = unidade
        self.ingredientes.update_ingrediente(ingrediente)

    @staticmethod
    def validar_reposicao(texto_quantidade):
        try:
            quantidade = int(texto_quantidade.strip())
        except ValueError:
            return None, "Informe uma quantidade inteira para reabastecer."
        if quantidade <= 0:
            return None, "A quantidade para reabastecer deve ser maior que zero."
        return quantidade, None

    def restock(self, ingrediente, quantidade):
        self.ingredientes.restock_ingrediente(ingrediente.id, quantidade)

    def remover(self, ingrediente):
        try:
            self.ingredientes.delete_ingrediente(ingrediente)
        except IntegrityError:
            return "Não foi possível remover: o ingrediente está em uso por algum item."
        return None
