from datetime import date

from sqlalchemy import Date, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Cardapio(Base):
    __tablename__ = "cardapios"

    _id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    _data: Mapped[date] = mapped_column("data", Date, nullable=False)
    _versao: Mapped[str] = mapped_column("versao", String, nullable=False)
    _ativo: Mapped[bool] = mapped_column(
        "ativo", Boolean, nullable=False, default=False
    )

    def __init__(
        self, id: int = None, data: date = None, versao: str = "", ativo: bool = False
    ):
        if id is not None:
            self._id = id
        self._data = data
        self._versao = versao
        self._ativo = ativo

    @property
    def data(self):
        return self._data

    @property
    def versao(self):
        return self._versao

    @property
    def id(self):
        return self._id

    @property
    def ativo(self):
        return self._ativo

    @id.setter
    def id(self, n_id):
        self._id = n_id

    @data.setter
    def data(self, n_data):
        self._data = n_data

    @versao.setter
    def versao(self, n_versao):
        self._versao = n_versao

    @ativo.setter
    def ativo(self, n_ativo):
        self._ativo = n_ativo

    def __eq__(self, outro):
        if isinstance(outro, Cardapio):
            return self._id == outro._id
        return False
