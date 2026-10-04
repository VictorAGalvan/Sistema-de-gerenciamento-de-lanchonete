import tkinter as tk
from views.login import LoginFrame
from views.cardapio_view import Cardapio
from views.ver_pedidos import MeuPedido, Pedidos
from views.editar_cardapio import ListaCardapios
class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pedidos")
        self.geometry("500x500")
        self.cliente = None
        self.eh_admin = False

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frame_atual = None
        self.mostrar(LoginFrame)

    def mostrar(self, classe_frame, **kwargs):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
        self.frame_atual = classe_frame(self.container, self, **kwargs)
        self.frame_atual.pack(fill="both", expand=True)

    def abrir_sistema_admin(self):
        self.eh_admin = True
        self.mostrar(MenuAdmin)

    def abrir_sistema_usuario(self):
        self.cliente = self.frame_atual.cliente
        self.eh_admin = False
        self.mostrar(MenuUsuario)

    def voltar_menu(self):
        self.mostrar(MenuAdmin if self.eh_admin else MenuUsuario)
    def voltar_menu(self):
        self.mostrar(MenuAdmin if self.eh_admin else MenuUsuario)

    def sair(self):
        self.cliente = None
        self.eh_admin = False
        self.mostrar(LoginFrame)


class MenuAdmin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Button(self, text="Ver pedidos", command=lambda: app.mostrar(Pedidos)).pack(pady=10)
        tk.Button(self, text="Ver cardápio", command=lambda: app.mostrar(Cardapio)).pack(pady=10)
        tk.Button(self, text="Editar cardápio", command=lambda: app.mostrar(ListaCardapios)).pack(pady=10)
        tk.Button(self, text="Sair", command=app.sair).pack(pady=10)


class MenuUsuario(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Button(self, text="Ver cardápio",
                  command=lambda: app.mostrar(Cardapio, cliente=app.cliente)).pack(pady=10)
        tk.Button(self, text="Meu pedido",
                  command=lambda: app.mostrar(MeuPedido, cliente=app.cliente)).pack(pady=10)
        tk.Button(self, text="Sair", command=app.sair).pack(pady=10)

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()