from sqlalchemy import text

from database.conexao import engine

from models.Pedido import Pedido
from models.Cliente import Cliente
from models.ItensPedido import ItensPedidos
from models.ItensCardapio import ItensCardapio


class PedidoDAO:

    def select(self):
        sql = text("""
            SELECT clientes.id, clientes.nome as cliente, mesa 
            FROM pedidos, clientes
            WHERE pedidos.idClientes = clientes.id
        """)
        with engine.connect() as connection:
            resultado = connection.execute(sql)
            pedidos = []

            for row in resultado:
                pedidos.append(
                    Pedido(id=row.id, itens_pedidos=[], cliente=None, mesa=row.mesa)
                )
            return pedidos

    def insert(self, pedido):
        with engine.begin() as connection:
            resultado = connection.execute(
                text("""
                    INSERT INTO pedidos (idPessoas, mesa)
                    VALUES (:id_pessoas, :mesa)
                    RETURNING id
                """),
                {"id_pessoas": pedido.cliente.id, "mesa": pedido.mesa},
            )

            id_pedido = resultado.scalar()

            for item in pedido.itens_pedidos:
                connection.execute(
                    text("""
                        INSERT INTO itensPedidos
                            (idItens, idPedidos)
                        VALUES
                            (:id_item, :id_pedido)
                    """),
                    {"id_item": item.item_cardapio.id, "id_pedido": id_pedido},
                )
        pedido.id = id_pedido
        
    def update(self, pedido):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE pedidos
                    SET idPessoas = :id_pessoas, mesa = :mesa
                    WHERE id = :id_pedido
                """),
                {
                    "id_pessoas": pedido.cliente.id,
                    "mesa": pedido.mesa,
                    "id_pedido": pedido.id,
                }
            )

            connection.execute(
                text("""
                    DELETE FROM itensPedidos
                    WHERE idPedidos = :id_pedido
                """),
                {
                    "id_pedido": pedido.id
                }
            )

            for item in pedido.itens_pedidos:
                connection.execute(
                    text("""
                        INSERT INTO itensPedidos (idItens, idPedidos)
                        VALUES (:id_item, :id_pedido)
                    """),
                    {
                        "id_item": item.item_cardapio.id,
                        "id_pedido": pedido.id
                    }
                )

    def delete(self, id_pedido):
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM itensPedidos
                    WHERE idPedidos = :id_pedido
                """),
                {
                    "id_pedido": id_pedido
                }
            )

            connection.execute(
                text("""
                    DELETE FROM pedidos
                    WHERE id = :id_pedido
                """),
                {
                    "id_pedido": id_pedido
                }
            )

    def selectID(self, id_pedido):
        sql = text("""
            SELECT
                p.id AS pedido_id,
                p.mesa,
                cl.id AS cliente_id,
                cl.nome AS cliente_nome,
                cl.cpf AS cliente_cpf,
                cl.telefone AS cliente_telefone,
                i.id AS item_id,
                i.nome AS item_nome,
                i.preco AS item_preco,
                i.categoria AS item_categoria
            FROM pedidos p
            LEFT JOIN clientes cl
                ON cl.id = p.idclientes
            LEFT JOIN itensPedidos ip
                ON ip.idPedidos = p.id
            LEFT JOIN itens i
                ON i.id = ip.idItens
            WHERE p.id = :id_pedido;
        """)

        with engine.connect() as connection:
            resultado = connection.execute(sql, {"id_pedido": id_pedido})
            linhas = resultado.fetchall()

        if not linhas:
            return None

        primeira_linha = linhas[0]
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

        for linha in linhas:
            if linha.item_id is None:
                continue

            item_cardapio = ItensCardapio(
                id=linha.item_id,
                nome=linha.item_nome,
                preco=linha.item_preco,
                categoria=linha.item_categoria,
            )

            item_pedido = ItensPedidos(
                pedido=pedido,
                item_cardapio=item_cardapio,
                quantidade=None,
                observacao=None,
                nome=linha.item_nome,
                preco=linha.item_preco,
                categoria=linha.item_categoria,
            )

            pedido.itens_pedidos.append(item_pedido)
        return pedido
