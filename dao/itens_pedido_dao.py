from models.ItensPedido import ItensPedido


itens_pedido_mock: list[ItensPedido] = []


class ItensPedidoDAO:
    def _pegar_maior_id(self) -> int:
        pk = 0
        for item in itens_pedido_mock:
            if item.id > pk:
                pk = item.id
        return pk

    def select(self) -> list[ItensPedido]:
        return itens_pedido_mock

    def selectID(self, id: int) -> ItensPedido | None:
        for item in itens_pedido_mock:
            if item.id == id:
                return item
        return None

    def insert(self, item: ItensPedido) -> None:
        item.id = self._pegar_maior_id() + 1
        itens_pedido_mock.append(item)

    def update(self, item: ItensPedido) -> None:
        pass

    def delete(self, item: ItensPedido) -> None:
        itens_pedido_mock.remove(item)

    def insertIngrediente(self, id_item: int, id_ingrediente: int) -> None:
        pass

    def deleteIngredientes(self, id_item: int) -> None:
        pass