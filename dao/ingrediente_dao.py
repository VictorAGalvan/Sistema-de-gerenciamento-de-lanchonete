from sqlalchemy import select, update

from database.conexao import SessionLocal
from models.Ingrediente import Ingrediente


class IngredienteDAO:

    def select(self):
        with SessionLocal() as session:
            return session.scalars(select(Ingrediente)).all()

    def selectID(self, id_ingrediente):
        with SessionLocal() as session:
            return session.get(Ingrediente, id_ingrediente)

    def insert(self, ingrediente: Ingrediente):
        with SessionLocal() as session:
            session.add(ingrediente)
            session.commit()
            session.refresh(ingrediente)
            return ingrediente

    def update(self, ingrediente: Ingrediente):
        with SessionLocal() as session:
            session.merge(ingrediente)
            session.commit()
        return ingrediente

    def restock(self, id_ingrediente: int, quantidade: float):
        with SessionLocal() as session:
            session.execute(
                update(Ingrediente)
                .where(Ingrediente._id == id_ingrediente)
                .values(quantidade=Ingrediente._quantidade + quantidade)
                .execution_options(synchronize_session=False)
            )
            session.commit()

    def delete(self, ingrediente: Ingrediente):
        with SessionLocal() as session:
            gerenciado = session.merge(ingrediente)
            session.delete(gerenciado)
            session.commit()
