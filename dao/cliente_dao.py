from models.Cliente import Cliente


cliente_mock: list[Cliente] = [
    Cliente(1, "Victor", "12345678900", "123456789", "senha123"),
]


class ClienteDAO:
    def _pegar_maior_id(self) -> int:
        pk = 0
        for cliente in cliente_mock:
            if cliente.id > pk:
                pk = cliente.id
        return pk

    def select(self) -> list[Cliente]:
        return cliente_mock

    def selectID(self, id: int) -> Cliente | None:
        for cliente in cliente_mock:
            if cliente.id == id:
                return cliente
        return None

    def selectNome(self, nome: str) -> Cliente | None:
        for cliente in cliente_mock:
            if cliente.nome == nome:
                return cliente
        return None

    def insert(self, cliente: Cliente) -> None:
        cliente.id = self._pegar_maior_id() + 1
        cliente_mock.append(cliente)

    def update(self, cliente: Cliente) -> None:
        pass

    def delete(self, cliente: Cliente) -> None:
        cliente_mock.remove(cliente)