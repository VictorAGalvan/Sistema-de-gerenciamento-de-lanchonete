from dao.generic_dao import GenericDAO
from models.Pedido  import Pedido


pedido_mock:list[Pedido] = []

class PedidoDAO(GenericDAO):
    def insert(self, pedido: Pedido) -> None:
        pedido_mock.append(pedido)

    def select_por_id(self, pedido_id: int) -> Pedido | None:
        for pedido in pedido_mock:
            if pedido.id == pedido_id:
                return pedido
        return None

    def select_todos(self) -> list[Pedido]:
        return pedido_mock

    def delete(self, pedido_id: int) -> None:
        for i in pedido_mock:
            if i.id == pedido_id:
                pedido_mock.remove(i)
                break

    def update(self, pedido: Pedido) -> None:
        for i in pedido_mock:
            if pedido == i:
                pedido_mock.remove(i)
                pedido_mock.append(pedido)
                break
