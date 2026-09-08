import tkinter as tk
from views.cardapio import Cardapio

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
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

        self.botao_login = tk.Button(self, text="Login", command=self.verificar_login)
        self.botao_login.pack(pady=10)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "admin" and senha == "admin":
            print("Login bem-sucedido!")
            self.master.abrir_sistema_admin()  

            print("A janela do cardápio foi fechada.")
        elif usuario == "user" and senha == "user":
            print("Login bem-sucedido!")
            self.master.abrir_sistema_usuario() # Impede interação com a janela principal
            print("A janela do cardápio foi fechada.")

