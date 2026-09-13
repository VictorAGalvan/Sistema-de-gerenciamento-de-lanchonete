from dao.generic_dao import GenericDAO
from models.EstadoPedido import Pronto
from models.Pedido  import Pedido


pedido_mock:list[Pedido] = []

class PedidoDAO(GenericDAO):
    def select_nao_finalizados(self) -> list[Pedido]:
        pedidos_nao_finalizados = []
        for pedido in pedido_mock:
            if not isinstance(pedido.estado, Pronto):
                pedidos_nao_finalizados.append(pedido)
        return pedidos_nao_finalizados
    def select_por_cliente(self, cliente_id: int) -> list[Pedido]:
        pedidos_do_cliente = []
        for pedido in pedido_mock:
            if pedido.cliente is not None and pedido.cliente.id == cliente_id:
                pedidos_do_cliente.append(pedido)
        return pedidos_do_cliente
    def pegar_maior_id(self) -> int:
            pk = 0
            if not pedido_mock:
                return pk
            
            for pedido in pedido_mock:
                if pedido.id is None:
                    raise ValueError("pedido ID não pode ser None")
                if pedido.id > pk:
                    pk = pedido.id
            return pk
    def insert(self, pedido: Pedido) -> None:
        pedido_mock.append(pedido)
    def select_nao_finalizados(self) -> list[Pedido]:
        return [p for p in pedido_mock if not isinstance(p.estado, Pronto)]
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
