import tkinter as tk
from tkinter import ttk

from controler.app_controller import AppController
from views.login import LoginFrame
from views.cardapio_view import Cardapio
from views.ver_pedidos import MeuPedido, Pedidos
from views.editar_cardapio import ListaCardapios
from views.ingredientes import ListaIngredientes
class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lanchonete")
        self.geometry("760x620")
        self.minsize(620, 480)
        self.configure(bg="#f3f5f7")
        self.option_add("*Font", ("Segoe UI", 10))
        self.option_add("*Background", "#f3f5f7")
        self.option_add("*Foreground", "#263238")
        self.option_add("*Button.Background", "#e5eaf0")
        self.option_add("*Button.ActiveBackground", "#d5e2dc")
        self.option_add("*Button.Relief", "flat")
        self.option_add("*Button.BorderWidth", 0)
        self.option_add("*Button.Padx", 12)
        self.option_add("*Button.Pady", 6)
        self.option_add("*Entry.Background", "#ffffff")
        self.option_add("*Entry.Relief", "solid")
        estilo = ttk.Style(self)
        estilo.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#263238",
            rowheight=28,
            borderwidth=0,
        )
        estilo.configure(
            "Treeview.Heading",
            background="#e5eaf0",
            foreground="#263238",
            font=("Segoe UI", 10, "bold"),
            padding=6,
        )
        estilo.map("Treeview", background=[("selected", "#cfe3d8")])
        self.controller = AppController()

        cabecalho = tk.Frame(self, bg="#31594b", padx=20, pady=12)
        cabecalho.pack(fill="x")
        tk.Label(
            cabecalho,
            text="LANCHONETE  |  SISTEMA DE PEDIDOS",
            bg="#31594b",
            fg="#ffffff",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")

        self.container = tk.Frame(self, padx=14, pady=14)
        self.container.pack(fill="both", expand=True)

        self.frame_atual = None
        self.mostrar(LoginFrame)

    def mostrar(self, classe_frame, **kwargs):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
        self.frame_atual = classe_frame(self.container, self, **kwargs)
        self.frame_atual.pack(fill="both", expand=True)

    def abrir_sistema_admin(self):
        self.controller.iniciar_sessao_admin()
        self.mostrar(MenuAdmin)

    def abrir_sistema_usuario(self):
        self.controller.iniciar_sessao_cliente(self.frame_atual.cliente)
        self.mostrar(MenuUsuario)

    def voltar_menu(self):
        self.mostrar(MenuAdmin if self.eh_admin else MenuUsuario)

    def sair(self):
        self.controller.encerrar_sessao()
        self.mostrar(LoginFrame)

    @property
    def cliente(self):
        return self.controller.cliente

    @property
    def eh_admin(self):
        return self.controller.eh_admin


class MenuAdmin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Label(self, text="Painel administrativo", font=("Segoe UI", 16, "bold")).pack(pady=(20, 12))
        tk.Button(self, text="Ver pedidos", command=lambda: app.mostrar(Pedidos)).pack(pady=6)
        tk.Button(self, text="Ver cardápio", command=lambda: app.mostrar(Cardapio)).pack(pady=6)
        tk.Button(self, text="Editar cardápio", command=lambda: app.mostrar(ListaCardapios)).pack(pady=6)
        tk.Button(self, text="Ingredientes e estoque", command=lambda: app.mostrar(ListaIngredientes)).pack(pady=6)
        tk.Button(self, text="Sair", command=app.sair).pack(pady=(18, 6))


class MenuUsuario(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Label(self, text="Bem-vindo!", font=("Segoe UI", 16, "bold")).pack(pady=(20, 12))
        tk.Button(
            self,
            text="Ver cardápio e montar pedido",
            command=lambda: app.mostrar(Cardapio, cliente=app.cliente),
        ).pack(pady=6)
        tk.Button(
            self,
            text="Meus pedidos",
            command=lambda: app.mostrar(MeuPedido, cliente=app.cliente),
        ).pack(pady=6)
        tk.Button(self, text="Sair", command=app.sair).pack(pady=(18, 6))

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()