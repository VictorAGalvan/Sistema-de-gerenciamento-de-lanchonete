import tkinter as tk
from controler.itens_cardapio_controler import ItensCardapioControler
from controler.itens_pedido_controler import ItensPedidoControler
from controler.pedido_controler import PedidoControler
from factory.PedidoFactory import PedidoFactory
from models.ItensPedido import ItensPedido
from controler.cardapio_controler import CardapioControler
from views.tabela import Tabela


class Cardapio(tk.Frame):
    def __init__(self, parent, app, cliente=None):
        super().__init__(parent)
        self.app = app
        self.cardapio_controler = CardapioControler()
        self.itens_cardapio_controler = ItensCardapioControler()
        self.itens_pedido_controler = ItensPedidoControler()
        self.pedido_controler = PedidoControler()
        self.cliente = cliente
        self.carrinho = []
        self.itens_por_iid = {}
        self.create_widgets()

    # ---------- carrinho ----------
    def buscar_item_carrinho(self, item_cardapio):
        for ip in self.carrinho:
            if ip.id == item_cardapio.id:
                return ip
        return None

    def _item_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um item na lista.")
            return None
        self.label_erro.config(text="")
        return self.itens_por_iid[iid]

    def _atualizar_qtd(self, item_cardapio):
        item_pedido = self.buscar_item_carrinho(item_cardapio)
        quantidade = item_pedido.quantidade if item_pedido else 0
        self.tabela.tree.set(str(item_cardapio.id), "qtd", quantidade)

    def adicionar_ao_pedido(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return

        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)
            self.carrinho.append(item_pedido)
        else:
            item_pedido.quantidade += 1
        self._atualizar_qtd(item_cardapio)

    def remover_do_pedido(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return

        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido and item_pedido.quantidade > 0:
            item_pedido.quantidade -= 1
            if item_pedido.quantidade == 0:
                self.carrinho.remove(item_pedido)
        self._atualizar_qtd(item_cardapio)

    def abrir_detalhes(self):
        item_cardapio = self._item_selecionado()
        if item_cardapio is None:
            return

        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)
            self.carrinho.append(item_pedido)
            self._atualizar_qtd(item_cardapio)
        ItensDetail(item_cardapio, item_pedido, master=self)


    def create_widgets(self):
        tk.Label(self, text="Bem-vindo ao Cardápio!").pack(pady=5)


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

        ativo_id = self.cardapio_controler.get_ativo_id()
        itens_do_cardapio = self.itens_cardapio_controler.listar_por_cardapio(ativo_id) if ativo_id is not None else []

        for item in itens_do_cardapio:
            iid = str(item.id)
            self.itens_por_iid[iid] = item
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(item.id, item.nome, f"R${item.preco:.2f}", item.categoria, 0)
            )

    def fazer_pedido(self):
        if not self.carrinho:
            self.label_erro.config(text="Adicione pelo menos um item.")
            return

        if self.cliente is None:
            try:
                mesa = int(self.entry_mesa.get())
            except ValueError:
                self.label_erro.config(text="Número da mesa inválido.")
                return
            novo_pedido = PedidoFactory.criar_pedido_mesa(None, mesa, self.carrinho)
        else:
            novo_pedido = PedidoFactory.criar_pedido_cliente(None, self.cliente, self.carrinho)

        self.pedido_controler.criar_pedido(novo_pedido)
        self.app.voltar_menu()


# Popup mantido como Toplevel de propósito: edita o item_pedido que está
# dentro do carrinho do Frame Cardapio, e trocar de tela perderia o carrinho.
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
        tk.Label(self, text="Ingredientes (clique para marcar/desmarcar):").pack(pady=5)

        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        tk.Label(rodape, text="Observação:").pack(pady=5)
        self.entry_observacao = tk.Entry(rodape)
        self.entry_observacao.insert(0, self.item_pedido.observacao or "")
        self.entry_observacao.pack(pady=5)
        tk.Button(rodape, text="Salvar", command=self.salvar).pack(pady=10)

        # Listbox em modo "multiple": cada clique marca/desmarca um ingrediente
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
        self.item_pedido.ingredientes = [self.ingredientes[i] for i in self.listbox.curselection()]
        self.item_pedido.observacao = self.entry_observacao.get()
        self.destroy()