from models.EstadoPedido import Recebido
from models.ItensPedido import ItensPedido
from models.Cliente import Cliente
from models.EstadoPedido import Recebido

class Pedido():
    def __init__(self,id:int ,itens_pedidos:list[ItensPedido], cliente:Cliente = None, mesa:int =None):
        self.id = id
        self.itens_pedidos = itens_pedidos
        self.cliente = cliente
        self.mesa = mesa
        self.estado = Recebido() 

    @property
    def estado(self):
        return self.__estado
    @property
    def itens_pedidos(self):
        return self.__itens_pedidos
    @property
    def cliente(self):
        return self.__cliente
    @property
    def mesa(self):
        return self.__mesa
    @property
    def id(self):
        return self.__id

    @estado.setter
    def estado(self, n_estado):
        self.__estado = n_estado   
    @id.setter
    def id(self, n_id):
        self.__id = n_id
    @itens_pedidos.setter
    def itens_pedidos(self, n_itens_pedidos):
        self.__itens_pedidos = n_itens_pedidos
    @cliente.setter
    def cliente(self, n_cliente):
        if n_cliente is not None and self.mesa is not None:
            raise Exception("Não é possível ter cliente e mesa ao mesmo tempo")
        self.__cliente = n_cliente

    @mesa.setter
    def mesa(self, n_mesa):
        if n_mesa is not None and self.cliente is not None:
            raise Exception("Não é possível ter cliente e mesa ao mesmo tempo")
        self.__mesa = n_mesa