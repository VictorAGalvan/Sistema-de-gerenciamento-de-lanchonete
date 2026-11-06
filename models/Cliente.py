from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    _id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    _nome: Mapped[str] = mapped_column("nome", String, nullable=False)
    _cpf: Mapped[str] = mapped_column("cpf", String, nullable=False, unique=True)
    _telefone: Mapped[str] = mapped_column("telefone", String, nullable=True)
    _senha: Mapped[str] = mapped_column(
        "senha", String, nullable=False, default="trocar123"
    )

    def __init__(
        self,
        id: int = None,
        nome: str = "",
        cpf: str = "",
        telefone: str = None,
        senha: str = "trocar123",
    ):
        if id is not None:
            self._id = id
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone
        self._senha = senha

    @property
    def senha(self):
        return self._senha

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def telefone(self):
        return self._telefone

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, n_id):
        self._id = n_id

    @nome.setter
    def nome(self, n_nome):
        self._nome = n_nome

    @cpf.setter
    def cpf(self, n_cpf):
        self._cpf = n_cpf

    @telefone.setter
    def telefone(self, n_telefone):
        self._telefone = n_telefone

    @senha.setter
    def senha(self, n_senha):
        self._senha = n_senha
