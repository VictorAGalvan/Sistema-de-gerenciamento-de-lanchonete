from sqlalchemy import select

from database.conexao import SessionLocal
from models.Cliente import Cliente


class ClienteDAO:

    def select(self):
        with SessionLocal() as session:
            return session.scalars(select(Cliente)).all()

    def selectID(self, id_cliente):
        with SessionLocal() as session:
            return session.get(Cliente, id_cliente)

    def selectNome(self, nome):
        with SessionLocal() as session:
            return session.scalars(select(Cliente).where(Cliente._nome == nome)).first()

    def insert(self, cliente):
        with SessionLocal() as session:
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
        return cliente

    def update(self, cliente):
        with SessionLocal() as session:
            session.merge(cliente)
            session.commit()
        return cliente

    def delete(self, id_cliente):
        with SessionLocal() as session:
            cliente = session.get(Cliente, id_cliente)
            if cliente:
                session.delete(cliente)
                session.commit()
