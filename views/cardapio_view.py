import tkinter as tk
import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
from controler.cardapio_controler import CardapioController




class Cardapio(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cardápio")
        self.geometry("400x300")
        self.controller = CardapioController()
        self.create_widgets()

    def adicionar_ao_pedido(self, item):
        print(f"Item adicionado ao pedido: {item['nome']} - R${item['preco']:.2f}")

    def remover_do_pedido(self, item):
        print(f"Item removido do pedido: {item['nome']} - R${item['preco']:.2f}")
    def create_widgets(self):
        self.label = tk.Label(self, text="Bem-vindo ao Cardápio!")
        
        lanches = self.controler.listar_itens()
        for item in lanches["itens"]:
            item_label = tk.Label(self, text=f"{item["nome"]} - R${item["preco"]:.2f} ({item["categoria"]})")
            
            item_label.pack(pady=5)
            adicionar = tk.Button(self, text="+", command=lambda i=item: self.adicionar_ao_pedido(i))
            adicionar.pack(pady=5)
            remover = tk.Button(self, text="-", command=lambda i=item: self.remover_do_pedido(i))
            item_label.pack(pady=5)
            remover.pack(pady=5)
        