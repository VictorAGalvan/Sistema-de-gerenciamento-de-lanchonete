import tkinter as tk
from dao import cliente_dao
from views.cardapio import Cardapio

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.dao_cliente = cliente_dao.ClienteDAO()
        self.cliente = None
        self.create_widgets()

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
        self.botao_login = tk.Button(self, text="Registrar", command=self.abrir_registro)
        self.botao_login.pack(pady=10)


    def abrir_registro(self):
        Registrar()
    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "admin" and senha == "admin":
            print("Login bem-sucedido!")
            self.master.abrir_sistema_admin()  

            #print("A janela do cardápio foi fechada.")
        else:
            cliente = self.dao_cliente.selecionar_por_nome(usuario)
            if cliente.senha == senha:
                print("Login bem-sucedido!")
                self.cliente = cliente
                self.master.abrir_sistema_usuario()
            else:
                self.label_erro.config(text="Usuário ou senha incorretos.")

class Registrar(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar")
        self.geometry("300x200")
        self.dao_cliente = cliente_dao.ClienteDAO()
        self.create_widgets()
    def create_widgets(self):
        self.label_nome = tk.Label(self, text="Nome:")
        self.label_nome.pack(pady=5)

        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)

        self.label_cpf = tk.Label(self, text="CPF:")
        self.label_cpf.pack(pady=5)

        self.entry_cpf = tk.Entry(self)
        self.entry_cpf.pack(pady=5)

        self.label_telefone = tk.Label(self, text="Telefone:")
        self.label_telefone.pack(pady=5)

        self.entry_telefone = tk.Entry(self)
        self.entry_telefone.pack(pady=5)

        self.label_senha = tk.Label(self, text="Senha:")
        self.label_senha.pack(pady=5)

        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack(pady=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=5)

        self.botao_registrar = tk.Button(self, text="Registrar", command=self.registrar_cliente)
        self.botao_registrar.pack(pady=10)

    def registrar_cliente(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        cpf = self.entry_cpf.get()
        telefone = self.entry_telefone.get()
        if not nome or not senha:
            self.label_erro.config(text="Nome e senha são obrigatórios.")
            return

        cliente_existente = self.dao_cliente.selecionar_por_nome(nome)
        if cliente_existente:
            self.label_erro.config(text="Nome de usuário já existe.")
            return

        novo_cliente = cliente_dao.Cliente(id=self.dao_cliente.pegar_maior_id() + 1, nome=nome, senha=senha,cpf=cpf,telefone=telefone)
        self.dao_cliente.insert(novo_cliente)
        self.destroy()