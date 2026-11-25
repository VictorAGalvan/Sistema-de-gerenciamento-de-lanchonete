import tkinter as tk
from controler.pedidos_view_controller import PedidosViewController
from views.tabela import Tabela


class Pedidos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = PedidosViewController()
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
            ("origem", "Mesa / Cliente", 150),
            ("total", "Total", 100),
            ("estado", "Estado", 150),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)

        for pedido in self.controller.listar_nao_finalizados():
            iid = str(pedido.id)
            self.pedidos_por_iid[iid] = pedido
            total = self.controller.calcular_total(pedido)
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(
                    f"#{pedido.id}",
                    self.controller.origem(pedido),
                    f"R${total:.2f}",
                    str(pedido.estado),
                )
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
        erro = self.controller.avancar_pedido(pedido)
        if erro:
            self.label_erro.config(text=erro)
            return
        self.tabela.tree.set(iid, "estado", str(pedido.estado))

    def abrir_detalhes(self):
        _, pedido = self._pedido_selecionado()
        if pedido is None:
            return
        self.app.mostrar(DetalhesPedido, pedido=pedido)


class DetalhesPedido(tk.Frame):
    def __init__(self, parent, app, pedido):
        super().__init__(parent)
        self.app = app
        self.pedido = pedido
        self.controller = PedidosViewController()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Pedido #{self.pedido.id}").pack(pady=5)
        tk.Label(self, text=f"Mesa / Cliente: {self.controller.origem(self.pedido)}").pack(pady=2)
        tk.Label(self, text=f"Estado: {self.pedido.estado}").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        botoes = tk.Frame(rodape)
        botoes.pack(pady=10)
        tk.Button(
            botoes, text="Ingredientes/Obs",
            command=lambda: self.app.mostrar(IngredientesPedido, pedido=self.pedido)
        ).pack(side="left", padx=5)
        tk.Button(
            botoes, text="Voltar",
            command=lambda: self.app.mostrar(Pedidos)
        ).pack(side="left", padx=5)

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
        self.controller = PedidosViewController()
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
        for pedido in self.controller.listar_por_cliente(self.cliente):
            for item in pedido.itens_pedidos:
                self.tabela.tree.insert(
                    "", "end",
                    values=(f"#{pedido.id}", str(pedido.estado), item.quantidade, item.nome)
                )
class IngredientesPedido(tk.Frame):
    def __init__(self, parent, app, pedido):
        super().__init__(parent)
        self.app = app
        self.pedido = pedido
        self.controller = PedidosViewController()
        self.labels_com_quebra = []
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Ingredientes e observações - Pedido #{self.pedido.id}").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")
        tk.Button(
            rodape, text="Voltar",
            command=lambda: self.app.mostrar(DetalhesPedido, pedido=self.pedido)
        ).pack(pady=10)

        frame_lista = tk.Frame(self)
        frame_lista.pack(fill="both", expand=True, padx=5)

        canvas = tk.Canvas(frame_lista, highlightthickness=0)
        barra = tk.Scrollbar(frame_lista, command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        lista = tk.Frame(canvas)
        janela_lista = canvas.create_window((0, 0), window=lista, anchor="nw")
        lista.bind(
            "<Configure>",
            lambda _evento: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda evento: self._ajustar_largura(
                evento.width, canvas, janela_lista
            ),
        )

        for item in self.pedido.itens_pedidos:
            ingredientes, observacao = self.controller.ingredientes_e_observacao(item)
            cartao = tk.Frame(lista, relief="groove", borderwidth=1, padx=8, pady=6)
            cartao.pack(fill="x", padx=4, pady=4)
            tk.Label(
                cartao,
                text=f"{item.quantidade} x {item.nome}",
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            ).pack(fill="x")
            self._adicionar_linha(cartao, "Ingredientes", ingredientes)
            self._adicionar_linha(cartao, "Observação", observacao)

        if not self.pedido.itens_pedidos:
            tk.Label(lista, text="Este pedido não possui itens.", anchor="w").pack(
                fill="x", padx=8, pady=8
            )

    def _adicionar_linha(self, parent, titulo, valor):
        label = tk.Label(
            parent,
            text=f"{titulo}: {valor}",
            justify="left",
            anchor="w",
            wraplength=500,
        )
        label.pack(fill="x", anchor="w", pady=2)
        self.labels_com_quebra.append(label)

    def _ajustar_largura(self, largura, canvas, janela_lista):
        canvas.itemconfigure(janela_lista, width=largura)
        largura_texto = max(160, largura - 36)
        for label in self.labels_com_quebra:
            label.configure(wraplength=largura_texto)