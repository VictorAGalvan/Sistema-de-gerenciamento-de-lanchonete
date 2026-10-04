import tkinter as tk
from controler.pedido_controler import PedidoControler
from models.EstadoPedido import Pronto


class Pedidos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pedido_controler = PedidoControler()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Pedidos realizados:").pack(pady=5)

        for pedido in self.pedido_controler.listar_nao_finalizados():
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
                command=lambda p=pedido: self.app.mostrar(DetalhesPedido, pedido=p)
            ).pack(side="left")

        tk.Button(self, text="Voltar", command=self.app.voltar_menu).pack(pady=10)

    def avancar_pedido(self, pedido, label_estado, botao):
        self.pedido_controler.avancar_pedido(pedido)
        label_estado.config(text=str(pedido.estado))
        if isinstance(pedido.estado, Pronto):
            botao.destroy()


class DetalhesPedido(tk.Frame):
    def __init__(self, parent, app, pedido):
        super().__init__(parent)
        self.app = app
        self.pedido = pedido
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Pedido #{self.pedido.id}").pack(pady=5)
        tk.Label(self, text=f"Estado: {self.pedido.estado}").pack(pady=5)

        for item in self.pedido.itens_pedidos:
            tk.Label(self, text=f"{item.quantidade}x {item.nome} - R${item.preco:.2f}").pack(anchor="w", padx=5)

        tk.Button(self, text="Voltar", command=lambda: self.app.mostrar(Pedidos)).pack(pady=10)


class MeuPedido(tk.Frame):
    def __init__(self, parent, app, cliente):
        super().__init__(parent)
        self.app = app
        self.pedido_controler = PedidoControler()
        self.cliente = cliente
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Meus pedidos:").pack(pady=5)

        for pedido in self.pedido_controler.listar_por_cliente(self.cliente.id):
            tk.Label(self, text=f"Pedido #{pedido.id} - {pedido.estado}").pack(pady=5)
            for item in pedido.itens_pedidos:
                tk.Label(self, text=f"{item.quantidade}x {item.nome}").pack(anchor="w", padx=5)

        tk.Button(self, text="Voltar", command=self.app.voltar_menu).pack(pady=10)