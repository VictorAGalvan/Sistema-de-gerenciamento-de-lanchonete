from dao.generic_dao import GenericDAO
from models.Cliente import Cliente


cliente_mock:list[Cliente] = [
    Cliente(1, "Victor", "12345678900", "123456789", "senha123"),
]

class ClienteDAO(GenericDAO):
    def selecionar_por_nome(self, nome: str) -> Cliente | None:
        for cliente in cliente_mock:
            if cliente.nome == nome:
                return cliente
        return None
    def pegar_maior_id(self) -> int:
        pk = 0
        if not cliente_mock:
            return pk
        
        for cliente in cliente_mock:
            if cliente.id is None:
                raise ValueError("Cliente ID não pode ser None")
            if cliente.id > pk:
                pk = cliente.id
        return pk
    def insert(self, cliente: Cliente) -> None:
        cliente_mock.append(cliente)

    def select_por_id(self, cliente_id: int) -> Cliente | None:
        for cliente in cliente_mock:
            if cliente.id == cliente_id:
                return cliente
        return None

    def select_todos(self) -> list[Cliente]:
        return cliente_mock

    def delete(self, cliente_id: int) -> None:
        for i in cliente_mock:
            if i.id == cliente_id:
                cliente_mock.remove(i)
                break

    def update(self, cliente: Cliente) -> None:
        for i in cliente_mock:
            if cliente == i:
                cliente_mock.remove(i)
                cliente_mock.append(cliente)
                break

