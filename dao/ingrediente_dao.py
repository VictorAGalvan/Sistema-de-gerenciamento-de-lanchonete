from sqlalchemy import select
from database.conexao import SessionLocal
from models.Ingrediente import Ingrediente

class IngredienteDAO:

    def inserir(self, ingrediente):

        with SessionLocal() as session:
            session.add(ingrediente)
            session.commit()
            session.refresh(ingrediente)

            return ingrediente

    def listar(self):

        with SessionLocal() as session:

            resultado = session.scalars(select(Ingrediente))

            return resultado.all()

    def buscar_por_id(self, id):

        with SessionLocal() as session:

            return session.get(Ingrediente, id)

    def atualizar(self, ingrediente):

        with SessionLocal() as session:

            session.merge(ingrediente)
            session.commit()

    def excluir(self, id):

        with SessionLocal() as session:

            ingrediente = session.get(Ingrediente, id)

            if ingrediente:
                session.delete(ingrediente)
                session.commit()
