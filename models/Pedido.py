from ItensPedido import ItensPedido
from Cliente import Cliente


class Pedido():
    def __init__(self, itens_pedidos:list[ItensPedido], cliente:Cliente = None, mesa:int =None):
        self.itens_pedidos = itens_pedidos
        self.cliente = cliente
        self.mesa = mesa

    @property
    def itens_pedidos(self):
        return self.__itens_pedidos
    @property
    def cliente(self):
        return self.__cliente
    @property
    def mesa(self):
        return self.__mesa
    
    @itens_pedidos.setter
    def itens_pedidos(self, n_itens_pedidos):
        self.__itens_pedidos = n_itens_pedidos
    @cliente.setter
    def cliente(self, n_cliente):
        if(self.mesa != None):
            raise Exception("Não é possível ter cliente e mesa ao mesmo tempo")
        self.__cliente = n_cliente
    @mesa.setter
    def mesa(self, n_mesa):
        if(self.cliente != None):
            raise Exception("Não é possível ter cliente e mesa ao mesmo tempo")
        self.__mesa = n_mesa