from dao.generic_dao import GenericDAO
from models.ItensCardapio import ItensCardapio


itens_cardapio_mock:list[ItensCardapio] = []

class ItensCardapioDAO(GenericDAO):
    def insert(self, itens_cardapio: ItensCardapio) -> None:
        itens_cardapio_mock.append(itens_cardapio)

    def select_por_id(self, itens_cardapio_id: int) -> ItensCardapio | None:
        for itens_cardapio in itens_cardapio_mock:
            if itens_cardapio.id == itens_cardapio_id:
                return itens_cardapio
        return None

    def select_todos(self) -> list[ItensCardapio]:
        return itens_cardapio_mock

    def delete(self, itens_cardapio_id: int) -> None:
        for i in itens_cardapio_mock:
            if i.id == itens_cardapio_id:
                itens_cardapio_mock.remove(i)
                break

    def update(self, itens_cardapio: ItensCardapio) -> None:
        for i in itens_cardapio_mock:
            if itens_cardapio == i:
                itens_cardapio_mock.remove(i)
                itens_cardapio_mock.append(itens_cardapio)
                break
