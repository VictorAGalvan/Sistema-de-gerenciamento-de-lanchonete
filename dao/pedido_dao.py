from sqlalchemy import text

from database.conexao import engine
from dao.itens_pedido_dao import ItensPedidoDAO
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
                id=row.cliente_id, nome=row.cliente_nome,
                cpf=row.cliente_cpf, telefone=row.cliente_telefone, senha=None
            )
            pedido = PedidoCliente(id=row.id, itens_pedidos=itens, cliente=cliente)
        else:
            pedido = PedidoMesa(id=row.id, itens_pedidos=itens, mesa=row.mesa)

        pedido.estado = self._char_para_estado(row.estado)
        return pedido

    def select(self):
        with engine.connect() as connection:
            resultado = connection.execute(text("""
                SELECT p.id, p.mesa, p.estado,
                       cl.id AS cliente_id, cl.nome AS cliente_nome,
                       cl.cpf AS cliente_cpf, cl.telefone AS cliente_telefone
                FROM pedidos p
                LEFT JOIN clientes cl ON cl.id = p.idclientes
                ORDER BY p.id
            """))
            return [self._montar_pedido(row) for row in resultado]

    def selectID(self, id_pedido):
        with engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT p.id, p.mesa, p.estado,
                           cl.id AS cliente_id, cl.nome AS cliente_nome,
                           cl.cpf AS cliente_cpf, cl.telefone AS cliente_telefone
                    FROM pedidos p
                    LEFT JOIN clientes cl ON cl.id = p.idclientes
                    WHERE p.id = :id
                """),
                {"id": id_pedido},
            ).fetchone()
            if row is None:
                return None
            return self._montar_pedido(row)

    def insert(self, pedido):
        cliente = getattr(pedido, "cliente", None)
        mesa = getattr(pedido, "mesa", None)

        with engine.begin() as connection:
            consumo_por_ingrediente = {}
            for item in pedido.itens_pedidos:
                for ingrediente in item.ingredientes:
                    consumo_por_ingrediente[ingrediente.id] = (
                        consumo_por_ingrediente.get(ingrediente.id, 0)
                        + item.quantidade
                        * item.quantidades_ingredientes.get(ingrediente.id, 1)
                    )

            ingredientes_bloqueados = {}
            for id_ingrediente in sorted(consumo_por_ingrediente):
                ingrediente = connection.execute(
                    text("""
                        SELECT nome, quantidade
                        FROM ingredientes
                        WHERE id = :id
                        FOR UPDATE
                    """),
                    {"id": id_ingrediente},
                ).fetchone()
                if ingrediente is None:
                    raise EstoqueInsuficienteError(
                        f"Ingrediente {id_ingrediente} não está mais cadastrado."
                    )
                ingredientes_bloqueados[id_ingrediente] = ingrediente

            for id_ingrediente, consumo in consumo_por_ingrediente.items():
                ingrediente = ingredientes_bloqueados[id_ingrediente]
                if ingrediente.quantidade < consumo:
                    raise EstoqueInsuficienteError(
                        f"Estoque insuficiente de {ingrediente.nome}: "
                        f"disponível {ingrediente.quantidade}, necessário {consumo}."
                    )

            for id_ingrediente, consumo in consumo_por_ingrediente.items():
                connection.execute(
                    text("""
                        UPDATE ingredientes
                        SET quantidade = quantidade - :consumo
                        WHERE id = :id
                    """),
                    {"id": id_ingrediente, "consumo": consumo},
                )

            resultado = connection.execute(
                text("""
                    INSERT INTO pedidos (idclientes, mesa, estado)
                    VALUES (:id_cliente, :mesa, :estado)
                    RETURNING id
                """),
                {
                    "id_cliente": cliente.id if cliente else None,
                    "mesa": mesa,
                    "estado": self._estado_para_char(pedido.estado),
                },
            )
            pedido.id = resultado.scalar()

            for item in pedido.itens_pedidos:
                resultado_item = connection.execute(
                    text("""
                        INSERT INTO itensPedido (idpedido, iditensCardapio, quantidade, observacao)
                        VALUES (:id_pedido, :id_item_cardapio, :quantidade, :observacao)
                        RETURNING id
                    """),
                    {
                        "id_pedido": pedido.id,
                        "id_item_cardapio": item.id,
                        "quantidade": item.quantidade,
                        "observacao": item.observacao,
                    },
                )
                id_item_pedido = resultado_item.scalar()

                for ingrediente in item.ingredientes:
                    connection.execute(
                        text("""
                            INSERT INTO itemIngredienteItensPedido
                                (iditensPedido, idingredientes, quantidade)
                            VALUES (:id_item_pedido, :id_ingrediente, :quantidade)
                        """),
                        {
                            "id_item_pedido": id_item_pedido,
                            "id_ingrediente": ingrediente.id,
                            "quantidade": item.quantidades_ingredientes.get(
                                ingrediente.id, 1
                            ),
                        },
                    )

    def update(self, pedido):
        with engine.begin() as connection:
            connection.execute(
                text("UPDATE pedidos SET estado = :estado WHERE id = :id"),
                {"estado": self._estado_para_char(pedido.estado), "id": pedido.id},
            )

    def delete(self, pedido):
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM itensPedido WHERE idpedido = :id"), {"id": pedido.id})
            connection.execute(text("DELETE FROM pedidos WHERE id = :id"), {"id": pedido.id})

    def select_nao_finalizados(self):
        return [p for p in self.select() if not isinstance(p.estado, Pronto)]

    def select_por_cliente(self, id_cliente):
        with engine.connect() as connection:
            resultado = connection.execute(
                text("""
                    SELECT p.id, p.mesa, p.estado,
                           cl.id AS cliente_id, cl.nome AS cliente_nome,
                           cl.cpf AS cliente_cpf, cl.telefone AS cliente_telefone
                    FROM pedidos p
                    JOIN clientes cl ON cl.id = p.idclientes
                    WHERE cl.id = :id_cliente
                    ORDER BY p.id
                """),
                {"id_cliente": id_cliente},
            )
            return [self._montar_pedido(row) for row in resultado]