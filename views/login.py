import tkinter as tk
from controler.login_controller import LoginController


class LoginFrame(tk.Frame):
    def __init__(self, parent, app, mensagem=None):
        super().__init__(parent)
        self.app = app
        self.controller = LoginController()
        self.cliente = None
        self.create_widgets()
        if mensagem:
            self.label_erro.config(text=mensagem, fg="green")

    def create_widgets(self):
        card = tk.Frame(self, highlightbackground="#cfd8dc", highlightthickness=1, padx=44, pady=30)
        card.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(card, text="Entrar", font=("Segoe UI", 20, "bold")).pack()
        tk.Label(card, text="Acesse sua conta para continuar", fg="#607d8b").pack(pady=(0, 16))

        tk.Label(card, text="Usuário").pack(anchor="w")
        self.entry_usuario = tk.Entry(card, width=30, font=("Segoe UI", 11))
        self.entry_usuario.pack(pady=(2, 10), ipady=4)

        tk.Label(card, text="Senha").pack(anchor="w")
        self.entry_senha = tk.Entry(card, width=30, show="*", font=("Segoe UI", 11))
        self.entry_senha.pack(pady=(2, 6), ipady=4)

        self.label_erro = tk.Label(card, text="", fg="red")
        self.label_erro.pack(pady=4)

        self.botao_login = tk.Button(card, text="Login", name="principal", width=24, command=self.verificar_login)
        self.botao_login.pack(pady=(6, 6))

        self.botao_registrar = tk.Button(card, text="Criar conta", name="secundario", width=36, command=self.abrir_registro)
        self.botao_registrar.pack()

        # Enter faz login; cursor ja começa no campo de usuario
        self.entry_usuario.bind("<Return>", lambda e: self.verificar_login())
        self.entry_senha.bind("<Return>", lambda e: self.verificar_login())
        self.entry_usuario.focus_set()

    def abrir_registro(self):
        self.app.mostrar(Registrar)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        cliente, perfil = self.controller.autenticar(usuario, senha)
        self.label_erro.config(text="", fg="red")
        if perfil == "admin":
            self.app.abrir_sistema_admin()
            return

        if perfil == "usuario":
            self.cliente = cliente
            self.app.abrir_sistema_usuario()
        else:
            self.label_erro.config(text="Usuário ou senha incorretos.")


class Registrar(tk.Frame):
    """Tela de cadastro de cliente (mesmo padrao das outras telas)."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = LoginController()
        self.create_widgets()

    def create_widgets(self):
        card = tk.Frame(self, highlightbackground="#cfd8dc", highlightthickness=1, padx=44, pady=30)
        card.place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(card, text="Criar conta", font=("Segoe UI", 20, "bold")).pack(pady=(0, 2))
        tk.Label(card, text="Preencha os dados para se cadastrar.", fg="#607d8b").pack(pady=(0, 12))

        form = tk.Frame(card)
        form.pack()

        campos = [
            ("Nome:", "entry_nome", ""),
            ("CPF:", "entry_cpf", ""),
            ("Telefone:", "entry_telefone", ""),
            ("Senha:", "entry_senha", "*"),
        ]
        for linha, (rotulo, atributo, mascara) in enumerate(campos):
            tk.Label(form, text=rotulo).grid(row=linha, column=0, sticky="e", padx=(0, 8), pady=6)
            entry = tk.Entry(form, width=28, show=mascara, font=("Segoe UI", 11))
            entry.grid(row=linha, column=1, pady=6, ipady=4)
            entry.bind("<Return>", lambda e: self.registrar_cliente())
            setattr(self, atributo, entry)

        self.label_erro = tk.Label(card, text="", fg="red")
        self.label_erro.pack(pady=4)

        botoes = tk.Frame(card)
        botoes.pack(pady=(6, 0))
        tk.Button(botoes, text="Voltar", name="secundario", width=14, command=self.voltar).pack(side="left", padx=5)
        tk.Button(botoes, text="Registrar", name="principal", width=12, command=self.registrar_cliente).pack(side="left", padx=5)

        self.entry_nome.focus_set()

    def voltar(self):
        self.app.mostrar(LoginFrame)

    def registrar_cliente(self):
        erro = self.controller.registrar(
            self.entry_nome.get(),
            self.entry_senha.get(),
            self.entry_cpf.get(),
            self.entry_telefone.get(),
        )
        if erro:
            self.label_erro.config(text=erro)
            return
        self.app.mostrar(LoginFrame, mensagem="Cadastro realizado! Faça login.")