import tkinter as tk
from tkinter import ttk


class Tabela(tk.Frame):

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
       
        sel = self.tree.selection()
        return sel[0] if sel else None