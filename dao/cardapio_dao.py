from models import Cardapio


cardapio_mock:list[Cardapio] = []

def select_cardapio() -> list[Cardapio]:
    return cardapio_mock

def insert_cardapio(cardapio: Cardapio) -> None:
    cardapio_mock.append(cardapio)

def update_cardapio(cardapio: Cardapio) -> None:
    for i in cardapio_mock:
        if cardapio == i:
            cardapio_mock.remove(i)
            cardapio_mock.append(cardapio)
            break

def delete_cardapio(cardapio: Cardapio) -> None:
    for i in cardapio_mock:
        if cardapio == i:
            cardapio_mock.remove(i)
            break