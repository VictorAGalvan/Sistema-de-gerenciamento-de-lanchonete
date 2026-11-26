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

        # botao padrao (verde)
        self.option_add("*Button.Background", "#31594b")
        self.option_add("*Button.Foreground", "#ffffff")
        self.option_add("*Button.ActiveBackground", "#264539")
        self.option_add("*Button.ActiveForeground", "#ffffff")
        self.option_add("*Button.Font", ("Segoe UI", 10, "bold"))
        self.option_add("*Button.Relief", "flat")
        self.option_add("*Button.BorderWidth", 0)
        self.option_add("*Button.Cursor", "hand2")
        self.option_add("*Button.Padx", 16)
        self.option_add("*Button.Pady", 7)
        # botoes secundarios (cinza): tk.Button(..., name="secundario")
        for nome in ("secundario", "secundario2", "secundario3"):
            self.option_add(f"*{nome}.Background", "#e5eaf0", 100)
            self.option_add(f"*{nome}.Foreground", "#263238", 100)
            self.option_add(f"*{nome}.ActiveBackground", "#cfd8dc", 100)
            self.option_add(f"*{nome}.ActiveForeground", "#263238", 100)
            self.option_add(f"*{nome}.Font", ("Segoe UI", 10), 100)
        # botao de perigo (vermelho): tk.Button(..., name="perigo")
        self.option_add("*perigo.Background", "#c62828", 100)
        self.option_add("*perigo.Foreground", "#ffffff", 100)
        self.option_add("*perigo.ActiveBackground", "#9e1f1f", 100)
        self.option_add("*perigo.ActiveForeground", "#ffffff", 100)

        # botao de destaque (acao principal da tela): tk.Button(..., name="principal")
        self.option_add("*principal.Font", ("Segoe UI", 11, "bold"), 100)
        self.option_add("*principal.Padx", 28, 100)
        self.option_add("*principal.Pady", 10, 100)
        # botao "Sair" do cabecalho
        self.option_add("*sair.Background", "#264539", 100)
        self.option_add("*sair.Foreground", "#ffffff", 100)
        self.option_add("*sair.ActiveBackground", "#1f382f", 100)
        self.option_add("*sair.ActiveForeground", "#ffffff", 100)
        self.option_add("*sair.Font", ("Segoe UI", 10), 100)
        self.option_add("*sair.Padx", 14, 100)
        self.option_add("*sair.Pady", 5, 100)

        self.option_add("*Entry.Background", "#ffffff")
        self.option_add("*Entry.Relief", "flat")
        self.option_add("*Entry.HighlightThickness", 1)
        self.option_add("*Entry.HighlightBackground", "#cfd8dc")
        self.option_add("*Entry.HighlightColor", "#31594b")

        # efeito ao passar o mouse (add="+" mantem o comportamento padrao do botao)
        self.bind_class("Button", "<Enter>", lambda e: self._hover(e, True), add="+")
        self.bind_class("Button", "<Leave>", lambda e: self._hover(e, False), add="+")

        estilo = ttk.Style(self)
        estilo.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#263238",
            rowheight=30,
            borderwidth=0,
        )
        estilo.configure(
            "Treeview.Heading",
            background="#e5eaf0",
            foreground="#263238",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            relief="flat",
        )
        estilo.map("Treeview", background=[("selected", "#cfe3d8")], foreground=[("selected", "#263238")])
        self.controller = AppController()

        cabecalho = tk.Frame(self, bg="#31594b", padx=20, pady=10)
        cabecalho.pack(fill="x")
        tk.Label(
            cabecalho,
            text="🍔  LANCHONETE",
            bg="#31594b",
            fg="#ffffff",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")
        tk.Label(
            cabecalho,
            text="  Sistema de pedidos",
            bg="#31594b",
            fg="#b7d3c7",
        ).pack(side="left", pady=(4, 0))
        # area da sessao (aparece so depois do login)
        self.btn_sair = tk.Button(cabecalho, text="Sair", name="sair", command=self.sair)
        self.lbl_sessao = tk.Label(cabecalho, text="", bg="#31594b", fg="#ffffff", font=("Segoe UI", 10, "bold"))

        self.container = tk.Frame(self, padx=14, pady=14)
        self.container.pack(fill="both", expand=True)

        self.frame_atual = None
        self.mostrar(LoginFrame)

    def _hover(self, evento, entrou):
        botao = evento.widget
        if str(botao.cget("state")) != "normal":
            return
        if entrou:
            botao._cor_original = botao.cget("bg")
            hover = {"#31594b": "#3f7260", "#e5eaf0": "#d5dde6", "#c62828": "#e53935", "#264539": "#1f382f"}
            botao.config(bg=hover.get(botao._cor_original, botao._cor_original))
        else:
            botao.config(bg=getattr(botao, "_cor_original", botao.cget("bg")))

    def mostrar(self, classe_frame, **kwargs):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
        self.frame_atual = classe_frame(self.container, self, **kwargs)
        self.frame_atual.pack(fill="both", expand=True)

    def _mostrar_sessao(self, nome):
        self.lbl_sessao.config(text=f"👤  {nome}")
        self.btn_sair.pack(side="right")
        self.lbl_sessao.pack(side="right", padx=(0, 14))

    def _ocultar_sessao(self):
        self.btn_sair.pack_forget()
        self.lbl_sessao.pack_forget()

    def abrir_sistema_admin(self):
        self.controller.iniciar_sessao_admin()
        self._mostrar_sessao("Administrador")
        self.mostrar(MenuAdmin)

    def abrir_sistema_usuario(self):
        self.controller.iniciar_sessao_cliente(self.frame_atual.cliente)
        self._mostrar_sessao(getattr(self.cliente, "nome", "Cliente"))
        self.mostrar(MenuUsuario)

    def voltar_menu(self):
        self.mostrar(MenuAdmin if self.eh_admin else MenuUsuario)

    def sair(self):
        self.controller.encerrar_sessao()
        self._ocultar_sessao()
        self.mostrar(LoginFrame)

    @property
    def cliente(self):
        return self.controller.cliente

    @property
    def eh_admin(self):
        return self.controller.eh_admin


def criar_tile(pai, icone, titulo, descricao, comando):
    """Cartao clicavel usado nos menus (icone + titulo + descricao)."""
    branco, hover = "#ffffff", "#eef5f1"
    tile = tk.Frame(pai, bg=branco, highlightbackground="#cfd8dc", highlightthickness=1,
                    cursor="hand2", padx=18, pady=14)
    lbl_icone = tk.Label(tile, text=icone, font=("Segoe UI Emoji", 22), bg=branco, cursor="hand2")
    lbl_icone.grid(row=0, column=0, rowspan=2, padx=(0, 14))
    lbl_titulo = tk.Label(tile, text=titulo, font=("Segoe UI", 12, "bold"), fg="#31594b",
                          bg=branco, anchor="w", width=22, cursor="hand2")
    lbl_titulo.grid(row=0, column=1, sticky="w")
    lbl_desc = tk.Label(tile, text=descricao, fg="#607d8b", bg=branco, anchor="w", width=28, cursor="hand2")
    lbl_desc.grid(row=1, column=1, sticky="w")
    partes = (tile, lbl_icone, lbl_titulo, lbl_desc)

    def entrar(_evento):
        for parte in partes:
            parte.config(bg=hover)
        tile.config(highlightbackground="#31594b")

    def sair(_evento):
        for parte in partes:
            parte.config(bg=branco)
        tile.config(highlightbackground="#cfd8dc")

    for parte in partes:
        parte.bind("<Enter>", entrar)
        parte.bind("<Leave>", sair)
        parte.bind("<Button-1>", lambda _evento: comando())
    return tile


class MenuAdmin(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        grade = tk.Frame(self)
        grade.place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(grade, text="Painel administrativo", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8)
        tk.Label(grade, text="O que você quer fazer?", fg="#607d8b").grid(
            row=1, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 10))
        opcoes = [
            ("📋", "Pedidos", "Acompanhe e avance os pedidos", Pedidos),
            ("🍽", "Ver cardápio", "Veja o cardápio ativo", Cardapio),
            ("✏", "Editar cardápio", "Itens, preços e receitas", ListaCardapios),
            ("📦", "Estoque", "Ingredientes e reposição", ListaIngredientes),
        ]
        for i, (icone, titulo, desc, destino) in enumerate(opcoes):
            criar_tile(grade, icone, titulo, desc, lambda d=destino: app.mostrar(d)).grid(
                row=2 + i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")


class MenuUsuario(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        nome = getattr(app.cliente, "nome", "") or ""
        grade = tk.Frame(self)
        grade.place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(grade, text=f"Olá, {nome.split(' ')[0]}!" if nome else "Bem-vindo!", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8)
        tk.Label(grade, text="O que você quer fazer?", fg="#607d8b").grid(
            row=1, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 10))
        criar_tile(grade, "🍔", "Fazer pedido", "Veja o cardápio e monte seu pedido",
                   lambda: app.mostrar(Cardapio, cliente=app.cliente)).grid(row=2, column=0, padx=8, pady=8, sticky="nsew")
        criar_tile(grade, "🧾", "Meus pedidos", "Acompanhe seus pedidos",
                   lambda: app.mostrar(MeuPedido, cliente=app.cliente)).grid(row=2, column=1, padx=8, pady=8, sticky="nsew")


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()