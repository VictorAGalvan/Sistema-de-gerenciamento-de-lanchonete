from dao.cardapio_dao import cardapio_mock, select_por_id
class CardapioControler:
    def __init__(self):
        pass

    def listar_itens(self):
        return cardapio_mock
    def encotrar_item_por_id(self, id:int):
        return select_por_id(id)
       

