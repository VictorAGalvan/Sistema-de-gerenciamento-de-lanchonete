from sqlalchemy import text

from database.conexao import engine

from models.Pedido import Pedido
from models.Cliente import Cliente
from models.ItensPedido import ItensPedidos
from models.ItensCardapio import ItensCardapio


class PedidoDAO:

    # Mapeamento entre o estado do pedido (model) e o CHAR da tabela pedidos
    ESTADOS_CHAR = {
        "Recebido": "R",
        "Na Fila": "N",
        "Em Preparo": "E",
        "Pronto": "P",
    }

    @staticmethod
    def _estado_para_char(estado) -> str:
        return PedidoDAO.ESTADOS_CHAR.get(str(estado), "R")

    @staticmethod
    def _char_para_estado(char):
        from models.EstadoPedido import Recebido, NaFila, EmPreparo, Pronto
        mapa = {"R": Recebido, "N": NaFila, "E": EmPreparo, "P": Pronto}
        return mapa.get(char, Recebido)()

    def select(self):
        sql = text("""
            SELECT p.id,
                   p.mesa,
                   p.estado,
                   cl.id  AS cliente_id,
                   cl.nome AS cliente_nome,
                   cl.cpf  AS cliente_cpf,
                   cl.telefone AS cliente_telefone
            FROM pedidos p
            LEFT JOIN clientes cl
                ON cl.id = p.idclientes
            ORDER BY p.id
        """)
        with engine.connect() as connection:
            resultado = connection.execute(sql)
            pedidos = []

            for row in resultado:
                cliente = None
                if row.cliente_id is not None:
                    cliente = Cliente(
                        id=row.cliente_id,
                        nome=row.cliente_nome,
                        cpf=row.cliente_cpf,
                        telefone=row.cliente_telefone,
                    )

                pedido = Pedido(
                    id=row.id,
                    itens_pedidos=[],
                    cliente=cliente,
                    mesa=row.mesa,
                )
                pedido.estado = self._char_para_estado(row.estado)
                pedidos.append(pedido)
            return pedidos

    def insert(self, pedido):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO pedidos
                        (idclientes, mesa, estado)
                    VALUES
                        (:id_clientes, :mesa, :estado)
                    RETURNING id
                """),
                {
                    "id_clientes": pedido.cliente.id if pedido.cliente else None,
                    "mesa": pedido.mesa if pedido.mesa is not None else 0,
                    "estado": self._estado_para_char(getattr(pedido, "estado", None)),
                },
            )

            id_pedido = resultado.scalar()

            for item in pedido.itens_pedidos:
                connection.execute(
                    text("""
                        INSERT INTO itensPedido
                            (iditensCardapio, quantidade, observacao)
                        VALUES
                            (:id_item, :quantidade, :observacao)
                    """),
                    {
                        "id_item": item.item_cardapio.id,
                        "quantidade": item.quantidade,
                        "observacao": item.observacao,
                    },
                )

        pedido.id = id_pedido

    def update(self, pedido):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE pedidos
                    SET idclientes = :id_clientes,
                        mesa = :mesa,
                        estado = :estado
                    WHERE id = :id_pedido
                """),
                {
                    "id_clientes": pedido.cliente.id if pedido.cliente else None,
                    "mesa": pedido.mesa if pedido.mesa is not None else 0,
                    "estado": self._estado_para_char(getattr(pedido, "estado", None)),
                    "id_pedido": pedido.id,
                },
            )

            for item in pedido.itens_pedidos:
                connection.execute(
                    text("""
                        INSERT INTO itensPedido
                            (iditensCardapio, quantidade, observacao)
                        VALUES
                            (:id_item, :quantidade, :observacao)
                    """),
                    {
                        "id_item": item.item_cardapio.id,
                        "quantidade": item.quantidade,
                        "observacao": item.observacao,
                    },
                )

    def delete(self, id_pedido):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM pedidos
                    WHERE id = :id_pedido
                """),
                {"id_pedido": id_pedido},
            )

    def selectID(self, id_pedido):
        sql = text("""
            SELECT
                p.id AS pedido_id,
                p.mesa,
                p.estado,
                cl.id AS cliente_id,
                cl.nome AS cliente_nome,
                cl.cpf AS cliente_cpf,
                cl.telefone AS cliente_telefone
            FROM pedidos p
            LEFT JOIN clientes cl
                ON cl.id = p.idclientes
            WHERE p.id = :id_pedido;
        """)

        with engine.connect() as connection:
            primeira_linha = connection.execute(sql, {"id_pedido": id_pedido}).fetchone()

        if not primeira_linha:
            return None

        cliente = None

        if primeira_linha.cliente_id is not None:
            cliente = Cliente(
                id=primeira_linha.cliente_id,
                nome=primeira_linha.cliente_nome,
                cpf=primeira_linha.cliente_cpf,
                telefone=primeira_linha.cliente_telefone,
            )

        pedido = Pedido(
            id=primeira_linha.pedido_id,
            itens_pedidos=[],
            cliente=cliente,
            mesa=primeira_linha.mesa,
        )
        pedido.estado = self._char_para_estado(primeira_linha.estado)

        return pedido
