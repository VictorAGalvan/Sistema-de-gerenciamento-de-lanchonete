from datetime import date

from dao.itens_cardapio_dao import ItensCardapioDAO
from models.Cardapio import Cardapio
from dao.generic_dao import GenericDAO

cardapio_mock: list[Cardapio] = [
    Cardapio(
        id=1,
        data=date(2026, 6, 26),
        versao="1.0",
        itens=ItensCardapioDAO().select_todos()
    )
]

_cardapio_ativo_id: int = None


class CardapioDAO(GenericDAO):
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

    def get_ativo_id(self) -> int | None:
        global _cardapio_ativo_id
        if _cardapio_ativo_id is None and cardapio_mock:
            _cardapio_ativo_id = cardapio_mock[0].id
        return _cardapio_ativo_id

    def get_ativo(self) -> Cardapio | None:
        ativo_id = self.get_ativo_id()
        if ativo_id is None:
            return None
        return self.select_por_id(ativo_id)

    def set_ativo(self, cardapio_id: int) -> None:
        global _cardapio_ativo_id
        if self.select_por_id(cardapio_id) is None:
            raise ValueError(f"Cardápio com id {cardapio_id} não existe.")
        _cardapio_ativo_id = cardapio_id