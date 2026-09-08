from dao.generic_dao import GenericDAO
from models.ItensPedido import ItensPedido

itens_pedido_mock:list[ItensPedido] = []

class ItensPedidoDAO(GenericDAO):
    def pegar_maior_id(self) -> int:
            pk = 0
            if not itens_pedido_mock:
                return pk
            
            for itens_pedido in itens_pedido_mock:
                if itens_pedido.id is None:
                    raise ValueError("itens_pedido ID não pode ser None")
                if itens_pedido.id > pk:
                    pk = itens_pedido.id
            return pk
    def insert(self, itens_pedido: ItensPedido) -> None:
        itens_pedido_mock.append(itens_pedido)

    def select_por_id(self, itens_pedido_id: int) -> ItensPedido | None:
        for itens_pedido in itens_pedido_mock:
            if itens_pedido.id == itens_pedido_id:
                return itens_pedido
        return None

    def select_todos(self) -> list[ItensPedido]:
        return itens_pedido_mock

    def delete(self, itens_pedido_id: int) -> None:
        for i in itens_pedido_mock:
            if i.id == itens_pedido_id:
                itens_pedido_mock.remove(i)
                break

    def update(self, itens_pedido: ItensPedido) -> None:
        for i in itens_pedido_mock:
            if itens_pedido == i:
                itens_pedido_mock.remove(i)
                itens_pedido_mock.append(itens_pedido)
                break
