from sqlalchemy import select, update

from database.conexao import SessionLocal
from models.ItensCardapio import ItensCardapio
from models.Ingrediente import Ingrediente


class ItensCardapioDAO:

    def select(self):
        with SessionLocal() as session:
            return session.scalars(select(ItensCardapio)).all()

    def selectID(self, id: int):
        with SessionLocal() as session:
            return session.get(ItensCardapio, id)

    def select_por_cardapio(self, id_cardapio: int):
        with SessionLocal() as session:
            return session.scalars(
                select(ItensCardapio).where(ItensCardapio._id_cardapio == id_cardapio)
            ).all()

    def insert(self, item: ItensCardapio):
        with SessionLocal() as session:
            session.add(item)
            session.commit()
            session.refresh(item)

    def update(self, item: ItensCardapio):
        with SessionLocal() as session:
            session.execute(
                update(ItensCardapio)
                .where(ItensCardapio._id == item.id)
                .values(nome=item.nome, preco=item.preco,
                        categoria=item.categoria, idcardapio=item.id_cardapio)
                .execution_options(synchronize_session=False)
            )
            session.commit()

    def delete(self, item: ItensCardapio):
        with SessionLocal() as session:
            gerenciado = session.merge(item)
            session.delete(gerenciado)
            session.commit()

    def selectIngredientes(self, id_item: int):
        with SessionLocal() as session:
            item = session.get(ItensCardapio, id_item)
            return list(item.ingredientes) if item else []

    def insertIngrediente(self, id_item: int, id_ingrediente: int):
        with SessionLocal() as session:
            item = session.get(ItensCardapio, id_item)
            ingrediente = session.get(Ingrediente, id_ingrediente)
            if item and ingrediente and ingrediente not in item.ingredientes:
                item.ingredientes.append(ingrediente)
                session.commit()

    def deleteIngredientes(self, id_item: int):
        with SessionLocal() as session:
            item = session.get(ItensCardapio, id_item)
            if item:
                item.ingredientes.clear()
                session.commit()
