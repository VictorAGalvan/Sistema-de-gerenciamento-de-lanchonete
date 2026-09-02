from models.Cardapio import Cardapio
from dao.generic_dao import GenericDAO

cardapio_mock:list[Cardapio] = []

class CardapioDAO (GenericDAO):
    def insert(self, cardapio: Cardapio) -> None:
        cardapio_mock.append(cardapio)

    def select_por_id(self, cardapio_id: int) -> Cardapio | None:
        for cardapio in cardapio_mock:
            if cardapio.id == cardapio_id:
                return cardapio
        return None

    def select_todos(self) -> list[Cardapio]:
        return cardapio_mock

    def delete(self, cardapio_id: int) -> None:
        for i in cardapio_mock:
            if i.id == cardapio_id:
                cardapio_mock.remove(i)
                break

    def update(self, cardapio: Cardapio) -> None:
        for i in cardapio_mock:
            if cardapio == i:
                cardapio_mock.remove(i)
                cardapio_mock.append(cardapio)
                break
