from dao.cliente_dao import ClienteDAO


class ClienteControler:
    def __init__(self):
        self.dao = ClienteDAO()

    def listar_clientes(self):
        return self.dao.select()

    def buscar_cliente(self, id_cliente):
        return self.dao.selectID(id_cliente)

    def buscar_cliente_por_nome(self, nome):
        return self.dao.selectNome(nome)

    def criar_cliente(self, cliente):
        return self.dao.insert(cliente)

    def atualizar_cliente(self, cliente):
        return self.dao.update(cliente)

    def remover_cliente(self, cliente):
        return self.dao.delete(cliente)