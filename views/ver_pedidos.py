import tkinter as tk
from dao.pedido_dao import PedidoDAO
from models.EstadoPedido import Pronto


class Pedidos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pedidos")
        self.geometry("400x300")
        self.dao_pedido = PedidoDAO()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Pedidos realizados:")
        self.label.pack(pady=5)

        for pedido in self.dao_pedido.select_todos():
            linha = tk.Frame(self)
            linha.pack(pady=5, fill="x")

            tk.Label(linha, text=f"Pedido #{pedido.id}").pack(side="left", padx=5)

            total = sum(ip.preco * ip.quantidade for ip in pedido.itens_pedidos)
            tk.Label(linha, text=f"Total: R${total:.2f}").pack(side="left", padx=5)

            label_estado = tk.Label(linha, text=str(pedido.estado))
            label_estado.pack(side="left", padx=5)

            tk.Button(
                linha, text="Avançar",
                command=lambda p=pedido, lbl=label_estado: self.avancar_pedido(p, lbl)
            ).pack(side="left")

    def avancar_pedido(self, pedido, label_estado):
        pedido.estado.avancar(pedido)
        label_estado.config(text=str(pedido.estado))