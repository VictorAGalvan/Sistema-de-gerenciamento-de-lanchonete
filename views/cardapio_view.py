import tkinter as tk
from tkinter import messagebox

from controler.cardapio_view_controller import CardapioViewController
from views.tabela import Tabela


class Cardapio(tk.Frame):
    def __init__(self, parent, app, cliente=None):
        super().__init__(parent)
        self.app = app
        self.cliente = cliente
        self.controller = CardapioViewController(cliente)
        self.itens_por_iid = {}
        self.label_carrinho = None
        self.create_widgets()

    def _item_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um item na lista.")
            return None
        self.label_erro.config(text="")
        return self.itens_por_iid[iid]

    def _atualizar_qtd(self, item_cardapio, quantidade):
        self.tabela.tree.set(str(item_cardapio.id), "qtd", quantidade)
        self._atualizar_resumo_carrinho()

    def _atualizar_resumo_carrinho(self):
        if self.label_carrinho is None:
            return
        total_itens = sum(item.quantidade for item in self.controller.carrinho)
        total_preco = sum(
            item.preco * item.quantidade for item in self.controller.carrinho
        )
        self.label_carrinho.config(
            text=f"Carrinho: {total_itens} item(ns)  |  Total: R$ {total_preco:.2f}"
        )

    def adicionar_ao_pedido(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return
        quantidade = self.controller.adicionar_ao_carrinho(item_cardapio)
        self._atualizar_qtd(item_cardapio, quantidade)

    def remover_do_pedido(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return
        quantidade = self.controller.remover_do_carrinho(item_cardapio)
        self._atualizar_qtd(item_cardapio, quantidade)

    def abrir_detalhes(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return

        item_pedido = self.controller.obter_item_para_detalhes(item_cardapio)
        self._atualizar_qtd(item_cardapio, item_pedido.quantidade)
        ItensDetail(item_cardapio, item_pedido, master=self)


    def create_widgets(self):
        tk.Label(self, text="Cardápio", font=("Segoe UI", 16, "bold")).pack(pady=5)
        tk.Label(
            self,
            text="Selecione um item e use + / - para ajustar a quantidade.",
        ).pack(pady=2)
        self.label_carrinho = tk.Label(self, text="Carrinho: 0 item(ns)  |  Total: R$ 0.00")
        self.label_carrinho.pack(pady=4)


        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        if self.cliente is None:
            tk.Label(rodape, text="Número da mesa:").pack(pady=2)
            self.entry_mesa = tk.Entry(rodape)
            self.entry_mesa.pack(pady=2)

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes_item = tk.Frame(rodape)
        botoes_item.pack(pady=5)
        tk.Button(botoes_item, text="+", width=4, command=self.adicionar_ao_pedido).pack(side="left", padx=2)
        tk.Button(botoes_item, text="-", width=4, command=self.remover_do_pedido).pack(side="left", padx=2)
        tk.Button(botoes_item, text="Info", command=self.abrir_detalhes).pack(side="left", padx=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=5)
        tk.Button(botoes, text="Fazer Pedido", command=self.fazer_pedido).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.app.voltar_menu).pack(side="left", padx=5)

        self.tabela = Tabela(self, [
            ("id", "ID", 40),
            ("nome", "Nome", 150),
            ("preco", "Preço", 70),
            ("categoria", "Categoria", 100),
            ("qtd", "Qtd", 40),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)

        for item in self.controller.listar_itens_ativos():
            iid = str(item.id)
            self.itens_por_iid[iid] = item
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(item.id, item.nome, f"R${item.preco:.2f}", item.categoria, 0)
            )

    def fazer_pedido(self):
        mesa = self.entry_mesa.get() if self.cliente is None else ""
        erro = self.controller.fazer_pedido(mesa)
        if erro:
            self.label_erro.config(text=erro)
            return
        self.app.voltar_menu()

class ItensDetail(tk.Toplevel):
    def __init__(self, item_cardapio, item_pedido, master=None):
        super().__init__(master)
        self.title(f"Detalhes do Item {item_pedido.nome}")
        self.geometry("300x350")
        self.item_cardapio = item_cardapio
        self.item_pedido = item_pedido
        self.ingredientes = list(self.item_cardapio.ingredientes)
        self.selecionados = {}
        self.quantidades = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Nome: {self.item_pedido.nome}").pack(pady=5)
        tk.Label(self, text=f"Preço: R${self.item_pedido.preco:.2f}").pack(pady=5)
        tk.Label(
            self,
            text="Personalize os ingredientes e suas quantidades antes de enviar o pedido.",
            wraplength=280,
        ).pack(pady=5)
        tk.Label(self, text="Marque os ingredientes e ajuste a quantidade:").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        tk.Label(rodape, text="Observação:").pack(pady=5)
        self.entry_observacao = tk.Entry(rodape)
        self.entry_observacao.insert(0, self.item_pedido.observacao or "")
        self.entry_observacao.pack(pady=5)
        tk.Button(rodape, text="Salvar", command=self.salvar).pack(pady=10)

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
            lambda evento: canvas.configure(
                scrollregion=(0, 0, evento.width, evento.height)
            ),
        )
        canvas.bind(
            "<Configure>",
            lambda evento: canvas.itemconfigure(janela_lista, width=evento.width),
        )

        tk.Label(lista, text="Ingrediente", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=3
        )
        tk.Label(lista, text="Qtd.").grid(row=0, column=1, padx=3)
        for i, ingrediente in enumerate(self.ingredientes):
            selecionado = ingrediente in self.item_pedido.ingredientes
            self.selecionados[ingrediente.id] = tk.IntVar(
                value=1 if selecionado else 0
            )
            self.quantidades[ingrediente.id] = tk.StringVar(
                value=str(
                    self.item_pedido.quantidades_ingredientes.get(
                        ingrediente.id, 1
                    )
                )
            )
            tk.Checkbutton(
                lista,
                text=f"{ingrediente.nome} ({ingrediente.unidade})",
                variable=self.selecionados[ingrediente.id],
                anchor="w",
            ).grid(row=i + 1, column=0, sticky="ew", padx=3)
            tk.Spinbox(
                lista,
                from_=1,
                to=999,
                width=5,
                textvariable=self.quantidades[ingrediente.id],
            ).grid(row=i + 1, column=1, padx=3)
        lista.columnconfigure(0, weight=1)

    def salvar(self):
        selecionados = []
        quantidades = {}
        for ingrediente in self.ingredientes:
            if not self.selecionados[ingrediente.id].get():
                continue
            try:
                quantidade = int(self.quantidades[ingrediente.id].get())
            except ValueError:
                messagebox.showerror(
                    "Quantidade inválida",
                    f"Informe uma quantidade inteira para {ingrediente.nome}.",
                    parent=self,
                )
                return
            if quantidade <= 0:
                messagebox.showerror(
                    "Quantidade inválida",
                    f"A quantidade de {ingrediente.nome} deve ser maior que zero.",
                    parent=self,
                )
                return
            selecionados.append(ingrediente)
            quantidades[ingrediente.id] = quantidade

        CardapioViewController.salvar_detalhes(
            self.item_pedido,
            selecionados,
            self.entry_observacao.get(),
            quantidades,
        )
        self.destroy()