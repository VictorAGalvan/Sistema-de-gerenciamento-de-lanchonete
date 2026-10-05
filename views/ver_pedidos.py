import tkinter as tk
from controler.pedido_controler import PedidoControler
from models.EstadoPedido import Pronto
from views.tabela import Tabela


class Pedidos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pedido_controler = PedidoControler()
        self.pedidos_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Pedidos realizados:").pack(pady=5)

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Avançar", command=self.avancar_pedido).pack(side="left", padx=5)
        tk.Button(botoes, text="Detalhes", command=self.abrir_detalhes).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.app.voltar_menu).pack(side="left", padx=5)

        self.tabela = Tabela(self, [
            ("id", "Pedido", 70),
            ("total", "Total", 100),
            ("estado", "Estado", 150),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)

        for pedido in self.pedido_controler.listar_nao_finalizados():
            iid = str(pedido.id)
            self.pedidos_por_iid[iid] = pedido
            total = sum(ip.preco * ip.quantidade for ip in pedido.itens_pedidos)
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(f"#{pedido.id}", f"R${total:.2f}", str(pedido.estado))
            )

    def _pedido_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um pedido na lista.")
            return None, None
        self.label_erro.config(text="")
        return iid, self.pedidos_por_iid[iid]

    def avancar_pedido(self):
        iid, pedido = self._pedido_selecionado()
        if pedido is None:
            return
        if isinstance(pedido.estado, Pronto):
            self.label_erro.config(text="Este pedido já está pronto.")
            return

        self.pedido_controler.avancar_pedido(pedido)
        self.tabela.tree.set(iid, "estado", str(pedido.estado))

    def abrir_detalhes(self):
        iid, pedido = self._pedido_selecionado()
        if pedido is None:
            return
        self.app.mostrar(DetalhesPedido, pedido=pedido)


class DetalhesPedido(tk.Frame):
    def __init__(self, parent, app, pedido):
        super().__init__(parent)
        self.app = app
        self.pedido = pedido
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Pedido #{self.pedido.id}").pack(pady=5)
        tk.Label(self, text=f"Estado: {self.pedido.estado}").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")
        tk.Button(rodape, text="Voltar", command=lambda: self.app.mostrar(Pedidos)).pack(pady=10)

        self.tabela = Tabela(self, [
            ("qtd", "Qtd", 50),
            ("item", "Item", 200),
            ("preco", "Preço", 80),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)

        for item in self.pedido.itens_pedidos:
            self.tabela.tree.insert(
                "", "end",
                values=(item.quantidade, item.nome, f"R${item.preco:.2f}")
            )


class MeuPedido(tk.Frame):
    def __init__(self, parent, app, cliente):
        super().__init__(parent)
        self.app = app
        self.pedido_controler = PedidoControler()
        self.cliente = cliente
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Meus pedidos:").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")
        tk.Button(rodape, text="Voltar", command=self.app.voltar_menu).pack(pady=10)

        self.tabela = Tabela(self, [
            ("pedido", "Pedido", 70),
            ("estado", "Estado", 110),
            ("qtd", "Qtd", 50),
            ("item", "Item", 180),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)

        # uma linha por item; o número e o estado do pedido se repetem
        for pedido in self.pedido_controler.listar_por_cliente(self.cliente.id):
            for item in pedido.itens_pedidos:
                self.tabela.tree.insert(
                    "", "end",
                    values=(f"#{pedido.id}", str(pedido.estado), item.quantidade, item.nome)
                )