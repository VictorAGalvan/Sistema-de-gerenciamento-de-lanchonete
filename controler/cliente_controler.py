from dao.cliente_dao import ClienteDAO

class ClienteController:
    def __init__(self):
        self.dao = ClienteDAO()

    def select_cliente(self):
        return self.dao.select()
    
    def insert_cliente(self, cliente):
        self.dao.insert(cliente)
        
    def update_cliente(self, cliente):
        self.dao.update(cliente)
        
    def delete_cliente(self, id_cliente):
        self.dao.delete(id_cliente)

    def selectID_cliente(self, id_cliente):
        return self.dao.selectID(id_cliente)