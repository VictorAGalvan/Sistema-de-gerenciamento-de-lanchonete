import tkinter as tk
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
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Nome: {self.item_pedido.nome}").pack(pady=5)
        tk.Label(self, text=f"Preço: R${self.item_pedido.preco:.2f}").pack(pady=5)
        tk.Label(
            self,
            text="Personalize antes de enviar o pedido. Depois, não será possível editar.",
            wraplength=280,
        ).pack(pady=5)
        tk.Label(self, text="Ingredientes (marque os que deseja manter):").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        tk.Label(rodape, text="Observação:").pack(pady=5)
        self.entry_observacao = tk.Entry(rodape)
        self.entry_observacao.insert(0, self.item_pedido.observacao or "")
        self.entry_observacao.pack(pady=5)
        tk.Button(rodape, text="Salvar", command=self.salvar).pack(pady=10)

        frame_lista = tk.Frame(self)
        frame_lista.pack(fill="both", expand=True, padx=5)

        self.listbox = tk.Listbox(frame_lista, selectmode="multiple", height=6, exportselection=False)
        barra = tk.Scrollbar(frame_lista, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        for i, ingrediente in enumerate(self.ingredientes):
            self.listbox.insert("end", ingrediente.nome)
            if ingrediente in self.item_pedido.ingredientes:
                self.listbox.selection_set(i)

    def salvar(self):
        selecionados = [
            self.ingredientes[i] for i in self.listbox.curselection()
        ]
        CardapioViewController.salvar_detalhes(
            self.item_pedido, selecionados, self.entry_observacao.get()
        )
        self.destroy()