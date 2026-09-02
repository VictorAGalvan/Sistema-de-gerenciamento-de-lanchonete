from dao.generic_dao import GenericDAO
from models.Ingrediente import Ingrediente


ingrediente_mock:list[Ingrediente] = []

class IngredienteDAO(GenericDAO):
    def insert(self, ingrediente: Ingrediente) -> None:
        ingrediente_mock.append(ingrediente)

    def select_por_id(self, ingrediente_id: int) -> Ingrediente | None:
        for ingrediente in ingrediente_mock:
            if ingrediente.id == ingrediente_id:
                return ingrediente
        return None

    def select_todos(self) -> list[Ingrediente]:
        return ingrediente_mock

    def delete(self, ingrediente_id: int) -> None:
        for i in ingrediente_mock:
            if i.id == ingrediente_id:
                ingrediente_mock.remove(i)
                break

    def update(self, ingrediente: Ingrediente) -> None:
        for i in ingrediente_mock:
            if ingrediente == i:
                ingrediente_mock.remove(i)
                ingrediente_mock.append(ingrediente)
                break
