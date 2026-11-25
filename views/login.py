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
        self.label_usuario = tk.Label(self, text="Usuário:")
        self.label_usuario.pack(pady=5)

        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        self.label_senha = tk.Label(self, text="Senha:")
        self.label_senha.pack(pady=5)

        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack(pady=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=5)

        self.botao_login = tk.Button(self, text="Login", command=self.verificar_login)
        self.botao_login.pack(pady=10)

        self.botao_registrar = tk.Button(self, text="Registrar", command=self.abrir_registro)
        self.botao_registrar.pack(pady=10)

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
        tk.Label(self, text="Criar conta", font=("Segoe UI", 16, "bold")).pack(pady=(10, 4))
        tk.Label(self, text="Preencha os dados para se cadastrar.").pack(pady=(0, 10))

        # rodape empacotado antes para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Registrar", command=self.registrar_cliente).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.voltar).pack(side="left", padx=5)

        form = tk.Frame(self)
        form.pack(pady=5)

        campos = [
            ("Nome:", "entry_nome", ""),
            ("CPF:", "entry_cpf", ""),
            ("Telefone:", "entry_telefone", ""),
            ("Senha:", "entry_senha", "*"),
        ]
        for linha, (rotulo, atributo, mascara) in enumerate(campos):
            tk.Label(form, text=rotulo).grid(row=linha, column=0, sticky="e", padx=3, pady=4)
            entry = tk.Entry(form, width=28, show=mascara)
            entry.grid(row=linha, column=1, pady=4)
            entry.bind("<Return>", lambda e: self.registrar_cliente())
            setattr(self, atributo, entry)

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