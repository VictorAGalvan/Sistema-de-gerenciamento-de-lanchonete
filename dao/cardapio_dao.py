from datetime import date

from dao.itens_cardapio_dao import ItensCardapioDAO
from models.Cardapio import Cardapio


cardapio_mock: list[Cardapio] = [
    Cardapio(id=1, data=date(2026, 6, 26), versao="1.0", ativo=True)
]


class CardapioDAO:
    def __init__(self):
        self.dao_itens = ItensCardapioDAO()

    def _pegar_maior_id(self) -> int:
        pk = 0
        for cardapio in cardapio_mock:
            if cardapio.id > pk:
                pk = cardapio.id
        return pk

    def select(self) -> list[Cardapio]:
        return cardapio_mock

    def selectID(self, id: int) -> Cardapio | None:
        for cardapio in cardapio_mock:
            if cardapio.id == id:
                return cardapio
        return None

    def insert(self, cardapio: Cardapio) -> None:
        cardapio.id = self._pegar_maior_id() + 1
        cardapio_mock.append(cardapio)

    def update(self, cardapio: Cardapio) -> None:
        pass

    def delete(self, cardapio: Cardapio) -> None:
        cardapio_mock.remove(cardapio)

    def get_ativo(self) -> Cardapio | None:
        for cardapio in cardapio_mock:
            if cardapio.ativo:
                return cardapio
        return None

    def get_ativo_id(self) -> int | None:
        ativo = self.get_ativo()
        return ativo.id if ativo else None

    def set_ativo(self, id_cardapio: int) -> None:
        alvo = self.selectID(id_cardapio)
        if alvo is None:
            raise ValueError(f"Cardápio com id {id_cardapio} não existe.")

        for cardapio in cardapio_mock:
            cardapio.ativo = (cardapio.id == id_cardapio)