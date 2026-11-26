import tkinter as tk

from controler.cardapio_admin_controller import CardapioAdminController
from models.Cardapio import Cardapio
from views.tabela import Tabela


class SeletorIngredientes(tk.Frame):

    def __init__(self, parent, selecionados=()):
        super().__init__(parent)
        self.controller = CardapioAdminController()
        self.ingredientes = self.controller.listar_ingredientes()
        ids = {ing.id for ing in selecionados}
        self.selecoes = {}
        self.quantidades = {}
        self.spinboxes = {}

        tk.Label(
            self,
            text="Quantidades",
            anchor="w",
        ).pack(fill="x", padx=3, pady=2)

        canvas = tk.Canvas(self, height=180, highlightthickness=0)
        barra = tk.Scrollbar(self, command=canvas.yview)
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
            lambda evento: canvas.itemconfigure(janela_lista, width=evento.width),
        )

        tk.Label(lista, text="Ingrediente", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=3
        )
        tk.Label(lista, text="Quantidade").grid(
            row=0, column=1, padx=3
        )

        if not self.ingredientes:
            tk.Label(
                lista,
                text="Cadastre ingredientes antes de editar a receita.",
                anchor="w",
            ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=3, pady=8)

        for i, ingrediente in enumerate(self.ingredientes):
            selecionado = ingrediente.id in ids
            self.selecoes[ingrediente.id] = tk.IntVar(
                master=self, value=1 if selecionado else 0
            )
            self.quantidades[ingrediente.id] = tk.StringVar(
                master=self, value="1" if selecionado else "0"
            )
            checkbox = tk.Checkbutton(
                lista,
                text=f"{ingrediente.nome} ({ingrediente.unidade})",
                variable=self.selecoes[ingrediente.id],
                anchor="w",
                command=lambda id_ingrediente=ingrediente.id: self._atualizar_linha(
                    id_ingrediente
                ),
            )
            checkbox.grid(row=i + 1, column=0, sticky="ew", padx=3)

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

        lista.columnconfigure(0, weight=1)

    def selecionados(self):
        return [
            ingrediente
            for ingrediente in self.ingredientes
            if self.selecoes[ingrediente.id].get()
        ]

    def _atualizar_linha(self, id_ingrediente):
        selecionado = self.selecoes[id_ingrediente].get()
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
class ListaCardapios(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = CardapioAdminController()
        self.cardapios_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=self.app.voltar_menu).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text="Cardápios disponíveis", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Label(titulos, text="Escolha um cardápio para editar ou tornar ativo.", fg="#607d8b").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red", anchor="w")
        self.label_erro.pack(fill="x", padx=5, pady=(6, 0))

        botoes = tk.Frame(rodape)
        botoes.pack(anchor="e", padx=5, pady=10)
        tk.Button(botoes, text="Novo Cardápio", name="secundario", command=self.novo_cardapio).pack(side="left", padx=(0, 8))
        tk.Button(botoes, text="Tornar Ativo", name="secundario2", command=self.tornar_ativo).pack(side="left", padx=(0, 8))
        tk.Button(botoes, text="Editar", name="principal", command=self.abrir_editar).pack(side="left")

        self.tabela = Tabela(self, [
            ("id", "ID", 40),
            ("versao", "Versão", 100),
            ("data", "Data", 100),
            ("ativo", "Ativo", 60),
        ])
        self.tabela.pack(fill="both", expand=True, padx=5)
        self.tabela.tree.tag_configure("ativo", background="#dcf1e3")
        self.desenhar_lista()

    def desenhar_lista(self):
        self.tabela.limpar()
        self.cardapios_por_iid = {}

        cardapios, ativo_id = self.controller.listar_cardapios()

        for cardapio in cardapios:
            iid = str(cardapio.id)
            self.cardapios_por_iid[iid] = cardapio
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(
                    cardapio.id,
                    f"v{cardapio.versao}",
                    cardapio.data.strftime("%d/%m/%Y"),
                    "✔ Ativo" if cardapio.id == ativo_id else "",
                ),
                tags=("ativo",) if cardapio.id == ativo_id else (),
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
        self.controller.tornar_ativo(cardapio)
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
        self.controller = CardapioAdminController()
        self.cardapio = cardapio if cardapio is not None else self.controller.novo_cardapio()
        self.eh_novo = cardapio is None
        self.itens_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        titulo = "Novo Cardápio" if self.eh_novo else "Editar Cardápio"
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=lambda: self.app.mostrar(ListaCardapios)).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text=titulo, font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        form = tk.LabelFrame(
            self, text=" Dados do cardápio ", font=("Segoe UI", 9, "bold"),
            fg="#607d8b", padx=14, pady=8,
        )
        form.pack(fill="x", padx=5, pady=(0, 10))
        tk.Label(form, text="Data (dd/mm/aaaa)").grid(row=0, column=0, sticky="w")
        self.entry_data = tk.Entry(form, width=16)
        self.entry_data.insert(0, self.cardapio.data.strftime("%d/%m/%Y"))
        self.entry_data.grid(row=1, column=0, sticky="w", padx=(0, 16), ipady=3)

        tk.Label(form, text="Versão").grid(row=0, column=1, sticky="w")
        self.entry_versao = tk.Entry(form, width=12)
        self.entry_versao.insert(0, self.cardapio.versao)
        self.entry_versao.grid(row=1, column=1, sticky="w", padx=(0, 16), ipady=3)

        tk.Button(form, text="Salvar Cardápio", name="principal", command=self.salvar).grid(row=1, column=2, sticky="w")

        tk.Label(self, text="Itens do cardápio", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x", padx=5, pady=(0, 4))

        
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        self.label_erro = tk.Label(rodape, text="", fg="red", anchor="w")
        self.label_erro.pack(fill="x", padx=5, pady=(6, 0))

        botoes_item = tk.Frame(rodape)
        botoes_item.pack(fill="x", padx=5, pady=10)
        tk.Button(botoes_item, text="Adicionar Item", command=self.adicionar_item).pack(side="left")
        tk.Button(botoes_item, text="Remover Item", name="perigo", command=self.remover_item).pack(side="right")
        tk.Button(botoes_item, text="Editar Item", name="secundario", command=self.editar_item).pack(side="right", padx=(0, 8))

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

        for item in self.controller.listar_itens(self.cardapio):
            iid = str(item.id)
            self.itens_por_iid[iid] = item
            ingredientes = ", ".join(ing.nome for ing in item.ingredientes) or "-"
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(
                    item.id,
                    item.nome,
                    f"R${item.preco:.2f}",
                    item.categoria,
                    ingredientes,
                )
            )

    def _item_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um item na lista.")
            return None
        self.label_erro.config(text="")
        return self.itens_por_iid[iid]

    def adicionar_item(self):
        if not self.controller.pode_adicionar_itens(self.cardapio):
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
        erro = self.controller.remover_item(item)
        if erro:
            self.label_erro.config(text=erro)
            return
        self.desenhar_itens()

    def salvar(self):
        erro = self.controller.salvar_cardapio(
            self.cardapio,
            self.eh_novo,
            self.entry_data.get(),
            self.entry_versao.get(),
        )
        if erro:
            self.label_erro.config(text=erro)
            return

        if self.eh_novo:
            self.eh_novo = False
            self.desenhar_itens()

        self.label_erro.config(text="")


class NovoItemWindow(tk.Frame):
    def __init__(self, parent, app, cardapio):
        super().__init__(parent)
        self.app = app
        self.controller = CardapioAdminController()
        self.cardapio = cardapio
        self.create_widgets()

    def create_widgets(self):
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=self.voltar).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text="Novo Item", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        tk.Label(self, text="Nome:", anchor="w").pack(fill="x", padx=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Preço:", anchor="w").pack(fill="x", padx=5)
        self.entry_preco = tk.Entry(self)
        self.entry_preco.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Categoria:", anchor="w").pack(fill="x", padx=5)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Ingredientes (clique para marcar/desmarcar):", anchor="w").pack(fill="x", padx=5)
        self.seletor = SeletorIngredientes(self)
        self.seletor.pack(fill="x", padx=5)

        self.label_erro = tk.Label(self, text="", fg="red", anchor="w")
        self.label_erro.pack(fill="x", padx=5, pady=(6, 0))

        botoes = tk.Frame(self)
        botoes.pack(anchor="e", padx=5, pady=10)
        tk.Button(botoes, text="Adicionar", name="principal", command=self.adicionar).pack(side="left")

    def adicionar(self):
        erro = self.controller.criar_item(
            self.cardapio,
            self.entry_nome.get(),
            self.entry_preco.get(),
            self.entry_categoria.get(),
            self.seletor.selecionados(),
        )
        if erro:
            self.label_erro.config(text=erro)
            return

        self.voltar()

    def voltar(self):
        self.app.mostrar(EditarCardapioWindow, cardapio=self.cardapio)

class EditItemWindow(tk.Frame):
    def __init__(self, parent, app, item_cardapio, cardapio):
        super().__init__(parent)
        self.app = app
        self.controller = CardapioAdminController()
        self.item_cardapio = item_cardapio
        self.cardapio = cardapio
        self.create_widgets()

    def create_widgets(self):
        topo = tk.Frame(self)
        topo.pack(fill="x")
        tk.Button(topo, text="← Voltar", name="secundario", command=self.voltar).pack(side="left")
        titulos = tk.Frame(topo)
        titulos.pack(side="left", padx=16)
        tk.Label(titulos, text=f"Editar {self.item_cardapio.nome}", font=("Segoe UI", 17, "bold"), fg="#263238").pack(anchor="w")
        tk.Frame(self, height=1, bg="#cfd8dc").pack(fill="x", pady=(12, 12))

        tk.Label(self, text="Nome:", anchor="w").pack(fill="x", padx=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.insert(0, self.item_cardapio.nome)
        self.entry_nome.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Preço:", anchor="w").pack(fill="x", padx=5)
        self.entry_preco = tk.Entry(self)
        self.entry_preco.insert(0, str(self.item_cardapio.preco))
        self.entry_preco.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Categoria:", anchor="w").pack(fill="x", padx=5)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.insert(0, self.item_cardapio.categoria)
        self.entry_categoria.pack(fill="x", padx=5, pady=(0, 8), ipady=3)

        tk.Label(self, text="Ingredientes (clique para marcar/desmarcar):", anchor="w").pack(fill="x", padx=5)
        self.seletor = SeletorIngredientes(self, self.item_cardapio.ingredientes)
        self.seletor.pack(fill="x", padx=5)

        self.label_erro = tk.Label(self, text="", fg="red", anchor="w")
        self.label_erro.pack(fill="x", padx=5, pady=(6, 0))

        botoes = tk.Frame(self)
        botoes.pack(anchor="e", padx=5, pady=10)
        tk.Button(botoes, text="Salvar", name="principal", command=self.salvar).pack(side="left")

    def voltar(self):
        self.app.mostrar(EditarCardapioWindow, cardapio=self.cardapio)

    def salvar(self):
        erro = self.controller.salvar_item(
            self.item_cardapio,
            self.entry_nome.get(),
            self.entry_preco.get(),
            self.entry_categoria.get(),
            self.seletor.selecionados(),
        )
        if erro:
            self.label_erro.config(text=erro)
            return
        self.voltar()