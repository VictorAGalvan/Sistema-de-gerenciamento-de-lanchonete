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
    INSERT INTO itensCardapio (id, nome, preco, categoria, idcardapio) VALUES
(1, 'X-Burger', 18.90, 'Hambúrguer', 3),
(2, 'X-Salada', 20.90, 'Hambúrguer', 3),
(3, 'X-Bacon', 22.90, 'Hambúrguer', 3),
(4, 'X-Egg', 21.90, 'Hambúrguer', 3),
(5, 'X-Tudo', 27.90, 'Hambúrguer', 3),
(6, 'X-Frango', 21.90, 'Hambúrguer', 3),
(7, 'X-Calabresa', 22.50, 'Hambúrguer', 3),
(8, 'Hot Dog Especial', 19.90, 'Hot Dog', 3),
(9, 'Batata Frita P', 10.90, 'Acompanhamento', 3),
(10, 'Batata Frita G', 16.90, 'Acompanhamento', 3),
(11, 'Refrigerante Lata', 6.00, 'Bebida', 3),
(12, 'Água Mineral', 4.00, 'Bebida', 3),
(13, 'Combo X-Burger', 29.90, 'Combo', 3),
(14, 'Combo X-Bacon', 33.90, 'Combo', 3),
(15, 'Combo X-Frango', 32.90, 'Combo', 3),
-- cópias para a versão 1.0
(16, 'X-Burger', 18.90, 'Hambúrguer', 1),
(17, 'X-Salada', 20.90, 'Hambúrguer', 1),
(18, 'X-Bacon', 22.90, 'Hambúrguer', 1),
(19, 'X-Egg', 21.90, 'Hambúrguer', 1),
(20, 'X-Tudo', 27.90, 'Hambúrguer', 1),
(21, 'X-Frango', 21.90, 'Hambúrguer', 1),
(22, 'X-Calabresa', 22.50, 'Hambúrguer', 1),
(23, 'Hot Dog Especial', 19.90, 'Hot Dog', 1),
-- cópias para a versão 2.0
(24, 'X-Burger', 18.90, 'Hambúrguer', 2),
(25, 'X-Salada', 20.90, 'Hambúrguer', 2),
(26, 'X-Bacon', 22.90, 'Hambúrguer', 2),
(27, 'X-Egg', 21.90, 'Hambúrguer', 2),
(28, 'X-Tudo', 27.90, 'Hambúrguer', 2),
(29, 'X-Frango', 21.90, 'Hambúrguer', 2),
(30, 'X-Calabresa', 22.50, 'Hambúrguer', 2),
(31, 'Hot Dog Especial', 19.90, 'Hot Dog', 2),
(32, 'Batata Frita P', 10.90, 'Acompanhamento', 2),
(33, 'Batata Frita G', 16.90, 'Acompanhamento', 2),
(34, 'Refrigerante Lata', 6.00, 'Bebida', 2),
(35, 'Água Mineral', 4.00, 'Bebida', 2);
    -- ============================================================
    -- 4. PEDIDOS
    -- Estados: R=Recebido, N=Na Fila, E=Em Preparo, P=Pronto
    -- ============================================================
    INSERT  INTO pedidos (
        id,
        idclientes,
        mesa,
        estado
    )
    VALUES              (1, 1, 1, 'N'),
    (2, 2, 2, 'N'),
    (3, 3, 3, 'N'),
    (4, 4, 4, 'N'),
    (5, 5, 5, 'E'),
    (6, 6, 6, 'E'),
    (7, 7, 7, 'P'),
    (8, 8, 8, 'P'),
    (9, 9, 9, 'N'),
    (10, 10, 10, 'N'),
    (11, 11, 1, 'E'),
    (12, 12, 2, 'P'),
    (13, 13, 3, 'N'),
    (14, 14, 4, 'N'),
    (15, 15, 5, 'E'),
    (16, 16, 6, 'P'),
    (17, 17, 7, 'N'),
    (18, 18, 8, 'E'),
    (19, 19, 9, 'P'),
    (20, 20, 10, 'N'),
    (21, 21, 1, 'N'),
    (22, 22, 2, 'E'),
    (23, 23, 3, 'P'),
    (24, 24, 4, 'N'),
    (25, 25, 5, 'E'),
    (26, 1, 6, 'P'),
    (27, 2, 7, 'N'),
    (28, 3, 8, 'E'),
    (29, 4, 9, 'P'),
    (30, 5, 10, 'N');
    -- ============================================================
    -- 5. ITENS DOS PEDIDOS
    -- 60 itens, com idpedido preenchido
    -- ============================================================
    INSERT INTO itensPedido (id, idpedido, iditensCardapio, quantidade, observacao) VALUES
    (1, 1, 1, 2, 'Sem cebola'),
    (2, 1, 9, 1, NULL),
    (3, 2, 3, 1, 'Adicionar queijo'),
    (4, 2, 11, 2, 'Sem gelo'),
    (5, 3, 2, 1, 'Sem tomate'),
    (6, 3, 10, 1, NULL),
    (7, 3, 11, 1, NULL),
    (8, 4, 5, 1, 'Carne bem passada'),
    (9, 4, 12, 1, NULL),
    (10, 5, 6, 2, 'Adicionar catupiry'),
    (11, 5, 9, 1, NULL),
    (12, 6, 7, 1, 'Sem cebola'),
    (13, 6, 11, 1, 'Sem gelo'),
    (14, 7, 4, 1, 'Adicionar bacon'),
    (15, 7, 10, 1, NULL),
    (16, 8, 8, 2, 'Pouco molho'),
    (17, 8, 11, 2, NULL),
    (18, 9, 1, 1, NULL),
    (19, 9, 9, 2, NULL),
    (20, 10, 13, 2, NULL),
    (21, 10, 12, 1, NULL),
    (22, 11, 2, 1, 'Sem alface'),
    (23, 11, 11, 1, NULL),
    (24, 12, 3, 2, 'Bem passado'),
    (25, 12, 10, 1, NULL),
    (26, 13, 5, 1, 'Sem tomate e sem cebola'),
    (27, 13, 11, 1, 'Sem gelo'),
    (28, 14, 6, 1, NULL),
    (29, 14, 9, 1, NULL),
    (30, 14, 11, 1, NULL),
    (31, 15, 14, 2, NULL),
    (32, 16, 8, 1, 'Sem milho'),
    (33, 16, 12, 1, NULL),
    (34, 17, 1, 2, NULL),
    (35, 17, 10, 1, NULL),
    (36, 18, 7, 1, 'Pouco molho'),
    (37, 18, 11, 1, NULL),
    (38, 19, 4, 1, 'Sem bacon'),
    (39, 19, 9, 1, NULL),
    (40, 20, 15, 1, NULL),
    (41, 20, 11, 1, NULL),
    (42, 21, 2, 2, 'Sem cebola'),
    (43, 21, 10, 1, NULL),
    (44, 22, 3, 1, 'Adicionar ovo'),
    (45, 22, 12, 1, NULL),
    (46, 23, 5, 1, 'Carne ao ponto'),
    (47, 23, 9, 1, NULL),
    (48, 23, 11, 1, NULL),
    (49, 24, 13, 1, NULL),
    (50, 24, 11, 1, NULL),
    (51, 25, 6, 2, 'Sem tomate'),
    (52, 25, 10, 1, NULL),
    (53, 26, 8, 1, NULL),
    (54, 26, 11, 1, 'Sem gelo'),
    (55, 27, 1, 1, 'Adicionar queijo'),
    (56, 27, 9, 1, NULL),
    (57, 28, 14, 1, NULL),
    (58, 28, 12, 1, NULL),
    (59, 29, 7, 2, 'Sem cebola'),
    (60, 30, 15, 1, 'Adicionar catupiry');
    -- ============================================================
    -- 6. CARDÁPIOS
    -- 3 versões
    -- ============================================================
    INSERT INTO cardapios (id, data, versao, ativo) VALUES
    (1, '2026-07-01', '1.0', false),
    (2, '2026-08-01', '2.0', false),
    (3, '2026-09-01', '3.0', true);
    -- ============================================================
    -- 7. RELAÇÃO ITEM CARDÁPIO × INGREDIENTES
    -- ============================================================
    INSERT  INTO itemIngredienteCardapio (id, iditensCardapio, idingredientes)
    VALUES (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 11),
    (5, 2, 1), (6, 2, 2), (7, 2, 3), (8, 2, 5), (9, 2, 6), (10, 2, 11),
    (11, 3, 1), (12, 3, 2), (13, 3, 3), (14, 3, 7), (15, 3, 11),
    (16, 4, 1), (17, 4, 2), (18, 4, 3), (19, 4, 8), (20, 4, 11),
    (21, 5, 1), (22, 5, 2), (23, 5, 3), (24, 5, 4), (25, 5, 5), (26, 5, 6), (27, 5, 7), (28, 5, 8), (29, 5, 12),
    (30, 6, 1), (31, 6, 13), (32, 6, 3), (33, 6, 5), (34, 6, 6), (35, 6, 14),
    (36, 7, 1), (37, 7, 15), (38, 7, 3), (39, 7, 12), (40, 7, 11),
    (41, 8, 16), (42, 8, 17), (43, 8, 18), (44, 8, 19), (45, 8, 11),
    (46, 9, 9),
    (47, 10, 9),
    (48, 11, 10),
    (49, 12, 20),
    (50, 13, 1), (51, 13, 2), (52, 13, 3), (53, 13, 9), (54, 13, 10),
    (55, 14, 1), (56, 14, 2), (57, 14, 3), (58, 14, 7), (59, 14, 9), (60, 14, 10),
    (61, 15, 1), (62, 15, 13), (63, 15, 3), (64, 15, 9), (65, 15, 10);
    -- ============================================================
    -- 8. ATUALIZAÇÃO DAS SEQUENCES
    -- ============================================================
    SELECT setval(pg_get_serial_sequence('clientes', 'id'), COALESCE((SELECT MAX(id) FROM clientes), 1));
    SELECT setval(pg_get_serial_sequence('ingredientes', 'id'), COALESCE((SELECT MAX(id) FROM ingredientes), 1));
    SELECT setval(pg_get_serial_sequence('itensCardapio', 'id'), COALESCE((SELECT MAX(id) FROM itensCardapio), 1));
    SELECT setval(pg_get_serial_sequence('itensPedido', 'id'), COALESCE((SELECT MAX(id) FROM itensPedido), 1));
    SELECT setval(pg_get_serial_sequence('pedidos', 'id'), COALESCE((SELECT MAX(id) FROM pedidos), 1));
    SELECT setval(pg_get_serial_sequence('cardapios', 'id'), COALESCE((SELECT MAX(id) FROM cardapios), 1));
    SELECT setval(pg_get_serial_sequence('itemIngredienteCardapio', 'id'), COALESCE((SELECT MAX(id) FROM itemIngredienteCardapio), 1));
END;

COMMIT TRANSACTION;