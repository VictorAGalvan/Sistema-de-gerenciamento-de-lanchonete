from models.EstadoPedido import Pronto
from models.Pedido import Pedido


pedido_mock: list[Pedido] = []


class PedidoDAO:
    def _pegar_maior_id(self) -> int:
        pk = 0
        for pedido in pedido_mock:
            if pedido.id > pk:
                pk = pedido.id
        return pk

    def select(self) -> list[Pedido]:
        return pedido_mock

    def selectID(self, id: int) -> Pedido | None:
        for pedido in pedido_mock:
            if pedido.id == id:
                return pedido
        return None

    def select_nao_finalizados(self) -> list[Pedido]:
        return [p for p in pedido_mock if not isinstance(p.estado, Pronto)]

    def select_por_cliente(self, id_cliente: int) -> list[Pedido]:
        return [p for p in pedido_mock if getattr(p, "cliente", None) is not None and p.cliente.id == id_cliente]

    def insert(self, pedido: Pedido) -> None:
        pedido.id = self._pegar_maior_id() + 1
        pedido_mock.append(pedido)

    def update(self, pedido: Pedido) -> None:
        pass

    def delete(self, pedido: Pedido) -> None:
        pedido_mock.remove(pedido)

    # junção pedido <-> itens_pedidos — no mock já ficam em pedido.itens_pedidos
    def insertItemPedido(self, id_pedido: int, id_item_pedido: int) -> None:
        pass