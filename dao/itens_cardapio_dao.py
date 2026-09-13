from dao.generic_dao import GenericDAO
from models.Ingrediente import Ingrediente
from models.ItensCardapio import ItensCardapio


itens_cardapio_mock: list[ItensCardapio] = [
        ItensCardapio(id=1, nome="X-Burguer", preco=10.0, categoria="Lanche", ingredientes=[Ingrediente(id=1, nome="Pão", unidade="unidade", quantidade=1), Ingrediente(id=2, nome="Hambúrguer", unidade="unidade", quantidade=1), Ingrediente(id=3, nome="Queijo", unidade="fatia", quantidade=1)]),
        ItensCardapio(id=2, nome="Coca-Cola", preco=5.0, categoria="Bebida", ingredientes=[]),
        ItensCardapio(id=3, nome="Batata Frita", preco=7.0, categoria="Acompanhamento", ingredientes=[]),
        ItensCardapio(id=4, nome="Sorvete", preco=4.0, categoria="Sobremesa", ingredientes=[]),
        ]

class ItensCardapioDAO(GenericDAO):
    def pegar_maior_id(self) -> int:
            pk = 0
            if not itens_cardapio_mock:
                return pk
            
            for itens_cardapio in itens_cardapio_mock:
                if itens_cardapio.id is None:
                    raise ValueError("itens_cardapio ID não pode ser None")
                if itens_cardapio.id > pk:
                    pk = itens_cardapio.id
            return pk
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
