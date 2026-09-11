import tkinter as tk
from views.login import LoginFrame
from views.cardapio import Cardapio
from views.ver_pedidos import Pedidos

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

        self.editar_cardapio = tk.Label(self, text="Editar cardápio")
        self.editar_cardapio.pack(pady=10)

    def abrir_sistema_usuario(self):
        self.login_frame.destroy()
        self.fazer_pedido = tk.Label(self, text="Fazer pedido")
        self.fazer_pedido.pack(pady=10)

        self.ver_cardapio = tk.Button(self, text="Ver cardápio", command=self.abrir_cardapio)
        self.ver_cardapio.pack(pady=10)

    def abrir_cardapio(self):
        Cardapio(self)

    def abrir_pedidos(self):
        Pedidos(self)


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()