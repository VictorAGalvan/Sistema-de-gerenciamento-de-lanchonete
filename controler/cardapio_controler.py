class CardapioControler:
    def __init__(self):
        pass

    def listar_itens(self):
        cardapio_mock = {
            "data":"26/06/2026",
            "versao":"1.0",
            "itens" : [
                {"nome":"X-Burguer", "preco": 10.0, "categoria":"Lanche"},
                {"nome":"Coca-Cola", "preco": 5.0, "categoria":"Bebida"},
                {"nome":"Batata Frita", "preco": 7.0, "categoria":"Acompanhamento"},
                {"nome":"Sorvete", "preco": 4.0, "categoria":"Sobremesa"}
            ]
        }
        return cardapio_mock
