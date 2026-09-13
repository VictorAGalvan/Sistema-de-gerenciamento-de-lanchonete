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

        for pedido in self.dao_pedido.select_nao_finalizados():
            linha = tk.Frame(self)
            linha.pack(pady=5, fill="x")

            tk.Label(linha, text=f"Pedido #{pedido.id}").pack(side="left", padx=5)

            total = sum(ip.preco * ip.quantidade for ip in pedido.itens_pedidos)
            tk.Label(linha, text=f"Total: R${total:.2f}").pack(side="left", padx=5)

            label_estado = tk.Label(linha, text=str(pedido.estado))
            label_estado.pack(side="left", padx=5)

            botao_avancar = tk.Button(linha, text="Avançar")
            botao_avancar.config(
                command=lambda p=pedido, lbl=label_estado, btn=botao_avancar: self.avancar_pedido(p, lbl, btn)
            )
            botao_avancar.pack(side="left")

            tk.Button(
                linha, text="Detalhes",
                command=lambda p=pedido: DetalhesPedido(p, master=self)
            ).pack(side="left")

    def avancar_pedido(self, pedido, label_estado, botao):
        pedido.estado.avancar(pedido)
        label_estado.config(text=str(pedido.estado))
        if isinstance(pedido.estado, Pronto):
            botao.destroy()


class DetalhesPedido(tk.Toplevel):
    def __init__(self, pedido, master=None):
        super().__init__(master)
        self.title(f"Detalhes do Pedido #{pedido.id}")
        self.geometry("300x300")
        self.pedido = pedido
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Pedido #{self.pedido.id}").pack(pady=5)
        tk.Label(self, text=f"Estado: {self.pedido.estado}").pack(pady=5)

        for item in self.pedido.itens_pedidos:
            tk.Label(self, text=f"{item.quantidade}x {item.nome} - R${item.preco:.2f}").pack(anchor="w", padx=5)


class MeuPedido(tk.Toplevel):
    def __init__(self, cliente, master=None):
        super().__init__(master)
        self.title("Meu Pedido")
        self.geometry("300x300")
        self.dao_pedido = PedidoDAO()
        self.cliente = cliente
        self.create_widgets()

    def create_widgets(self):
        for pedido in self.dao_pedido.select_por_cliente(self.cliente.id):
            tk.Label(self, text=f"Pedido #{pedido.id} - {pedido.estado}").pack(pady=5)
            for item in pedido.itens_pedidos:
                tk.Label(self, text=f"{item.quantidade}x {item.nome}").pack(anchor="w", padx=5)