class AppController:
    def __init__(self):
        self.cliente = None
        self.eh_admin = False

    def iniciar_sessao_admin(self):
        self.cliente = None
        self.eh_admin = True

    def iniciar_sessao_cliente(self, cliente):
        self.cliente = cliente
        self.eh_admin = False

    def encerrar_sessao(self):
        self.cliente = None
        self.eh_admin = False
