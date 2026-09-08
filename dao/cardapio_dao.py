from datetime import date

from models import ItensCardapio
from models.Cardapio import Cardapio
from dao.generic_dao import GenericDAO

cardapio_mock: list[Cardapio] = [
    Cardapio(
        id=1,
        data=date(2026, 6, 26),
        versao="1.0",
        itens=[
            ItensCardapio(id=1, nome="X-Burguer", preco=10.0, categoria="Lanche", igredientes=[]),
            ItensCardapio(id=2, nome="Coca-Cola", preco=5.0, categoria="Bebida", igredientes=[]),
        ]
    )
]

class CardapioDAO (GenericDAO):
    def pegar_maior_id(self) -> int:
            pk = 0
            if not cardapio_mock:
                return pk
            
            for cardapio in cardapio_mock:
                if cardapio.id is None:
                    raise ValueError("Cardapio ID não pode ser None")
                if cardapio.id > pk:
                    pk = cardapio.id
            return pk
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
