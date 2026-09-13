from abc import ABC

from models.EstadoPedido import Recebido
from models.ItensPedido import ItensPedido



class Pedido(ABC):
    def __init__(self,id:int ,itens_pedidos:list[ItensPedido]):
        self.id = id
        self.itens_pedidos = itens_pedidos
 
        self.estado = Recebido() 

    @property
    def estado(self):
        return self.__estado
    @property
    def itens_pedidos(self):
        return self.__itens_pedidos
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