from dao.itens_cardapio_dao import ItensCardapioDAO
from dao.itens_pedido_dao import ItensPedidoDAO
from dao.pedido_dao import PedidoDAO
from factory.PedidoFactory import PedidoFactory
from models.Pedido import Pedido
from models.ItensPedido import ItensPedido
import tkinter as tk


class Cardapio(tk.Toplevel):
    def __init__(self, master=None, cliente = None):
        super().__init__(master)
        self.title("Cardápio")
        self.geometry("400x300")
        self.dao_itens = ItensCardapioDAO()
        self.pedido = Pedido(id=0, itens_pedidos=[])
        self.cliente =cliente
        self.pedido_factory = PedidoFactory()
        self.create_widgets()

    def buscar_item_pedido(self, item_cardapio):
        for ip in self.pedido.itens_pedidos:
            if ip.id == item_cardapio.id:
                return ip
        return None

    def adicionar_ao_pedido(self, item_cardapio, label_contagem):
        item_pedido = self.buscar_item_pedido(item_cardapio)
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)
            self.pedido.itens_pedidos.append(item_pedido)
        else:
            item_pedido.quantidade += 1
        label_contagem.config(text=str(item_pedido.quantidade))

    def remover_do_pedido(self, item_cardapio, label_contagem): 
        item_pedido = self.buscar_item_pedido(item_cardapio)
        if item_pedido and item_pedido.quantidade > 0:
            item_pedido.quantidade -= 1
            label_contagem.config(text=str(item_pedido.quantidade))
            if item_pedido.quantidade == 0:
                self.pedido.itens_pedidos.remove(item_pedido)

    def abrir_detalhes(self, item_cardapio, label_contagem):
        item_pedido = self.buscar_item_pedido(item_cardapio)
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)
            self.pedido.itens_pedidos.append(item_pedido)
            label_contagem.config(text=str(item_pedido.quantidade))
        ItensDetail(item_cardapio, item_pedido, master=self)

    def create_widgets(self):
        self.label = tk.Label(self, text="Bem-vindo ao Cardápio!")
        self.label.pack(pady=5)

        for item in self.dao_itens.select_todos():
            linha = tk.Frame(self)
            linha.pack(pady=5, fill="x")

            tk.Label(linha, text=f"[{item.id}] {item.nome} - R${item.preco:.2f} ({item.categoria})").pack(side="left", padx=5)

            contagem = tk.Label(linha, text="0")

            tk.Button(linha, text="+", command=lambda i=item, lbl=contagem: self.adicionar_ao_pedido(i, lbl)).pack(side="left")
            contagem.pack(side="left", padx=5)
            tk.Button(linha, text="-", command=lambda i=item, lbl=contagem: self.remover_do_pedido(i, lbl)).pack(side="left")
            tk.Button(linha, text="Info", command=lambda i=item, lbl=contagem: self.abrir_detalhes(i, lbl)).pack(side="left", padx=5)
        if(self.cliente is None):
            self.label_mesa = tk.Label(self, text="Número da mesa:")
            self.label_mesa.pack(pady=5)

            self.entry_mesa = tk.Entry(self)
            self.entry_mesa.pack(pady=5)

        botao_fazer_pedido = tk.Button(self, text="Fazer Pedido", command=self.fazer_pedido)
        botao_fazer_pedido.pack(pady=10)

    def fazer_pedido(self):
        if(self.cliente is None):
            mesa = int(self.entry_mesa.get())

        dao_pedido = PedidoDAO()
        dao_itens_pedido = ItensPedidoDAO()

        if(self.cliente is None):
            novo_pedido = self.pedido_factory.criar_pedido_mesa(mesa, self.pedido.itens_pedidos)
        else:
            novo_pedido = self.pedido_factory.criar_pedido_cliente(self.cliente, self.pedido.itens_pedidos)
        dao_pedido.insert(novo_pedido)

        for item_pedido in novo_pedido.itens_pedidos:
            item_pedido.id = dao_itens_pedido.pegar_maior_id() + 1
            dao_itens_pedido.insert(item_pedido)
        self.destroy()

class ItensDetail(tk.Toplevel):
    def __init__(self, item_cardapio, item_pedido, master=None):
        super().__init__(master)
        self.title(f"Detalhes do Item {item_pedido.nome}")
        self.geometry("300x350")
        self.item_cardapio = item_cardapio
        self.item_pedido = item_pedido
        self.vars_ingredientes = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Nome: {self.item_pedido.nome}").pack(pady=5)
        tk.Label(self, text=f"Preço: R${self.item_pedido.preco:.2f}").pack(pady=5)

        tk.Label(self, text="Ingredientes:").pack(pady=5)
        for ingrediente in self.item_cardapio.ingredientes:
            incluido = ingrediente in self.item_pedido.ingredientes
            var = tk.BooleanVar(value=incluido)
            self.vars_ingredientes[ingrediente] = var
            tk.Checkbutton(self, text=ingrediente.nome, variable=var).pack(anchor="w")

        tk.Label(self, text="Observação:").pack(pady=5)
        self.entry_observacao = tk.Entry(self)
        self.entry_observacao.insert(0, self.item_pedido.observacao or "")
        self.entry_observacao.pack(pady=5)

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=10)

    def salvar(self):
        ingredientes_selecionados = []
        for ingrediente, var in self.vars_ingredientes.items():
            if var.get():
                ingredientes_selecionados.append(ingrediente)

        self.item_pedido.ingredientes = ingredientes_selecionados
        self.item_pedido.observacao = self.entry_observacao.get()
        self.destroy()