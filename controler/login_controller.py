from controler.cliente_controler import ClienteControler
from models.Cliente import Cliente


class LoginController:
    def __init__(self):
        self.clientes = ClienteControler()

    def autenticar(self, usuario, senha):
        if usuario == "admin" and senha == "admin":
            return None, "admin"

        cliente = self.clientes.buscar_cliente_por_nome(usuario)
        if cliente is not None and cliente.senha == senha:
            return cliente, "usuario"
        return None, None

    def registrar(self, nome, senha, cpf, telefone):
        if not nome or not senha:
            return "Nome e senha são obrigatórios."

        if self.clientes.buscar_cliente_por_nome(nome):
            return "Nome de usuário já existe."

        self.clientes.criar_cliente(
            Cliente(id=None, nome=nome, senha=senha, cpf=cpf, telefone=telefone)
        )
        return None
