from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.Ingrediente import Ingrediente

# tabela de associação item do cardápio <-> ingrediente
item_ingrediente_cardapio = Table(
    "itemIngredienteCardapio",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("iditensCardapio", ForeignKey("itenscardapio.id"), nullable=False),
    Column("idingredientes", ForeignKey("ingredientes.id"), nullable=False),
)


class ItensCardapio(Base):
    __tablename__ = "itenscardapio"

    _id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    _nome: Mapped[str] = mapped_column("nome", String, nullable=False)
    _preco: Mapped[float] = mapped_column("preco", Numeric(10, 2), nullable=False)
    _categoria: Mapped[str] = mapped_column("categoria", String, nullable=False)
    _id_cardapio: Mapped[int | None] = mapped_column(
        "idcardapio", ForeignKey("cardapios.id"), nullable=True
    )

    ingredientes: Mapped[list["Ingrediente"]] = relationship(
        secondary=item_ingrediente_cardapio,
        lazy="selectin",
    )

    def __init__(
        self,
        id: int = None,
        nome: str = "",
        preco: float = 0.0,
        categoria: str = "",
        ingredientes: list[Ingrediente] = None,
        id_cardapio: int = None,
    ):
        if id is not None:
            self._id = id
        self._nome = nome
        self._preco = preco
        self._categoria = categoria
        self.ingredientes = list(ingredientes) if ingredientes is not None else []
        self._id_cardapio = id_cardapio

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def preco(self):
        return self._preco

    @property
    def categoria(self):
        return self._categoria

    @property
    def id_cardapio(self):
        return self._id_cardapio

    @id.setter
    def id(self, n_id):
        self._id = n_id

    @nome.setter
    def nome(self, n_nome):
        self._nome = n_nome

    @preco.setter
    def preco(self, n_preco):
        self._preco = n_preco

    @categoria.setter
    def categoria(self, n_categoria):
        self._categoria = n_categoria

    @id_cardapio.setter
    def id_cardapio(self, n_id_cardapio):
        self._id_cardapio = n_id_cardapio

    def __eq__(self, outro):
        if isinstance(outro, ItensCardapio):
            return self._id == outro._id
        return False

    def __hash__(self):
        return hash(self._id)
