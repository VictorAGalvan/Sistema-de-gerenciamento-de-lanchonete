from dao.itens_cardapio_dao import ItensCardapioDAO
from models.Pedido import Pedido
from models.ItensPedido import ItensPedido
import tkinter as tk
class Cardapio(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cardápio")
        self.geometry("400x300")
        self.dao_itens = ItensCardapioDAO()
        self.pedido = Pedido(id=1, itens_pedidos=[])  # cliente/mesa depois
        self.create_widgets()

    def adicionar_ao_pedido(self, item_cardapio, label_contagem):
        item_pedido = next(
            (ip for ip in self.pedido.itens_pedidos if ip.id == item_cardapio.id),  # MUDOU: ip.item_cardapio.id -> ip.id
            None
        )
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)  # MUDOU: só passa item_cardapio e quantidade
            self.pedido.itens_pedidos.append(item_pedido)
        else:
            item_pedido.quantidade += 1
        label_contagem.config(text=str(item_pedido.quantidade))

    def remover_do_pedido(self, item_cardapio, label_contagem):
        item_pedido = next(
            (ip for ip in self.pedido.itens_pedidos if ip.id == item_cardapio.id),  # MUDOU: igual acima
            None
        )
        if item_pedido and item_pedido.quantidade > 0:
            item_pedido.quantidade -= 1
            label_contagem.config(text=str(item_pedido.quantidade))
            if item_pedido.quantidade == 0:
                self.pedido.itens_pedidos.remove(item_pedido)

    def create_widgets(self):
        self.label = tk.Label(self, text="Bem-vindo ao Cardápio!")
        self.label.pack(pady=5)

        for item in self.dao_itens.select_todos():
            linha = tk.Frame(self)
            linha.pack(pady=5, fill="x")

            tk.Label(linha, text=f"{item.nome} - R${item.preco:.2f} ({item.categoria})").pack(side="left", padx=5)

            contagem = tk.Label(linha, text="0")

            tk.Button(linha, text="+", command=lambda i=item, lbl=contagem: self.adicionar_ao_pedido(i, lbl)).pack(side="left")
            contagem.pack(side="left", padx=5)
            tk.Button(linha, text="-", command=lambda i=item, lbl=contagem: self.remover_do_pedido(i, lbl)).pack(side="left")

        botao_fazer_pedido = tk.Button(self, text="Fazer Pedido", command=self.fazer_pedido)
        botao_fazer_pedido.pack(pady=10)

    def fazer_pedido(self):
        print(f"Pedido #{self.pedido.id}")
        for item_pedido in self.pedido.itens_pedidos:
            print(f"  {item_pedido.quantidade}x {item_pedido.nome} - R${item_pedido.preco:.2f}")
        total = sum(ip.preco * ip.quantidade for ip in self.pedido.itens_pedidos)
        print(f"Total: R${total:.2f}")