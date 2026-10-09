import tkinter as tk

from controler.ingrediente_controler import IngredienteController
from models.Ingrediente import Ingrediente
from views.tabela import Tabela


class ListaIngredientes(tk.Frame):
    """CRUD de ingredientes numa tela só.

    Clicar numa linha preenche o formulário:
      - Adicionar -> cria um ingrediente NOVO com os dados digitados
      - Salvar    -> altera o ingrediente SELECIONADO (mesmo id)
      - Remover   -> apaga o ingrediente selecionado
      - Limpar    -> desmarca a linha e esvazia o formulário
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.controller = IngredienteController()
        self.ingredientes_por_iid = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Ingredientes", font=("Arial", 10, "bold")).pack(pady=5)

        # rodapé empacotado antes da tabela para nunca sumir da tela
        rodape = tk.Frame(self)
        rodape.pack(side="bottom", fill="x")

        form = tk.Frame(rodape)
        form.pack(pady=2)

        tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="e", padx=3, pady=1)
        self.entry_nome = tk.Entry(form, width=25)
        self.entry_nome.grid(row=0, column=1, pady=1)

        tk.Label(form, text="Unidade:").grid(row=1, column=0, sticky="e", padx=3, pady=1)
        self.entry_unidade = tk.Entry(form, width=25)
        self.entry_unidade.grid(row=1, column=1, pady=1)

        tk.Label(form, text="Quantidade:").grid(row=2, column=0, sticky="e", padx=3, pady=1)
        self.entry_quantidade = tk.Entry(form, width=25)
        self.entry_quantidade.grid(row=2, column=1, pady=1)

        self.label_erro = tk.Label(rodape, text="", fg="red")
        self.label_erro.pack(pady=2)

        botoes = tk.Frame(rodape)
        botoes.pack(pady=6)
        tk.Button(botoes, text="Adicionar", command=self.adicionar).pack(side="left", padx=2)
        tk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=2)
        tk.Button(botoes, text="Remover", command=self.remover).pack(side="left", padx=2)
        tk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left", padx=2)
        tk.Button(botoes, text="Voltar", command=self.app.voltar_menu).pack(side="left", padx=2)

        self.tabela = Tabela(self, [
            ("id", "ID", 40),
            ("nome", "Nome", 170),
            ("unidade", "Unidade", 80),
            ("quantidade", "Quantidade", 90),
        ], height=6)
        self.tabela.pack(fill="both", expand=True, padx=5)
        self.tabela.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)

        self.desenhar_lista()

    # ---------- auxiliares ----------
    def desenhar_lista(self):
        self.tabela.limpar()
        self.ingredientes_por_iid = {}

        for ing in self.controller.select_ingrediente():
            iid = str(ing.id)
            self.ingredientes_por_iid[iid] = ing
            self.tabela.tree.insert(
                "", "end", iid=iid,
                values=(ing.id, ing.nome, ing.unidade, ing.quantidade)
            )

    def ao_selecionar(self, event=None):
        iid = self.tabela.selecionado()
        if iid is None:
            return
        ing = self.ingredientes_por_iid[iid]
        self._preencher_formulario(ing.nome, ing.unidade, ing.quantidade)
        self.label_erro.config(text="")

    def _preencher_formulario(self, nome="", unidade="", quantidade=""):
        for entry, valor in (
            (self.entry_nome, nome),
            (self.entry_unidade, unidade),
            (self.entry_quantidade, quantidade),
        ):
            entry.delete(0, "end")
            entry.insert(0, str(valor))

    def limpar(self):
        self.tabela.tree.selection_remove(self.tabela.tree.selection())
        self._preencher_formulario()
        self.label_erro.config(text="")

    def _ler_formulario(self):
        nome = self.entry_nome.get().strip()
        unidade = self.entry_unidade.get().strip()
        texto_qtd = self.entry_quantidade.get().strip().replace(",", ".")

        if not nome or not unidade or not texto_qtd:
            self.label_erro.config(text="Preencha nome, unidade e quantidade.")
            return None
        try:
            quantidade = float(texto_qtd)
        except ValueError:
            self.label_erro.config(text="Quantidade inválida.")
            return None
        return nome, unidade, quantidade

    def _ingrediente_selecionado(self):
        iid = self.tabela.selecionado()
        if iid is None:
            self.label_erro.config(text="Selecione um ingrediente na lista.")
            return None
        return self.ingredientes_por_iid[iid]

    # ---------- CRUD ----------
    def adicionar(self):
        dados = self._ler_formulario()
        if dados is None:
            return
        nome, unidade, quantidade = dados

        self.controller.insert_ingrediente(
            Ingrediente(id=None, nome=nome, unidade=unidade, quantidade=quantidade)
        )
        self.desenhar_lista()
        self.limpar()

    def salvar(self):
        ingrediente = self._ingrediente_selecionado()
        if ingrediente is None:
            return
        dados = self._ler_formulario()
        if dados is None:
            return

        ingrediente.nome, ingrediente.unidade, ingrediente.quantidade = dados
        self.controller.update_ingrediente(ingrediente)
        self.desenhar_lista()
        self.limpar()

    def remover(self):
        ingrediente = self._ingrediente_selecionado()
        if ingrediente is None:
            return

        try:
            self.controller.delete_ingrediente(ingrediente)
        except Exception:
            self.label_erro.config(
                text="Não foi possível remover: o ingrediente está em uso por algum item."
            )
            return
        self.desenhar_lista()
        self.limpar() 