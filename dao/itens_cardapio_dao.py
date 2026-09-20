from models.ItensCardapio import ItensCardapio
from models.Ingrediente import Ingrediente


itens_cardapio_mock: list[ItensCardapio] = [
    ItensCardapio(id=1, nome="X-Burguer", preco=10.0, categoria="Lanche", id_cardapio=1, ingredientes=[
        Ingrediente(id=1, nome="Pão", unidade="unidade", quantidade=1),
        Ingrediente(id=2, nome="Hambúrguer", unidade="unidade", quantidade=1),
        Ingrediente(id=3, nome="Queijo", unidade="fatia", quantidade=1),
    ]),
    ItensCardapio(id=2, nome="Coca-Cola", preco=5.0, categoria="Bebida", id_cardapio=1, ingredientes=[]),
    ItensCardapio(id=3, nome="Batata Frita", preco=7.0, categoria="Acompanhamento", id_cardapio=1, ingredientes=[]),
    ItensCardapio(id=4, nome="Sorvete", preco=4.0, categoria="Sobremesa", id_cardapio=1, ingredientes=[]),
]


class ItensCardapioDAO:
    def _pegar_maior_id(self) -> int:
        pk = 0
        for item in itens_cardapio_mock:
            if item.id > pk:
                pk = item.id
        return pk

    def select(self) -> list[ItensCardapio]:
        return itens_cardapio_mock

    def selectID(self, id: int) -> ItensCardapio | None:
        for item in itens_cardapio_mock:
            if item.id == id:
                return item
        return None

    def select_por_cardapio(self, id_cardapio: int) -> list[ItensCardapio]:
        return [item for item in itens_cardapio_mock if item.id_cardapio == id_cardapio]

    def insert(self, item: ItensCardapio) -> None:
        item.id = self._pegar_maior_id() + 1
        itens_cardapio_mock.append(item)

    def update(self, item: ItensCardapio) -> None:
        pass  # já é o mesmo objeto na lista; alterações refletem direto

    def delete(self, item: ItensCardapio) -> None:
        itens_cardapio_mock.remove(item)

    def selectIngredientes(self, id_item: int) -> list[Ingrediente]:
        item = self.selectID(id_item)
        return item.ingredientes if item else []

    def insertIngrediente(self, id_item: int, id_ingrediente: int) -> None:
        pass

    def deleteIngredientes(self, id_item: int) -> None:
        pass