import tkinter as tk
from controler.pedidos_view_controller import PedidosViewController
from views.tabela import Tabela

CORES_ESTADO = {
    "recebido": "#e3f2fd",
    "na_fila": "#fff4d6",
    "em_preparo": "#ffe5cc",
    "pronto": "#dcf1e3",
}


def tag_estado(estado):
    return str(estado).lower().replace(" ", "_")


def configurar_tags_estado(tree):
    for tag, cor in CORES_ESTADO.items():
        tree.tag_configure(tag, background=cor)


class Pedidos(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = PedidosViewController()
        self.pedidos_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=self.app.voltar_menu).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text="Pedidos realizados", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Label(titulos, text="Selecione um pedido para avançar o estado ou ver os detalhes.", fg="#607d8b").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red", anchor="w")
        self.label_erro.pack(fill="x", padx=5, pady=(6, 0))

        botoes = tk.Frame(rodape)
        botoes.pack(anchor="e", padx=5, pady=10)
        tk.Button(botoes, text="Detalhes", name="secundario", command=self.abrir_detalhes).pack(side="left", padx=(0, 8))
        tk.Button(botoes, text="Avançar estado  ▶", name="principal", command=self.avancar_pedido).pack(side="left")

        self.tabela = Tabela(self, [
            ("id", "Pedido", 70),
            ("origem", "Mesa / Cliente", 150),
            ("total", "Total", 100),
            ("estado", "Estado", 150),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)
        configurar_tags_estado(self.tabela.tree)

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
                ),
                tags=(tag_estado(pedido.estado),),
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
        self.tabela.tree.item(iid, tags=(tag_estado(pedido.estado),))

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
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=lambda: self.app.mostrar(Pedidos)).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text=f"Pedido #{self.pedido.id}", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))
        info = tk.Frame(self)
        info.pack(fill="x", padx=5, pady=(0, 12))
        for coluna, (rotulo, valor) in enumerate([
            ("MESA / CLIENTE", self.controller.origem(self.pedido)),
            ("ESTADO", str(self.pedido.estado)),
        ]):
            caixa = tk.Frame(info, highlightbackground="#cfd8dc", highlightthickness=1, padx=18, pady=10)
            caixa.grid(row=0, column=coluna, sticky="w", padx=(0, 12))
            tk.Label(caixa, text=rotulo, font=("Segoe UI", 8, "bold"), fg="#607d8b").pack(anchor="w")
            tk.Label(caixa, text=valor, font=("Segoe UI", 14, "bold")).pack(anchor="w")

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        botoes = tk.Frame(rodape)
        botoes.pack(anchor="e", padx=5, pady=10)
        tk.Button(
            botoes, text="Ingredientes / Obs", name="principal",
            command=lambda: self.app.mostrar(IngredientesPedido, pedido=self.pedido)
        ).pack(side="left")

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
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=self.app.voltar_menu).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text="Meus pedidos", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Label(titulos, text="Acompanhe o andamento dos seus pedidos.", fg="#607d8b").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        self.tabela = Tabela(self, [
            ("pedido", "Pedido", 70),
            ("estado", "Estado", 110),
            ("qtd", "Qtd", 50),
            ("item", "Item", 180),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)
        configurar_tags_estado(self.tabela.tree)

        # uma linha por item; o número e o estado do pedido se repetem
        for pedido in self.controller.listar_por_cliente(self.cliente):
            for item in pedido.itens_pedidos:
                self.tabela.tree.insert(
                    "", "end",
                    values=(f"#{pedido.id}", str(pedido.estado), item.quantidade, item.nome),
                    tags=(tag_estado(pedido.estado),),
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
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=lambda: self.app.mostrar(DetalhesPedido, pedido=self.pedido)).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text=f"Ingredientes e observações - Pedido #{self.pedido.id}", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

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
            cartao = tk.Frame(lista, highlightbackground="#cfd8dc", highlightthickness=1, padx=10, pady=8)
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