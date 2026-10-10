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
            quantidade = float(texto_quantidade)
        except ValueError:
            return None, "Quantidade inválida."
        return (nome, unidade, quantidade), None

    def adicionar(self, dados):
        nome, unidade, quantidade = dados
        self.ingredientes.insert_ingrediente(
            Ingrediente(id=None, nome=nome, unidade=unidade, quantidade=quantidade)
        )

    def salvar(self, ingrediente, dados):
        ingrediente.nome, ingrediente.unidade, ingrediente.quantidade = dados
        self.ingredientes.update_ingrediente(ingrediente)

    def remover(self, ingrediente):
        try:
            self.ingredientes.delete_ingrediente(ingrediente)
        except IntegrityError:
            return "Não foi possível remover: o ingrediente está em uso por algum item."
        return None
