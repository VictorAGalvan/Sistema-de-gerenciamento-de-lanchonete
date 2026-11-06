from sqlalchemy import select

from database.conexao import SessionLocal
from dao.itens_pedido_dao import ItensPedidoDAO, ItensPedidoLinha, ItemIngredientePedido
from models.PedidoMesa import PedidoMesa
from models.PedidoCliente import PedidoCliente
from models.Cliente import Cliente
from models.EstadoPedido import Recebido, NaFila, EmPreparo, Pronto
from models.EstoqueInsuficienteError import EstoqueInsuficienteError

ESTADOS_CHAR = {"Recebido": "R", "Na Fila": "N", "Em Preparo": "E", "Pronto": "P"}
CHAR_PARA_ESTADO = {"R": Recebido, "N": NaFila, "E": EmPreparo, "P": Pronto}


class PedidoDAO:
    def __init__(self):
        self.dao_itens_pedido = ItensPedidoDAO()

    def _estado_para_char(self, estado):
        return ESTADOS_CHAR.get(str(estado), "R")

    def _char_para_estado(self, char):
        return CHAR_PARA_ESTADO.get(char, Recebido)()

    def _montar_pedido(self, row):
        itens = self.dao_itens_pedido.select_por_pedido(row.id)

        if row.cliente_id is not None:
            cliente = Cliente(
                id=row.cliente_id,
                nome=row.cliente_nome,
                cpf=row.cliente_cpf,
                telefone=row.cliente_telefone,
                senha=None,
            )
            pedido = PedidoCliente(id=row.id, itens_pedidos=itens, cliente=cliente)
        else:
            pedido = PedidoMesa(id=row.id, itens_pedidos=itens, mesa=row.mesa)

        pedido.estado = self._char_para_estado(row.estado)
        return pedido

    def select(self):
        with SessionLocal() as session:
            resultado = session.execute(
                select(
                    PedidoLinha.id,
                    PedidoLinha.mesa,
                    PedidoLinha.estado,
                    Cliente._id.label("cliente_id"),
                    Cliente._nome.label("cliente_nome"),
                    Cliente._cpf.label("cliente_cpf"),
                    Cliente._telefone.label("cliente_telefone"),
                )
                .outerjoin(Cliente, Cliente._id == PedidoLinha.id_cliente)
                .order_by(PedidoLinha.id)
            ).all()
        return [self._montar_pedido(row) for row in resultado]

    def selectID(self, id_pedido):
        with SessionLocal() as session:
            row = session.execute(
                select(
                    PedidoLinha.id,
                    PedidoLinha.mesa,
                    PedidoLinha.estado,
                    Cliente._id.label("cliente_id"),
                    Cliente._nome.label("cliente_nome"),
                    Cliente._cpf.label("cliente_cpf"),
                    Cliente._telefone.label("cliente_telefone"),
                )
                .outerjoin(Cliente, Cliente._id == PedidoLinha.id_cliente)
                .where(PedidoLinha.id == id_pedido)
            ).first()
        return self._montar_pedido(row) if row else None

    def select_por_cliente(self, id_cliente):
        with SessionLocal() as session:
            resultado = session.execute(
                select(
                    PedidoLinha.id,
                    PedidoLinha.mesa,
                    PedidoLinha.estado,
                    Cliente._id.label("cliente_id"),
                    Cliente._nome.label("cliente_nome"),
                    Cliente._cpf.label("cliente_cpf"),
                    Cliente._telefone.label("cliente_telefone"),
                )
                .join(Cliente, Cliente._id == PedidoLinha.id_cliente)
                .where(Cliente._id == id_cliente)
                .order_by(PedidoLinha.id)
            ).all()
        return [self._montar_pedido(row) for row in resultado]

    def insert(self, pedido):
        cliente = getattr(pedido, "cliente", None)
        mesa = getattr(pedido, "mesa", None)

        with SessionLocal() as session:
            # cálculo do consumo total por ingrediente
            consumo_por_ingrediente = {}
            for item in pedido.itens_pedidos:
                for ingrediente in item.ingredientes:
                    consumo_por_ingrediente[
                        ingrediente.id
                    ] = consumo_por_ingrediente.get(
                        ingrediente.id, 0
                    ) + item.quantidade * item.quantidades_ingredientes.get(
                        ingrediente.id, 1
                    )

            #Trava lógica para impedir condição de corrida entre pedidos
            ingredientes_bloqueados = {}
            for id_ingrediente in sorted(consumo_por_ingrediente):
                ingrediente = session.execute(
                    select(IngredienteLinha)
                    .where(IngredienteLinha._id == id_ingrediente)
                    .with_for_update()
                ).scalar_one_or_none()
                if ingrediente is None:
                    raise EstoqueInsuficienteError(
                        f"Ingrediente {id_ingrediente} não está mais cadastrado."
                    )
                ingredientes_bloqueados[id_ingrediente] = ingrediente

            for id_ingrediente, consumo in consumo_por_ingrediente.items():
                ingrediente = ingredientes_bloqueados[id_ingrediente]
                if ingrediente._quantidade < consumo:
                    raise EstoqueInsuficienteError(
                        f"Estoque insuficiente de {ingrediente._nome}: "
                        f"disponível {ingrediente._quantidade}, necessário {consumo}."
                    )

            for id_ingrediente, consumo in consumo_por_ingrediente.items():
                ingredientes_bloqueados[id_ingrediente]._quantidade -= consumo

            linha = PedidoLinha(
                id_cliente=cliente.id if cliente else None,
                mesa=mesa,
                estado=self._estado_para_char(pedido.estado),
            )
            session.add(linha)
            session.flush()
            pedido.id = linha.id

            for item in pedido.itens_pedidos:
                linha_item = ItensPedidoLinha(
                    id_pedido=pedido.id,
                    id_item_cardapio=item.id,
                    quantidade=item.quantidade,
                    observacao=item.observacao,
                )
                session.add(linha_item)
                session.flush()

                for ingrediente in item.ingredientes:
                    session.add(
                        ItemIngredientePedido(
                            id_item_pedido=linha_item.id,
                            id_ingrediente=ingrediente.id,
                            quantidade=item.quantidades_ingredientes.get(
                                ingrediente.id, 1
                            ),
                        )
                    )

            session.commit()

    def update(self, pedido):
        with SessionLocal() as session:
            linha = session.get(PedidoLinha, pedido.id)
            if linha:
                linha.estado = self._estado_para_char(pedido.estado)
                session.commit()

    def delete(self, pedido):
        with SessionLocal() as session:
            ids_itens = [
                row[0] for row in session.execute(
                    select(ItensPedidoLinha.id)
                    .where(ItensPedidoLinha.id_pedido == pedido.id)
                ).all()
            ]
            if ids_itens:
                session.query(ItemIngredientePedido).filter(
                    ItemIngredientePedido.id_item_pedido.in_(ids_itens)
                ).delete(synchronize_session=False)
            session.query(ItensPedidoLinha).filter(
                ItensPedidoLinha.id_pedido == pedido.id
            ).delete(synchronize_session=False)
            linha = session.get(PedidoLinha, pedido.id)
            if linha:
                session.delete(linha)
            session.commit()

    def select_nao_finalizados(self):
        return [p for p in self.select() if not isinstance(p.estado, Pronto)]


# ---- entidades ORM auxiliares (tabelas pedidos e trava de estoque) ----

from sqlalchemy import CHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
from models.Ingrediente import Ingrediente as IngredienteLinha

class PedidoLinha(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int | None] = mapped_column(
        "idclientes", ForeignKey("clientes.id"), nullable=True
    )
    mesa: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado: Mapped[str] = mapped_column(CHAR, nullable=False, default="R")
