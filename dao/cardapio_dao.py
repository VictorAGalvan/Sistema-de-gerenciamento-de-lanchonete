from sqlalchemy import select, update

from database.conexao import SessionLocal
from models.Cardapio import Cardapio


class CardapioDAO:
    def select(self):
        with SessionLocal() as session:
            return session.scalars(select(Cardapio).order_by(Cardapio._data)).all()

    def selectID(self, id: int):
        with SessionLocal() as session:
            return session.get(Cardapio, id)

    def insert(self, cardapio: Cardapio):
        with SessionLocal() as session:
            session.add(cardapio)
            session.commit()
            session.refresh(cardapio)

    def update(self, cardapio: Cardapio):
        with SessionLocal() as session:
            session.merge(cardapio)
            session.commit()

    def delete(self, cardapio: Cardapio):
        with SessionLocal() as session:
            gerenciado = session.merge(cardapio)
            session.delete(gerenciado)
            session.commit()

    def get_ativo(self):
        with SessionLocal() as session:
            return session.scalars(
                select(Cardapio).where(Cardapio._ativo == True)  # noqa: E712
            ).first()

    def get_ativo_id(self):
        ativo = self.get_ativo()
        return ativo.id if ativo else None

    def set_ativo(self, id_cardapio: int):
        with SessionLocal() as session:
            session.execute(update(Cardapio).values(ativo=False))
            session.execute(
                update(Cardapio).where(Cardapio._id == id_cardapio).values(ativo=True)
            )
            session.commit()
