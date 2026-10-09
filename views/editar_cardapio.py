import tkinter as tk
from datetime import date, datetime

from controler.cardapio_controler import CardapioControler
from controler.itens_cardapio_controler import ItensCardapioControler
from models.Cardapio import Cardapio
from views.tabela import Tabela

from controler.ingrediente_controler import IngredienteController


class SeletorIngredientes(tk.Frame):
    """Listbox de múltipla escolha com todos os ingredientes cadastrados."""

    def __init__(self, parent, selecionados=()):
        super().__init__(parent)
        self.ingredientes = IngredienteController().select_ingrediente()
        ids = {ing.id for ing in selecionados}

        self.listbox = tk.Listbox(self, selectmode="multiple", height=5, exportselection=False)
        barra = tk.Scrollbar(self, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        for i, ing in enumerate(self.ingredientes):
            self.listbox.insert("end", ing.nome)
            if ing.id in ids:
                self.listbox.selection_set(i)

    def selecionados(self):
        return [self.ingredientes[i] for i in self.listbox.curselection()]
class ListaCardapios(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.cardapio_controler = CardapioControler()
        self.cardapios_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Cardápios disponíveis:", font=("Arial", 10, "bold")).pack(pady=5)

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Editar", command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(botoes, text="Tornar Ativo", command=self.tornar_ativo).pack(side="left", padx=5)
        tk.Button(botoes, text="Novo Cardápio", command=self.novo_cardapio).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.app.voltar_menu).pack(side="left", padx=5)

        self.tabela = Tabela(self, [
            ("id", "ID", 40),
            ("versao", "Versão", 100),
            ("data", "Data", 100),
            ("ativo", "Ativo", 60),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)
        self.desenhar_lista()

    def desenhar_lista(self):
        self.tabela.limpar()
        self.cardapios_por_iid = {}

        ativo_id = self.cardapio_controler.get_ativo_id()

        for cardapio in self.cardapio_controler.listar_cardapios():
            iid = str(cardapio.id)
            self.cardapios_por_iid[iid] = cardapio
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(
                    cardapio.id,
                    f"v{cardapio.versao}",
                    cardapio.data.strftime("%d/%m/%Y"),
                    "Sim" if cardapio.id == ativo_id else "",
                )
            )

    def _cardapio_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um cardápio na lista.")
            return None
        self.label_erro.config(text="")
        return self.cardapios_por_iid[iid]

    def tornar_ativo(self):
        cardapio = self._cardapio_selecionado()
        if cardapio is None:
            return
        self.cardapio_controler.tornar_ativo(cardapio.id)
        self.desenhar_lista()

    def abrir_editar(self):
        cardapio = self._cardapio_selecionado()
        if cardapio is None:
            return
        self.app.mostrar(EditarCardapioWindow, cardapio=cardapio)

    def novo_cardapio(self):
        self.app.mostrar(EditarCardapioWindow, cardapio=None)


class EditarCardapioWindow(tk.Frame):
    def __init__(self, parent, app, cardapio: Cardapio = None):
        super().__init__(parent)
        self.app = app
        self.cardapio_controler = CardapioControler()
        self.itens_cardapio_controler = ItensCardapioControler()
        self.cardapio = cardapio if cardapio is not None else Cardapio(id=None, data=date.today(), versao="")
        self.eh_novo = cardapio is None
        self.itens_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        titulo = "Novo Cardápio" if self.eh_novo else "Editar Cardápio"
        tk.Label(self, text=titulo, font=("Arial", 10, "bold")).pack(pady=5)

        tk.Label(self, text="Data (dd/mm/aaaa):").pack(pady=2)
        self.entry_data = tk.Entry(self)
        self.entry_data.insert(0, self.cardapio.data.strftime("%d/%m/%Y"))
        self.entry_data.pack(pady=2)

        tk.Label(self, text="Versão:").pack(pady=2)
        self.entry_versao = tk.Entry(self)
        self.entry_versao.insert(0, self.cardapio.versao)
        self.entry_versao.pack(pady=2)

        tk.Label(self, text="Itens:").pack(pady=2)

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes_item = tk.Frame(rodape)
        botoes_item.pack(pady=5)
        tk.Button(botoes_item, text="Adicionar Item", command=self.adicionar_item).pack(side="left", padx=3)
        tk.Button(botoes_item, text="Editar Item", command=self.editar_item).pack(side="left", padx=3)
        tk.Button(botoes_item, text="Remover Item", command=self.remover_item).pack(side="left", padx=3)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=5)
        tk.Button(botoes, text="Salvar Cardápio", command=self.salvar).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=lambda: self.app.mostrar(ListaCardapios)).pack(side="left", padx=5)

        self.tabela = Tabela(self, [
            ("id", "ID", 40),
            ("nome", "Nome", 120),
            ("preco", "Preço", 60),
            ("categoria", "Categoria", 90),
            ("ingredientes", "Ingredientes", 170),
        ], height=6)
        self.tabela.pack(fill="both", expand=True, padx=5)
        self.desenhar_itens()

    def desenhar_itens(self):
        self.tabela.limpar()
        self.itens_por_iid = {}

        if self.cardapio.id is None:
            return  # cardápio ainda não salvo, não tem itens pra buscar

        for item in self.itens_cardapio_controler.listar_por_cardapio(self.cardapio.id):
            iid = str(item.id)
            self.itens_por_iid[iid] = item
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(item.id, item.nome, f"R${item.preco:.2f}", item.categoria)
            )
        ingredientes = ", ".join(ing.nome for ing in item.ingredientes) or "-"
        self.tabela.tree.insert(
            "", "end", iid=iid,
            values=(item.id, item.nome, f"R${item.preco:.2f}", item.categoria, ingredientes)
        )

    def _item_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um item na lista.")
            return None
        self.label_erro.config(text="")
        return self.itens_por_iid[iid]

    def adicionar_item(self):
        if self.cardapio.id is None:
            self.label_erro.config(text="Salve o cardápio antes de adicionar itens.")
            return
        self.app.mostrar(NovoItemWindow, cardapio=self.cardapio)

    def editar_item(self):
        item = self._item_selecionado()
        if item is None:
            return
        self.app.mostrar(EditItemWindow, item_cardapio=item, cardapio=self.cardapio)

    def remover_item(self):
        item = self._item_selecionado()
        if item is None:
            return
        self.itens_cardapio_controler.remover_item_cardapio(item)
        self.desenhar_itens()

    def salvar(self):
        try:
            nova_data = datetime.strptime(self.entry_data.get(), "%d/%m/%Y").date()
        except ValueError:
            self.label_erro.config(text="Data inválida. Use dd/mm/aaaa.")
            return

        self.cardapio.data = nova_data
        self.cardapio.versao = self.entry_versao.get()

        if self.eh_novo:
            self.cardapio_controler.criar_cardapio(self.cardapio)
            self.eh_novo = False
            self.desenhar_itens()  # agora que tem id, permite mostrar/adicionar itens
        else:
            self.cardapio_controler.editar_cardapio(self.cardapio)

        self.label_erro.config(text="")


class NovoItemWindow(tk.Frame):
    def __init__(self, parent, app, cardapio):
        super().__init__(parent)
        self.app = app
        self.itens_cardapio_controler = ItensCardapioControler()
        self.cardapio = cardapio
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Novo Item", font=("Arial", 10, "bold")).pack(pady=2)

        tk.Label(self, text="Nome:").pack(pady=2)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=2)

        tk.Label(self, text="Preço:").pack(pady=2)
        self.entry_preco = tk.Entry(self)
        self.entry_preco.pack(pady=2)

        tk.Label(self, text="Categoria:").pack(pady=2)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.pack(pady=2)

        tk.Label(self, text="Ingredientes (clique para marcar/desmarcar):").pack(pady=2)
        self.seletor = SeletorIngredientes(self)
        self.seletor.pack(fill="x", padx=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(self)
        botoes.pack(pady=5)
        tk.Button(botoes, text="Adicionar", command=self.adicionar).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.voltar).pack(side="left", padx=5)

    def adicionar(self):
        try:
            preco = float(self.entry_preco.get())
        except ValueError:
            self.label_erro.config(text="Preço inválido.")
            return

        from models.ItensCardapio import ItensCardapio
        novo_item = ItensCardapio(
            id=None,
            nome=self.entry_nome.get(),
            preco=preco,
            categoria=self.entry_categoria.get(),
            ingredientes=self.seletor.selecionados(),
            id_cardapio=self.cardapio.id
        )
        self.itens_cardapio_controler.criar_item_cardapio(novo_item)
        self.voltar()

    def voltar(self):
        self.app.mostrar(EditarCardapioWindow, cardapio=self.cardapio)

    def adicionar(self):
        try:
            preco = float(self.entry_preco.get())
        except ValueError:
            self.label_erro.config(text="Preço inválido.")
            return

        from models.ItensCardapio import ItensCardapio
        novo_item = ItensCardapio(
            id=None,
            nome=self.entry_nome.get(),
            preco=preco,
            categoria=self.entry_categoria.get(),
            ingredientes=[],
            id_cardapio=self.cardapio.id
        )
        self.itens_cardapio_controler.criar_item_cardapio(novo_item)
        self.voltar()


class EditItemWindow(tk.Frame):
    def __init__(self, parent, app, item_cardapio, cardapio):
        super().__init__(parent)
        self.app = app
        self.itens_cardapio_controler = ItensCardapioControler()
        self.item_cardapio = item_cardapio
        self.cardapio = cardapio
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Editar {self.item_cardapio.nome}", font=("Arial", 10, "bold")).pack(pady=5)

        tk.Label(self, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.insert(0, self.item_cardapio.nome)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="Preço:").pack(pady=5)
        self.entry_preco = tk.Entry(self)
        self.entry_preco.insert(0, str(self.item_cardapio.preco))
        self.entry_preco.pack(pady=5)

        tk.Label(self, text="Categoria:").pack(pady=5)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.insert(0, self.item_cardapio.categoria)
        self.entry_categoria.pack(pady=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=5)

        botoes = tk.Frame(self)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", command=self.voltar).pack(side="left", padx=5)

    def voltar(self):
        self.app.mostrar(EditarCardapioWindow, cardapio=self.cardapio)

    def salvar(self):
        try:
            novo_preco = float(self.entry_preco.get())
        except ValueError:
            self.label_erro.config(text="Preço inválido.")
            return

        self.item_cardapio.nome = self.entry_nome.get()
        self.item_cardapio.preco = novo_preco
        self.item_cardapio.categoria = self.entry_categoria.get()

        self.itens_cardapio_controler.editar_item_cardapio(self.item_cardapio)
        self.voltar()