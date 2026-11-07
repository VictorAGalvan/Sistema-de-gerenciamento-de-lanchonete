from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    _id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    _nome: Mapped[str] = mapped_column("nome", String, nullable=False)
    _unidade: Mapped[str] = mapped_column("unidade", String, nullable=False)
    _quantidade: Mapped[int] = mapped_column(
        "quantidade", Integer, nullable=False, default=0
    )

    def __init__(
        self, id: int = None, nome: str = "", unidade: str = "un", quantidade: float = 0
    ):
        if id is not None:
            self._id = id
        self._nome = nome
        self._unidade = unidade
        self._quantidade = quantidade

    @property
    def nome(self):
        return self._nome

    @property
    def unidade(self):
        return self._unidade

    @property
    def quantidade(self):
        return self._quantidade

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, n_id):
        self._id = n_id

    @nome.setter
    def nome(self, n_nome):
        self._nome = n_nome

    @unidade.setter
    def unidade(self, n_unidade):
        self._unidade = n_unidade

    @quantidade.setter
    def quantidade(self, n_quantidade):
        self._quantidade = n_quantidade

    def __str__(self):
        return f"Ingrediente(id={self.id}, nome='{self.nome}', unidade='{self.unidade}', quantidade={self.quantidade})"

    def __repr__(self):
        return self.__str__()
