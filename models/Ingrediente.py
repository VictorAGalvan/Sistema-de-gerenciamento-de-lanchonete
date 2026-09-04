from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(50))

    unidade: Mapped[int] = mapped_column(Integer)
    
    quantidade: Mapped[int] = mapped_column(Integer)
