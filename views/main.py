import tkinter as tk
from views.login import LoginFrame
from views.cardapio_view import Cardapio
from views.ver_pedidos import MeuPedido, Pedidos
from views.editar_cardapio import ListaCardapios
class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pedidos")
        self.geometry("400x300")
        self.login_frame = LoginFrame(self)

    def abrir_sistema_admin(self):

        self.login_frame.destroy()

        self.ver_pedido = tk.Button(self, text="Ver pedidos", command=self.abrir_pedidos)
        self.ver_pedido.pack(pady=10)

        self.ver_cardapio = tk.Button(self, text="Ver cardápio", command=self.abrir_cardapio)
        self.ver_cardapio.pack(pady=10)

        self.editar_cardapio = tk.Button(self, text="Editar cardápio",command=self.abrir_editar_cardapio)
        self.editar_cardapio.pack(pady=10)

    def abrir_sistema_usuario(self):
        self.cliente = self.login_frame.cliente
        self.login_frame.destroy()
        self.ver_cardapio = tk.Button(self, text="Ver cardápio", command=self.abrir_cardapio_cliente)
        self.ver_cardapio.pack(pady=10)
        self.meu_pedido = tk.Button(self, text="Meu pedido", command=self.abrir_meu_pedido)
        self.meu_pedido.pack(pady=10)

    def abrir_cardapio(self):
        Cardapio(self)

    def abrir_cardapio_cliente(self):
        Cardapio(self,cliente=self.cliente)

    def abrir_pedidos(self):
        Pedidos(self)

    def abrir_editar_cardapio(self):
        ListaCardapios(self)

    def abrir_meu_pedido(self):
        MeuPedido(cliente=self.cliente,master=self)

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()