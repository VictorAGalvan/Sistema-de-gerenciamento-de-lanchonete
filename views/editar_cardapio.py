import tkinter as tk
from datetime import date, datetime

from controler.cardapio_controler import CardapioControler
from controler.itens_cardapio_controler import ItensCardapioControler
from models.Cardapio import Cardapio


class ListaCardapios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cardápios")
        self.geometry("400x300")
        self.cardapio_controler = CardapioControler()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Cardápios disponíveis:", font=("Arial", 10, "bold")).pack(pady=5)

        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(pady=5, fill="x")
        self.desenhar_lista()

        tk.Button(self, text="Novo Cardápio", command=self.novo_cardapio).pack(pady=10)

    def desenhar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        ativo_id = self.cardapio_controler.get_ativo_id()

        for cardapio in self.cardapio_controler.listar_cardapios():
            linha = tk.Frame(self.frame_lista)
            linha.pack(pady=2, fill="x")

            texto = f"[{cardapio.id}] v{cardapio.versao} - {cardapio.data.strftime('%d/%m/%Y')}"
            if cardapio.id == ativo_id:
                texto += "  (Ativo)"
            tk.Label(linha, text=texto).pack(side="left", padx=5)

            tk.Button(linha, text="Editar", command=lambda c=cardapio: self.abrir_editar(c)).pack(side="left", padx=2)

            botao_ativo = tk.Button(linha, text="Tornar Ativo", command=lambda c=cardapio: self.tornar_ativo(c))
            if cardapio.id == ativo_id:
                botao_ativo.config(state="disabled")
            botao_ativo.pack(side="left", padx=2)

    def tornar_ativo(self, cardapio):
        self.cardapio_controler.tornar_ativo(cardapio.id)
        self.desenhar_lista()

    def abrir_editar(self, cardapio):
        EditarCardapioWindow(cardapio, master=self, on_salvar=self.desenhar_lista)

    def novo_cardapio(self):
        EditarCardapioWindow(None, master=self, on_salvar=self.desenhar_lista)


class EditarCardapioWindow(tk.Toplevel):
    def __init__(self, cardapio: Cardapio = None, master=None, on_salvar=None):
        super().__init__(master)
        self.cardapio_controler = CardapioControler()
        self.itens_cardapio_controler = ItensCardapioControler()
        self.on_salvar = on_salvar
        self.cardapio = cardapio if cardapio is not None else Cardapio(id=None, data=date.today(), versao="")
        self.eh_novo = cardapio is None
        self.title("Novo Cardápio" if self.eh_novo else "Editar Cardápio")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Data (dd/mm/aaaa):").pack(pady=5)
        self.entry_data = tk.Entry(self)
        self.entry_data.insert(0, self.cardapio.data.strftime("%d/%m/%Y"))
        self.entry_data.pack(pady=5)

        tk.Label(self, text="Versão:").pack(pady=5)
        self.entry_versao = tk.Entry(self)
        self.entry_versao.insert(0, self.cardapio.versao)
        self.entry_versao.pack(pady=5)

        tk.Label(self, text="Itens:").pack(pady=5)
        self.frame_itens = tk.Frame(self)
        self.frame_itens.pack(pady=5, fill="x")
        self.desenhar_itens()

        tk.Button(self, text="Adicionar Item Novo", command=self.adicionar_item).pack(pady=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=5)

        tk.Button(self, text="Salvar Cardápio", command=self.salvar).pack(pady=10)

    def desenhar_itens(self):
        for widget in self.frame_itens.winfo_children():
            widget.destroy()

        if self.cardapio.id is None:
            return  # cardápio ainda não salvo, não tem itens pra buscar

        for item in self.itens_cardapio_controler.listar_por_cardapio(self.cardapio.id):
            linha = tk.Frame(self.frame_itens)
            linha.pack(pady=2, fill="x")

            tk.Label(linha, text=f"[{item.id}] {item.nome} - R${item.preco:.2f} ({item.categoria})").pack(side="left", padx=5)
            tk.Button(linha, text="Editar", command=lambda i=item: self.editar_item(i)).pack(side="left", padx=2)
            tk.Button(linha, text="Remover", command=lambda i=item: self.remover_item(i)).pack(side="left", padx=2)

    def adicionar_item(self):
        if self.cardapio.id is None:
            self.label_erro.config(text="Salve o cardápio antes de adicionar itens.")
            return
        NovoItemWindow(self.cardapio, master=self, on_salvar=self.desenhar_itens)

    def editar_item(self, item_cardapio):
        EditItemWindow(item_cardapio, master=self, on_salvar=self.desenhar_itens)

    def remover_item(self, item_cardapio):
        self.itens_cardapio_controler.remover_item_cardapio(item_cardapio)
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

        if self.on_salvar:
            self.on_salvar()


class NovoItemWindow(tk.Toplevel):
    def __init__(self, cardapio, master=None, on_salvar=None):
        super().__init__(master)
        self.title("Novo Item")
        self.geometry("300x250")
        self.itens_cardapio_controler = ItensCardapioControler()
        self.cardapio = cardapio
        self.on_salvar = on_salvar
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="Preço:").pack(pady=5)
        self.entry_preco = tk.Entry(self)
        self.entry_preco.pack(pady=5)

        tk.Label(self, text="Categoria:").pack(pady=5)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.pack(pady=5)

        self.label_erro = tk.Label(self, text="", fg="red")
        self.label_erro.pack(pady=5)

        tk.Button(self, text="Adicionar", command=self.adicionar).pack(pady=10)

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

        if self.on_salvar:
            self.on_salvar()
        self.destroy()


class EditItemWindow(tk.Toplevel):
    def __init__(self, item_cardapio, master=None, on_salvar=None):
        super().__init__(master)
        self.title(f"Editar {item_cardapio.nome}")
        self.geometry("300x250")
        self.itens_cardapio_controler = ItensCardapioControler()
        self.item_cardapio = item_cardapio
        self.on_salvar = on_salvar
        self.create_widgets()

    def create_widgets(self):
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

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=10)

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

        if self.on_salvar:
            self.on_salvar()
        self.destroy()