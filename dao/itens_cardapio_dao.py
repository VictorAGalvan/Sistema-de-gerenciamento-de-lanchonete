from sqlalchemy import text

from database.conexao import engine
from models.ItensCardapio import ItensCardapio
from models.Ingrediente import Ingrediente


<<<<<<< HEAD
class ItensCardapioDAO:

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT id, nome, preco, categoria
                FROM itensCardapio
            """))

            itens = []
            for row in resultado:
                itens.append(
                    ItensCardapio(
                        id=row.id,
                        nome=row.nome,
                        preco=row.preco,
                        categoria=row.categoria,
                    )
                )
            return itens

    def insert(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itensCardapio
                        (nome, preco, categoria)
                    VALUES
                        (:nome, :preco, :categoria)
                """),
                {
                    "nome": item.nome,
                    "preco": item.preco,
                    "categoria": item.categoria,
                },
            )

    def update(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE itensCardapio
                    SET nome = :nome,
                        preco = :preco,
                        categoria = :categoria
                    WHERE id = :id
                """),
                {
                    "id": item.id,
                    "nome": item.nome,
                    "preco": item.preco,
                    "categoria": item.categoria,
                },
            )

    def delete(self, item: ItensCardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itensCardapio
                    WHERE id = :id
                """),
                {"id": item.id},
            )

    def selectID(self, id: int):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT id, nome, preco, categoria
                    FROM itensCardapio
                    WHERE id = :id
                """),
                {"id": id},
            ).fetchone()

            if row is not None:
                return ItensCardapio(
                    id=row.id,
                    nome=row.nome,
                    preco=row.preco,
                    categoria=row.categoria,
                )
            return None

    def selectIngredientes(self, id_item: int):
        """Ingredientes de um item do cardápio,
        via tabela itemIngredienteCardapio."""
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT g.id, g.nome, g.unidade, g.quantidade
                    FROM itemIngredienteCardapio icg
                    JOIN ingredientes g
                        ON g.id = icg.idingredientes
                    WHERE icg.iditensCardapio = :id_item
                """),
                {"id_item": id_item},
            )

            return [
                Ingrediente(
                    id=row.id,
                    nome=row.nome,
                    unidade=row.unidade,
                    quantidade=row.quantidade,
                )
                for row in resultado
            ]

    def insertIngrediente(self, id_item: int, id_ingrediente: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO itemIngredienteCardapio
                        (iditensCardapio, idingredientes)
                    VALUES
                        (:id_item, :id_ingrediente)
                """),
                {"id_item": id_item, "id_ingrediente": id_ingrediente},
            )

    def deleteIngredientes(self, id_item: int):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itemIngredienteCardapio
                    WHERE iditensCardapio = :id_item
                """),
                {"id_item": id_item},
            )
=======
itens_cardapio_mock: list[ItensCardapio] = [
    ItensCardapio(id=1, nome="X-Burguer", preco=10.0, categoria="Lanche", ingredientes=[
        Ingrediente(id=1, nome="Pão", unidade="unidade", quantidade=1),
        Ingrediente(id=2, nome="Hambúrguer", unidade="unidade", quantidade=1),
        Ingrediente(id=3, nome="Queijo", unidade="fatia", quantidade=1),
    ]),
    ItensCardapio(id=2, nome="Coca-Cola", preco=5.0, categoria="Bebida", ingredientes=[]),
    ItensCardapio(id=3, nome="Batata Frita", preco=7.0, categoria="Acompanhamento", ingredientes=[]),
    ItensCardapio(id=4, nome="Sorvete", preco=4.0, categoria="Sobremesa", ingredientes=[]),
]


class ItensCardapioDAO:
    def _pegar_maior_id(self) -> int:
        pk = 0
        for item in itens_cardapio_mock:
            if item.id > pk:
                pk = item.id
        return pk

    def select(self) -> list[ItensCardapio]:
        return itens_cardapio_mock

    def selectID(self, id: int) -> ItensCardapio | None:
        for item in itens_cardapio_mock:
            if item.id == id:
                return item
        return None

    def insert(self, item: ItensCardapio) -> None:
        item.id = self._pegar_maior_id() + 1
        itens_cardapio_mock.append(item)

    def update(self, item: ItensCardapio) -> None:
        pass  # já é o mesmo objeto na lista; alterações refletem direto

    def delete(self, item: ItensCardapio) -> None:
        itens_cardapio_mock.remove(item)

    # métodos de "tabela de junção" — no mock não fazem nada,
    # porque os ingredientes já ficam dentro de item.ingredientes
    def selectIngredientes(self, id_item: int) -> list[Ingrediente]:
        item = self.selectID(id_item)
        return item.ingredientes if item else []

    def insertIngrediente(self, id_item: int, id_ingrediente: int) -> None:
        pass

    def deleteIngredientes(self, id_item: int) -> None:
        pass
>>>>>>> add/interface
