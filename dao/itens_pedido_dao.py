from sqlalchemy import select

from database.conexao import SessionLocal
from models.ItensPedido import ItensPedido
from models.ItensCardapio import ItensCardapio, item_ingrediente_cardapio
from models.Ingrediente import Ingrediente


class ItensPedidoDAO:
    def _montar(self, row):
        item_cardapio = ItensCardapio(
            id=row.item_id,
            nome=row.item_nome,
            preco=row.item_preco,
            categoria=row.item_categoria,
            ingredientes=[],
        )
        item_pedido = ItensPedido(
            item_cardapio,
            quantidade=row.quantidade,
            observacao=row.observacao or "",
        )
        item_pedido.id = row.id
        (
            item_pedido.ingredientes,
            item_pedido.quantidades_ingredientes,
        ) = self.selectIngredientesComQuantidade(row.id)
        return item_pedido

    def select(self):
        with SessionLocal() as session:
            resultado = session.execute(
                select(
                    ItensPedidoLinha.id,
                    ItensPedidoLinha.quantidade,
                    ItensPedidoLinha.observacao,
                    ItensCardapio._id.label("item_id"),
                    ItensCardapio._nome.label("item_nome"),
                    ItensCardapio._preco.label("item_preco"),
                    ItensCardapio._categoria.label("item_categoria"),
                )
                .join(
                    ItensCardapio,
                    ItensCardapio._id == ItensPedidoLinha.id_item_cardapio,
                )
                .order_by(ItensPedidoLinha.id)
            ).all()
        return [self._montar(row) for row in resultado]

    def selectID(self, id_item):
        with SessionLocal() as session:
            row = session.execute(
                select(
                    ItensPedidoLinha.id,
                    ItensPedidoLinha.quantidade,
                    ItensPedidoLinha.observacao,
                    ItensCardapio._id.label("item_id"),
                    ItensCardapio._nome.label("item_nome"),
                    ItensCardapio._preco.label("item_preco"),
                    ItensCardapio._categoria.label("item_categoria"),
                )
                .join(
                    ItensCardapio,
                    ItensCardapio._id == ItensPedidoLinha.id_item_cardapio,
                )
                .where(ItensPedidoLinha.id == id_item)
            ).first()
        return self._montar(row) if row else None

    def select_por_pedido(self, id_pedido: int):
        with SessionLocal() as session:
            resultado = session.execute(
                select(
                    ItensPedidoLinha.id,
                    ItensPedidoLinha.quantidade,
                    ItensPedidoLinha.observacao,
                    ItensCardapio._id.label("item_id"),
                    ItensCardapio._nome.label("item_nome"),
                    ItensCardapio._preco.label("item_preco"),
                    ItensCardapio._categoria.label("item_categoria"),
                )
                .join(
                    ItensCardapio,
                    ItensCardapio._id == ItensPedidoLinha.id_item_cardapio,
                )
                .where(ItensPedidoLinha.id_pedido == id_pedido)
            ).all()
        return [self._montar(row) for row in resultado]

    def insert(self, item: ItensPedido):
        with SessionLocal() as session:
            linha = ItensPedidoLinha(
                id_item_cardapio=item.id,
                quantidade=item.quantidade,
                observacao=item.observacao,
            )
            session.add(linha)
            session.commit()
            session.refresh(linha)
            item.id = linha.id

    def update(self, item: ItensPedido):
        with SessionLocal() as session:
            linha = session.get(ItensPedidoLinha, item.id)
            if linha:
                linha.quantidade = item.quantidade
                linha.observacao = item.observacao
                session.commit()

    def delete(self, item: ItensPedido):
        self.deleteIngredientes(item.id)
        with SessionLocal() as session:
            linha = session.get(ItensPedidoLinha, item.id)
            if linha:
                session.delete(linha)
                session.commit()

    def selectIngredientesComQuantidade(self, id_item_pedido: int):
        with SessionLocal() as session:
            resultado = session.execute(
                select(Ingrediente, ItemIngredientePedido.quantidade)
                .join(
                    ItemIngredientePedido,
                    ItemIngredientePedido.id_ingrediente == Ingrediente._id,
                )
                .where(ItemIngredientePedido.id_item_pedido == id_item_pedido)
            ).all()
        ingredientes = []
        quantidades = {}
        for ingrediente, quantidade_item in resultado:
            session_expunge = Ingrediente(
                id=ingrediente.id,
                nome=ingrediente.nome,
                unidade=ingrediente.unidade,
                quantidade=ingrediente.quantidade,
            )
            ingredientes.append(session_expunge)
            quantidades[ingrediente.id] = quantidade_item
        return ingredientes, quantidades

    def insertIngrediente(
        self, id_item_pedido: int, id_ingrediente: int, quantidade: int = 1
    ):
        with SessionLocal() as session:
            session.add(
                ItemIngredientePedido(
                    id_item_pedido=id_item_pedido,
                    id_ingrediente=id_ingrediente,
                    quantidade=quantidade,
                )
            )
            session.commit()

    def deleteIngredientes(self, id_item_pedido: int):
        with SessionLocal() as session:
            session.query(ItemIngredientePedido).filter(
                ItemIngredientePedido.id_item_pedido == id_item_pedido
            ).delete(synchronize_session=False)
            session.commit()


# ---- linhas ORM auxiliares (não fazem parte do domínio) ----

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class ItensPedidoLinha(Base):
    __tablename__ = "itenspedido"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_pedido: Mapped[int | None] = mapped_column(
        "idpedido", ForeignKey("pedidos.id"), nullable=True
    )
    id_item_cardapio: Mapped[int] = mapped_column(
        "iditenscardapio", ForeignKey("itenscardapio.id"), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    observacao: Mapped[str | None] = mapped_column(String, nullable=True)

class ItemIngredientePedido(Base):
    __tablename__ = "itemingredienteitenspedido"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_item_pedido: Mapped[int] = mapped_column(
        "iditenspedido", ForeignKey("itenspedido.id"), nullable=False
    )
    id_ingrediente: Mapped[int] = mapped_column(
        "idingredientes", ForeignKey("ingredientes.id"), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
