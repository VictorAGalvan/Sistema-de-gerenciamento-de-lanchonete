BEGIN;
    -- ============================================================
    -- 1. CLIENTES
    -- ============================================================
    INSERT  INTO clientes (
        id,
        nome,
        cpf,
        telefone
    )
    VALUES               (1, 'João da Silva', '11111111101', '54991111101'),
    (2, 'Maria Oliveira', '11111111102', '54991111102'),
    (3, 'Carlos Pereira', '11111111103', '54991111103'),
    (4, 'Ana Souza', '11111111104', '54991111104'),
    (5, 'Pedro Santos', '11111111105', '54991111105'),
    (6, 'Juliana Costa', '11111111106', '54991111106'),
    (7, 'Rafael Martins', '11111111107', '54991111107'),
    (8, 'Fernanda Alves', '11111111108', '54991111108'),
    (9, 'Lucas Rodrigues', '11111111109', '54991111109'),
    (10, 'Camila Ferreira', '11111111110', '54991111110'),
    (11, 'Bruno Gomes', '11111111111', '54991111111'),
    (12, 'Larissa Ribeiro', '11111111112', '54991111112'),
    (13, 'Gabriel Carvalho', '11111111113', '54991111113'),
    (14, 'Mariana Lopes', '11111111114', '54991111114'),
    (15, 'Felipe Almeida', '11111111115', '54991111115'),
    (16, 'Beatriz Rocha', '11111111116', '54991111116'),
    (17, 'Gustavo Barbosa', '11111111117', '54991111117'),
    (18, 'Isabela Nunes', '11111111118', '54991111118'),
    (19, 'Matheus Teixeira', '11111111119', '54991111119'),
    (20, 'Amanda Cardoso', '11111111120', '54991111120'),
    (21, 'Diego Moreira', '11111111121', '54991111121'),
    (22, 'Carolina Martins', '11111111122', '54991111122'),
    (23, 'Henrique Mendes', '11111111123', '54991111123'),
    (24, 'Bianca Castro', '11111111124', '54991111124'),
    (25, 'Eduardo Fernandes', '11111111125', '54991111125');
    -- ============================================================
    -- 2. INGREDIENTES / ESTOQUE
    -- ============================================================
    INSERT  INTO ingredientes (
        id,
        nome,
        unidade,
        quantidade
    )
    VALUES                   (1, 'Pão de hambúrguer', 'unidade', 80),
    (2, 'Carne bovina', 'unidade', 65),
    (3, 'Queijo mussarela', 'fatia', 150),
    (4, 'Presunto', 'fatia', 120),
    (5, 'Alface', 'folha', 180),
    (6, 'Tomate', 'unidade', 75),
    (7, 'Bacon', 'fatia', 100),
    (8, 'Ovo', 'unidade', 90),
    (9, 'Batata', 'kg', 45),
    (10, 'Refrigerante lata', 'unidade', 120),
    (11, 'Molho especial', 'ml', 7000),
    (12, 'Cebola', 'unidade', 60),
    (13, 'Frango grelhado', 'unidade', 45),
    (14, 'Catupiry', 'grama', 3000),
    (15, 'Calabresa', 'unidade', 35),
    (16, 'Pão de hot dog', 'unidade', 50),
    (17, 'Salsicha', 'unidade', 50),
    (18, 'Milho', 'grama', 2500),
    (19, 'Batata palha', 'grama', 3000),
    (20, 'Água mineral', 'unidade', 80);
    -- ============================================================
    -- 3. ITENS DO CARDÁPIO
    -- ============================================================
    INSERT  INTO itensCardapio (
        id,
        nome,
        preco,
        categoria
    )
    VALUES                    (1, 'X-Burger', 18.90, 'Hambúrguer'),
    (2, 'X-Salada', 20.90, 'Hambúrguer'),
    (3, 'X-Bacon', 22.90, 'Hambúrguer'),
    (4, 'X-Egg', 21.90, 'Hambúrguer'),
    (5, 'X-Tudo', 27.90, 'Hambúrguer'),
    (6, 'X-Frango', 21.90, 'Hambúrguer'),
    (7, 'X-Calabresa', 22.50, 'Hambúrguer'),
    (8, 'Hot Dog Especial', 19.90, 'Hot Dog'),
    (9, 'Batata Frita P', 10.90, 'Acompanhamento'),
    (10, 'Batata Frita G', 16.90, 'Acompanhamento'),
    (11, 'Refrigerante Lata', 6.00, 'Bebida'),
    (12, 'Água Mineral', 4.00, 'Bebida'),
    (13, 'Combo X-Burger', 29.90, 'Combo'),
    (14, 'Combo X-Bacon', 33.90, 'Combo'),
    (15, 'Combo X-Frango', 32.90, 'Combo');
    -- ============================================================
    -- 4. PEDIDOS
    -- 30 pedidos
    -- ============================================================
    INSERT  INTO pedidos (
        id,
        idclientes,
        mesa,
        estado
    )
    VALUES              (1, 1, 1, 'F'),
    (2, 2, 2, 'F'),
    (3, 3, 3, 'F'),
    (4, 4, 4, 'F'),
    (5, 5, 5, 'P'),
    (6, 6, 6, 'P'),
    (7, 7, 7, 'A'),
    (8, 8, 8, 'A'),
    (9, 9, 9, 'F'),
    (10, 10, 10, 'F'),
    (11, 11, 1, 'P'),
    (12, 12, 2, 'A'),
    (13, 13, 3, 'F'),
    (14, 14, 4, 'F'),
    (15, 15, 5, 'P'),
    (16, 16, 6, 'A'),
    (17, 17, 7, 'F'),
    (18, 18, 8, 'P'),
    (19, 19, 9, 'A'),
    (20, 20, 10, 'F'),
    (21, 21, 1, 'F'),
    (22, 22, 2, 'P'),
    (23, 23, 3, 'A'),
    (24, 24, 4, 'F'),
    (25, 25, 5, 'P'),
    (26, 1, 6, 'A'),
    (27, 2, 7, 'F'),
    (28, 3, 8, 'P'),
    (29, 4, 9, 'A'),
    (30, 5, 10, 'F');
    -- ============================================================
    -- 5. ITENS DOS PEDIDOS
    -- 60 itens
    --
    -- Cada pedido possui pelo menos 1 item.
    -- Vários pedidos possuem 2 ou 3 produtos.
    -- ============================================================
    INSERT  INTO itensPedido (
        id,
        iditensCardapio,
        quantidade,
        observacao
    )
    VALUES                  -- Pedido 1
    (1, 1, 2, 'Sem cebola'),
    (2, 9, 1, NULL),
    -- Pedido 2
    (3, 3, 1, 'Adicionar queijo'),
    (4, 11, 2, 'Sem gelo'),
    -- Pedido 3
    (5, 2, 1, 'Sem tomate'),
    (6, 10, 1, NULL),
    (7, 11, 1, NULL),
    -- Pedido 4
    (8, 5, 1, 'Carne bem passada'),
    (9, 12, 1, NULL),
    -- Pedido 5
    (10, 6, 2, 'Adicionar catupiry'),
    (11, 9, 1, NULL),
    -- Pedido 6
    (12, 7, 1, 'Sem cebola'),
    (13, 11, 1, 'Sem gelo'),
    -- Pedido 7
    (14, 4, 1, 'Adicionar bacon'),
    (15, 10, 1, NULL),
    -- Pedido 8
    (16, 8, 2, 'Pouco molho'),
    (17, 11, 2, NULL),
    -- Pedido 9
    (18, 1, 1, NULL),
    (19, 9, 2, NULL),
    -- Pedido 10
    (20, 13, 2, NULL),
    (21, 12, 1, NULL),
    -- Pedido 11
    (22, 2, 1, 'Sem alface'),
    (23, 11, 1, NULL),
    -- Pedido 12
    (24, 3, 2, 'Bem passado'),
    (25, 10, 1, NULL),
    -- Pedido 13
    (26, 5, 1, 'Sem tomate e sem cebola'),
    (27, 11, 1, 'Sem gelo'),
    -- Pedido 14
    (28, 6, 1, NULL),
    (29, 9, 1, NULL),
    (30, 11, 1, NULL),
    -- Pedido 15
    (31, 14, 2, NULL),
    -- Pedido 16
    (32, 8, 1, 'Sem milho'),
    (33, 12, 1, NULL),
    -- Pedido 17
    (34, 1, 2, NULL),
    (35, 10, 1, NULL),
    -- Pedido 18
    (36, 7, 1, 'Pouco molho'),
    (37, 11, 1, NULL),
    -- Pedido 19
    (38, 4, 1, 'Sem bacon'),
    (39, 9, 1, NULL),
    -- Pedido 20
    (40, 15, 1, NULL),
    (41, 11, 1, NULL),
    -- Pedido 21
    (42, 2, 2, 'Sem cebola'),
    (43, 10, 1, NULL),
    -- Pedido 22
    (44, 3, 1, 'Adicionar ovo'),
    (45, 12, 1, NULL),
    -- Pedido 23
    (46, 5, 1, 'Carne ao ponto'),
    (47, 9, 1, NULL),
    (48, 11, 1, NULL),
    -- Pedido 24
    (49, 13, 1, NULL),
    (50, 11, 1, NULL),
    -- Pedido 25
    (51, 6, 2, 'Sem tomate'),
    (52, 10, 1, NULL),
    -- Pedido 26
    (53, 8, 1, NULL),
    (54, 11, 1, 'Sem gelo'),
    -- Pedido 27
    (55, 1, 1, 'Adicionar queijo'),
    (56, 9, 1, NULL),
    -- Pedido 28
    (57, 14, 1, NULL),
    (58, 12, 1, NULL),
    -- Pedido 29
    (59, 7, 2, 'Sem cebola'),
    -- Pedido 30
    (60, 15, 1, 'Adicionar catupiry');
    -- ============================================================
    -- 6. CARDÁPIOS
    -- 3 versões
    -- ============================================================
    -- ------------------------------------------------------------
    -- Versão 1.0 — Julho
    -- ------------------------------------------------------------
    INSERT  INTO cardapios (
        id,
        iditensCardapio,
        data,
        versao
    )
    VALUES                (1, 1, '2026-07-01', '1.0'),
    (2, 2, '2026-07-01', '1.0'),
    (3, 3, '2026-07-01', '1.0'),
    (4, 4, '2026-07-01', '1.0'),
    (5, 5, '2026-07-01', '1.0'),
    (6, 6, '2026-07-01', '1.0'),
    (7, 7, '2026-07-01', '1.0'),
    (8, 8, '2026-07-01', '1.0');
    -- ------------------------------------------------------------
    -- Versão 2.0 — Agosto
    -- ------------------------------------------------------------
    INSERT  INTO cardapios (
        id,
        iditensCardapio,
        data,
        versao
    )
    VALUES                (9, 1, '2026-08-01', '2.0'),
    (10, 2, '2026-08-01', '2.0'),
    (11, 3, '2026-08-01', '2.0'),
    (12, 4, '2026-08-01', '2.0'),
    (13, 5, '2026-08-01', '2.0'),
    (14, 6, '2026-08-01', '2.0'),
    (15, 7, '2026-08-01', '2.0'),
    (16, 8, '2026-08-01', '2.0'),
    (17, 9, '2026-08-01', '2.0'),
    (18, 10, '2026-08-01', '2.0'),
    (19, 11, '2026-08-01', '2.0'),
    (20, 12, '2026-08-01', '2.0');
    -- ------------------------------------------------------------
    -- Versão 3.0 — Setembro
    -- ------------------------------------------------------------
    INSERT  INTO cardapios (
        id,
        iditensCardapio,
        data,
        versao
    )
    VALUES                (21, 1, '2026-09-01', '3.0'),
    (22, 2, '2026-09-01', '3.0'),
    (23, 3, '2026-09-01', '3.0'),
    (24, 4, '2026-09-01', '3.0'),
    (25, 5, '2026-09-01', '3.0'),
    (26, 6, '2026-09-01', '3.0'),
    (27, 7, '2026-09-01', '3.0'),
    (28, 8, '2026-09-01', '3.0'),
    (29, 9, '2026-09-01', '3.0'),
    (30, 10, '2026-09-01', '3.0'),
    (31, 11, '2026-09-01', '3.0'),
    (32, 12, '2026-09-01', '3.0'),
    (33, 13, '2026-09-01', '3.0'),
    (34, 14, '2026-09-01', '3.0'),
    (35, 15, '2026-09-01', '3.0');
    -- ============================================================
    -- 7. RELAÇÃO ITEM CARDÁPIO × INGREDIENTES
    -- ============================================================
    -- X-Burger
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (1, 1, 1),
    (2, 1, 2),
    (3, 1, 3),
    (4, 1, 11);
    -- X-Salada
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (5, 2, 1),
    (6, 2, 2),
    (7, 2, 3),
    (8, 2, 5),
    (9, 2, 6),
    (10, 2, 11);
    -- X-Bacon
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (11, 3, 1),
    (12, 3, 2),
    (13, 3, 3),
    (14, 3, 7),
    (15, 3, 11);
    -- X-Egg
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (16, 4, 1),
    (17, 4, 2),
    (18, 4, 3),
    (19, 4, 8),
    (20, 4, 11);
    -- X-Tudo
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (21, 5, 1),
    (22, 5, 2),
    (23, 5, 3),
    (24, 5, 4),
    (25, 5, 5),
    (26, 5, 6),
    (27, 5, 7),
    (28, 5, 8),
    (29, 5, 12);
    -- X-Frango
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (30, 6, 1),
    (31, 6, 13),
    (32, 6, 3),
    (33, 6, 5),
    (34, 6, 6),
    (35, 6, 14);
    -- X-Calabresa
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (36, 7, 1),
    (37, 7, 15),
    (38, 7, 3),
    (39, 7, 12),
    (40, 7, 11);
    -- Hot Dog Especial
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (41, 8, 16),
    (42, 8, 17),
    (43, 8, 18),
    (44, 8, 19),
    (45, 8, 11);
    -- Batata Frita P
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (46, 9, 9);
    -- Batata Frita G
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (47, 10, 9);
    -- Refrigerante Lata
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (48, 11, 10);
    -- Água Mineral
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (49, 12, 20);
    -- Combo X-Burger
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (50, 13, 1),
    (51, 13, 2),
    (52, 13, 3),
    (53, 13, 9),
    (54, 13, 10);
    -- Combo X-Bacon
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (55, 14, 1),
    (56, 14, 2),
    (57, 14, 3),
    (58, 14, 7),
    (59, 14, 9),
    (60, 14, 10);
    -- Combo X-Frango
    INSERT  INTO itemIngredienteCardapio (
        id,
        iditensCardapio,
        idingredientes
    )
    VALUES                              (61, 15, 1),
    (62, 15, 13),
    (63, 15, 3),
    (64, 15, 9),
    (65, 15, 10);
    -- ============================================================
    -- 8. ATUALIZAÇÃO DAS SEQUENCES
    -- ============================================================
    SELECT setval(pg_get_serial_sequence('clientes', 'id'), COALESCE ((SELECT MAX(id)
                                                                       FROM   clientes), 1));
    SELECT setval(pg_get_serial_sequence('ingredientes', 'id'), COALESCE ((SELECT MAX(id)
                                                                           FROM   ingredientes), 1));
    SELECT setval(pg_get_serial_sequence('itensCardapio', 'id'), COALESCE ((SELECT MAX(id)
                                                                            FROM   itensCardapio), 1));
    SELECT setval(pg_get_serial_sequence('itensPedido', 'id'), COALESCE ((SELECT MAX(id)
                                                                          FROM   itensPedido), 1));
    SELECT setval(pg_get_serial_sequence('pedidos', 'id'), COALESCE ((SELECT MAX(id)
                                                                      FROM   pedidos), 1));
    SELECT setval(pg_get_serial_sequence('cardapios', 'id'), COALESCE ((SELECT MAX(id)
                                                                        FROM   cardapios), 1));
    SELECT setval(pg_get_serial_sequence('itemIngredienteCardapio', 'id'), COALESCE ((SELECT MAX(id)
                                                                                      FROM   itemIngredienteCardapio), 1));
END;

COMMIT TRANSACTION;