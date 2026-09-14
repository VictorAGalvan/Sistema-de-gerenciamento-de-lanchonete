from datetime import date

from dao.itens_cardapio_dao import ItensCardapioDAO
from models.Cardapio import Cardapio


cardapio_mock: list[Cardapio] = [
    Cardapio(id=1, data=date(2026, 6, 26), versao="1.0", itens=ItensCardapioDAO().select())
]

_cardapio_ativo_id: int = None


class CardapioDAO:
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

    # junção cardápio <-> itens — no mock, itens já ficam em cardapio.itens
    def insertItem(self, id_cardapio: int, id_item: int) -> None:
        pass

    def deleteItens(self, id_cardapio: int) -> None:
        pass

    def get_ativo_id(self) -> int | None:
        global _cardapio_ativo_id
        if _cardapio_ativo_id is None and cardapio_mock:
            _cardapio_ativo_id = cardapio_mock[0].id
        return _cardapio_ativo_id

    def set_ativo(self, id_cardapio: int) -> None:
        global _cardapio_ativo_id
        if self.selectID(id_cardapio) is None:
            raise ValueError(f"Cardápio com id {id_cardapio} não existe.")
        _cardapio_ativo_id = id_cardapio