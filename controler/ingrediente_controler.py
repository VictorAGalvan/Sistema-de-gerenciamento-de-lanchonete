from dao.ingrediente_dao import IngredienteDAO


class IngredienteController:

    def __init__(self):
        self.dao = IngredienteDAO()

    def select_ingrediente(self):
        return self.dao.select()

    def insert_ingrediente(self, ingrediente):
        return self.dao.insert(ingrediente)

    def update_ingrediente(self, ingrediente):
        return self.dao.update(ingrediente)

    def delete_ingrediente(self, ingrediente):
        return self.dao.delete(ingrediente)

    def selectID_ingrediente(self, id):
        return self.dao.selectID(id)
