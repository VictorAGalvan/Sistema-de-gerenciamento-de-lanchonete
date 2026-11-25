import tkinter as tk

from controler.cardapio_view_controller import CardapioViewController
from views.tabela import Tabela


class Cardapio(tk.Frame):
    def __init__(self, parent, app, cliente=None, controller=None):
        super().__init__(parent)
        self.app = app
        self.cliente = cliente
        # reaproveita o controller (e o carrinho) ao voltar da tela de detalhes
        self.controller = controller or CardapioViewController(cliente)
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
        self.app.mostrar(
            ItensDetail,
            item_cardapio=item_cardapio,
            item_pedido=item_pedido,
            controller=self.controller,
            cliente=self.cliente,
        )

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
            no_carrinho = self.controller.buscar_item_carrinho(item)
            qtd = no_carrinho.quantidade if no_carrinho else 0
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(item.id, item.nome, f"R${item.preco:.2f}", item.categoria, qtd)
            )
        self._atualizar_resumo_carrinho()

    def fazer_pedido(self):
        mesa = self.entry_mesa.get() if self.cliente is None else ""
        erro = self.controller.fazer_pedido(mesa)
        if erro:
            self.label_erro.config(text=erro)
            return
        self.app.voltar_menu()


class ItensDetail(tk.Frame):
    def __init__(self, parent, app, item_cardapio, item_pedido, controller, cliente=None):
        super().__init__(parent)
        self.app = app
        self.item_cardapio = item_cardapio
        self.item_pedido = item_pedido
        self.controller = controller
        self.cliente = cliente
        self.ingredientes = list(self.item_cardapio.ingredientes)
        self.selecionados = {}
        self.quantidades = {}
        self.checkboxes = {}
        self.spinboxes = {}
        self.create_widgets()

    def voltar(self):
        self.app.mostrar(Cardapio, cliente=self.cliente, controller=self.controller)

    def create_widgets(self):
        tk.Label(
            self, text=f"Detalhes: {self.item_pedido.nome}", font=("Segoe UI", 16, "bold")
        ).pack(pady=5)
        tk.Label(self, text=f"Preço: R${self.item_pedido.preco:.2f}").pack(pady=2)
        tk.Label(
            self,
            text="Marque os ingredientes e ajuste a quantidade de cada um.",
        ).pack(pady=2)

        barra_selecao = tk.Frame(self)
        barra_selecao.pack(fill="x", padx=8, pady=4)
        self.label_selecao = tk.Label(barra_selecao, anchor="w")
        self.label_selecao.pack(side="left")
        tk.Button(
            barra_selecao,
            text="Limpar seleção",
            command=lambda: self._definir_selecao(False),
        ).pack(side="right", padx=2)
        tk.Button(
            barra_selecao,
            text="Marcar todos",
            command=lambda: self._definir_selecao(True),
        ).pack(side="right", padx=2)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        tk.Label(rodape, text="Observação:").pack(pady=2)
        self.entry_observacao = tk.Entry(rodape)
        self.entry_observacao.insert(0, self.item_pedido.observacao or "")
        self.entry_observacao.pack(pady=2)

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.voltar).pack(side="left", padx=5)

        frame_lista = tk.Frame(self)
        frame_lista.pack(fill="both", expand=True, padx=5)

        canvas = tk.Canvas(frame_lista, highlightthickness=0)
        barra = tk.Scrollbar(frame_lista, command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.canvas_ingredientes = canvas

        lista = tk.Frame(canvas)
        janela_lista = canvas.create_window((0, 0), window=lista, anchor="nw")
        lista.bind(
            "<Configure>",
            lambda _evento: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda evento: self._ajustar_lista(
                evento.width, canvas, janela_lista
            ),
        )
        self._vincular_rolagem(canvas)
        self._vincular_rolagem(lista)

        tk.Label(lista, text="Ingrediente", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=3
        )
        tk.Label(lista, text="Qtd.").grid(row=0, column=1, padx=3)
        ingredientes_selecionados = {
            ingrediente.id for ingrediente in self.item_pedido.ingredientes
        }
        if not self.ingredientes:
            tk.Label(
                lista,
                text="Este item não possui ingredientes cadastrados.",
                anchor="w",
            ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=3, pady=8)

        for i, ingrediente in enumerate(self.ingredientes):
            selecionado = ingrediente.id in ingredientes_selecionados
            self.selecionados[ingrediente.id] = tk.IntVar(
                value=1 if selecionado else 0
            )
            self.quantidades[ingrediente.id] = tk.StringVar(
                value=str(
                    self.item_pedido.quantidades_ingredientes.get(ingrediente.id, 1)
                    if selecionado
                    else 0
                )
            )
            checkbox = tk.Checkbutton(
                lista,
                text=f"{ingrediente.nome} ({ingrediente.unidade})",
                variable=self.selecionados[ingrediente.id],
                anchor="w",
                command=lambda id_ingrediente=ingrediente.id: self._atualizar_linha(
                    id_ingrediente
                ),
            )
            checkbox.grid(row=i + 1, column=0, sticky="ew", padx=3)
            self.checkboxes[ingrediente.id] = checkbox

            spinbox = tk.Spinbox(
                lista,
                from_=0,
                to=999,
                width=5,
                textvariable=self.quantidades[ingrediente.id],
                state="normal" if selecionado else "disabled",
            )
            spinbox.grid(row=i + 1, column=1, padx=3)
            self.spinboxes[ingrediente.id] = spinbox
            self._vincular_rolagem(checkbox)
            self._vincular_rolagem(spinbox)

        lista.columnconfigure(0, weight=1)
        self._atualizar_contagem()

    def _ajustar_lista(self, largura, canvas, janela_lista):
        canvas.itemconfigure(janela_lista, width=largura)
        largura_texto = max(140, largura - 125)
        for checkbox in self.checkboxes.values():
            checkbox.configure(wraplength=largura_texto)

    def _vincular_rolagem(self, widget):
        widget.bind("<MouseWheel>", self._rolar_ingredientes)
        widget.bind("<Button-4>", self._rolar_ingredientes)
        widget.bind("<Button-5>", self._rolar_ingredientes)

    def _rolar_ingredientes(self, evento):
        botao = getattr(evento, "num", 0)
        if botao == 4:
            unidades = -1
        elif botao == 5:
            unidades = 1
        else:
            delta = getattr(evento, "delta", 0) or 0
            unidades = int(-delta / 120)
            if delta and not unidades:
                unidades = -1 if delta > 0 else 1

        if unidades:
            self.canvas_ingredientes.yview_scroll(unidades, "units")
        return "break"

    def _atualizar_linha(self, id_ingrediente):
        selecionado = self.selecionados[id_ingrediente].get()
        if selecionado:
            try:
                quantidade = int(self.quantidades[id_ingrediente].get())
            except ValueError:
                quantidade = 0
            if quantidade <= 0:
                self.quantidades[id_ingrediente].set("1")
            estado = "normal"
        else:
            self.quantidades[id_ingrediente].set("0")
            estado = "disabled"
        self.spinboxes[id_ingrediente].configure(state=estado)
        self._atualizar_contagem()

    def _definir_selecao(self, selecionado):
        for id_ingrediente, variavel in self.selecionados.items():
            variavel.set(1 if selecionado else 0)
            self._atualizar_linha(id_ingrediente)

    def _atualizar_contagem(self):
        total = sum(variavel.get() for variavel in self.selecionados.values())
        self.label_selecao.config(
            text=f"Ingredientes selecionados: {total}"
        )

    def salvar(self):
        selecionados = []
        quantidades = {}
        for ingrediente in self.ingredientes:
            if not self.selecionados[ingrediente.id].get():
                continue
            try:
                quantidade = int(self.quantidades[ingrediente.id].get())
            except ValueError:
                self.label_erro.config(
                    text=f"Informe uma quantidade inteira para {ingrediente.nome}."
                )
                return
            if quantidade <= 0:
                self.label_erro.config(
                    text=f"A quantidade de {ingrediente.nome} deve ser maior que zero."
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
        self.voltar()