from sqlalchemy import text

from database.conexao import engine
from models.Cardapio import Cardapio


class CardapioDAO:

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT id, data, versao, ativo
                FROM cardapios
                ORDER BY data
            """))
            return [
                Cardapio(id=row.id, data=row.data, versao=row.versao, ativo=row.ativo)
                for row in resultado
            ]

    def selectID(self, id: int):
        with engine.connect() as connection:
            row = connection.execute(
                text("SELECT id, data, versao, ativo FROM cardapios WHERE id = :id"),
                {"id": id},
            ).fetchone()
            if row is None:
                return None
            return Cardapio(id=row.id, data=row.data, versao=row.versao, ativo=row.ativo)

    def insert(self, cardapio: Cardapio):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO cardapios (data, versao, ativo)
                    VALUES (:data, :versao, :ativo)
                    RETURNING id
                """),
                {"data": cardapio.data, "versao": cardapio.versao, "ativo": cardapio.ativo},
            )
            cardapio.id = resultado.scalar()

    def update(self, cardapio: Cardapio):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE cardapios
                    SET data = :data, versao = :versao
                    WHERE id = :id
                """),
                {"id": cardapio.id, "data": cardapio.data, "versao": cardapio.versao},
            )

    def delete(self, cardapio: Cardapio):
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM cardapios WHERE id = :id"), {"id": cardapio.id})

    def get_ativo(self):
        with engine.connect() as connection:
            row = connection.execute(
                text("SELECT id, data, versao, ativo FROM cardapios WHERE ativo = true LIMIT 1")
            ).fetchone()
            if row is None:
                return None
            return Cardapio(id=row.id, data=row.data, versao=row.versao, ativo=row.ativo)

    def get_ativo_id(self):
        ativo = self.get_ativo()
        return ativo.id if ativo else None

    def set_ativo(self, id_cardapio: int):
        with engine.begin() as connection:
            connection.execute(text("UPDATE cardapios SET ativo = false"))
            connection.execute(
                text("UPDATE cardapios SET ativo = true WHERE id = :id"),
                {"id": id_cardapio},
            )