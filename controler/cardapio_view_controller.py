from controler.cardapio_controler import CardapioControler
from controler.itens_cardapio_controler import ItensCardapioControler
from controler.pedido_controler import PedidoControler
from factory.PedidoFactory import PedidoFactory
from models.EstoqueInsuficienteError import EstoqueInsuficienteError
from models.ItensPedido import ItensPedido


class CardapioViewController:
    def __init__(self, cliente=None):
        self.cliente = cliente
        self.cardapios = CardapioControler()
        self.itens_cardapio = ItensCardapioControler()
        self.pedidos = PedidoControler()
        self.carrinho = []

    def listar_itens_ativos(self):
        ativo_id = self.cardapios.get_ativo_id()
        if ativo_id is None:
            return []
        return self.itens_cardapio.listar_por_cardapio(ativo_id)

    def buscar_item_carrinho(self, item_cardapio):
        for item_pedido in self.carrinho:
            if item_pedido.id == item_cardapio.id:
                return item_pedido
        return None

    def adicionar_ao_carrinho(self, item_cardapio):
        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido is None:
            item_pedido = ItensPedido(item_cardapio, quantidade=1)
            self.carrinho.append(item_pedido)
        else:
            item_pedido.quantidade += 1
        return item_pedido.quantidade

    def remover_do_carrinho(self, item_cardapio):
        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido is None:
            return 0

        item_pedido.quantidade -= 1
        if item_pedido.quantidade == 0:
            self.carrinho.remove(item_pedido)
            return 0
        return item_pedido.quantidade

    def obter_item_para_detalhes(self, item_cardapio):
        item_pedido = self.buscar_item_carrinho(item_cardapio)
        if item_pedido is None:
            self.adicionar_ao_carrinho(item_cardapio)
            item_pedido = self.buscar_item_carrinho(item_cardapio)
        return item_pedido

    @staticmethod
    def salvar_detalhes(item_pedido, ingredientes, observacao, quantidades_ingredientes=None):
        item_pedido.ingredientes = ingredientes
        item_pedido.observacao = observacao
        item_pedido.quantidades_ingredientes = (
            quantidades_ingredientes
            if quantidades_ingredientes is not None
            else {ingrediente.id: 1 for ingrediente in ingredientes}
        )

    def fazer_pedido(self, mesa_texto=""):
        if not self.carrinho:
            return "Adicione pelo menos um item."

        if self.cliente is None:
            try:
                mesa = int(mesa_texto)
            except ValueError:
                return "Número da mesa inválido."
            novo_pedido = PedidoFactory.criar_pedido_mesa(None, mesa, self.carrinho)
        else:
            novo_pedido = PedidoFactory.criar_pedido_cliente(
                None, self.cliente, self.carrinho
            )

        try:
            self.pedidos.criar_pedido(novo_pedido)
        except EstoqueInsuficienteError as erro:
            return str(erro)
        return None
