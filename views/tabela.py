import tkinter as tk
from tkinter import ttk


class Tabela(tk.Frame):
    """Tabela com barra de rolagem (ttk.Treeview).

    colunas: lista de tuplas (id_da_coluna, titulo, largura)
        Tabela(self, [("id", "ID", 40), ("nome", "Nome", 150)])

    Use `tabela.tree` para inserir linhas:
        tabela.tree.insert("", "end", iid="1", values=(1, "X-Burger"))
    """

    def __init__(self, parent, colunas, height=8):
        super().__init__(parent)
        self.tree = ttk.Treeview(
            self,
            columns=[c[0] for c in colunas],
            show="headings",
            height=height,
            selectmode="browse",
        )
        for col_id, titulo, largura in colunas:
            self.tree.heading(col_id, text=titulo)
            self.tree.column(col_id, width=largura, anchor="w")

        barra = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    def limpar(self):
        self.tree.delete(*self.tree.get_children())

    def selecionado(self):
        """Devolve o iid da linha selecionada, ou None."""
        sel = self.tree.selection()
        return sel[0] if sel else None