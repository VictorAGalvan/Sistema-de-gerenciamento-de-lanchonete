CREATE TABLE clientes (
       id       SERIAL  PRIMARY KEY NOT NULL,
       nome     VARCHAR NOT NULL,
       cpf      VARCHAR NOT NULL,
       telefone VARCHAR NOT NULL,
       email    VARCHAR,
       UNIQUE (cpf)
);

CREATE TABLE pedidos (
       id         SERIAL PRIMARY KEY NOT NULL,
       idClientes INT   ,
       mesa       INT    NOT NULL
);

CREATE TABLE cardapios (
       id     SERIAL PRIMARY KEY NOT NULL,
       data   DATE   NOT NULL,
       versao INT    NOT NULL
);

CREATE TABLE itens (
       id        SERIAL  PRIMARY KEY NOT NULL,
       preco     FLOAT   NOT NULL,
       categoria CHAR    NOT NULL,
       nome      VARCHAR NOT NULL
);

CREATE TABLE Ingredientes (
       id         SERIAL  PRIMARY KEY NOT NULL,
       nome       VARCHAR NOT NULL,
       unidade    INT     NOT NULL,
       quantidade INT     NOT NULL
);

CREATE TABLE itensPedidos (
       -- id SERIAL PRIMARY KEY NOT NULL,
       idItens    INT     NOT NULL,
       idPedidos  INT     NOT NULL,
       quantidade INT     NOT NULL,
       observacao VARCHAR
);

CREATE TABLE itensCardapio (
       -- id SERIAL PRIMARY KEY NOT NULL,
       idCardapio INT NOT NULL,
       idItens    INT NOT NULL
);

CREATE TABLE itensIngredientes (
       -- id SERIAL PRIMARY KEY NOT NULL,
       idIngredientes INT NOT NULL,
       idItens        INT NOT NULL
);

ALTER TABLE pedidos
       ADD FOREIGN KEY (idClientes) REFERENCES clientes (id);

ALTER TABLE itensPedidos
       ADD FOREIGN KEY (idItens) REFERENCES itens (id);

ALTER TABLE itensPedidos
       ADD FOREIGN KEY (idPedidos) REFERENCES pedidos (id);

ALTER TABLE itensCardapio
       ADD FOREIGN KEY (idCardapio) REFERENCES cardapios (id);

ALTER TABLE itensCardapio
       ADD FOREIGN KEY (idItens) REFERENCES itens (id);

ALTER TABLE itensIngredientes
       ADD FOREIGN KEY (idIngredientes) REFERENCES Ingredientes (id);

ALTER TABLE itensIngredientes
       ADD FOREIGN KEY (idItens) REFERENCES itens (id);

-- TESTES
BEGIN
       -- ============================================================
       -- 1. CLIENTES
       -- ============================================================
       INSERT INTO clientes (
              nome,
              cpf,
              telefone,
              email
       )
       SELECT 'João da Silva',
              '11111111111',
              '54999990001',
              'joao@email.com'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   clientes
                          WHERE  cpf = '11111111111');
       INSERT INTO clientes (
              nome,
              cpf,
              telefone,
              email
       )
       SELECT 'Maria Oliveira',
              '22222222222',
              '54999990002',
              'maria@email.com'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   clientes
                          WHERE  cpf = '22222222222');
       INSERT INTO clientes (
              nome,
              cpf,
              telefone,
              email
       )
       SELECT 'Carlos Souza',
              '33333333333',
              '54999990003',
              'carlos@email.com'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   clientes
                          WHERE  cpf = '33333333333');
       INSERT INTO clientes (
              nome,
              cpf,
              telefone,
              email
       )
       SELECT 'Ana Pereira',
              '44444444444',
              '54999990004',
              'ana@email.com'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   clientes
                          WHERE  cpf = '44444444444');
       -- ============================================================
       -- 2. ITENS DO CARDÁPIO
       -- ============================================================
       INSERT INTO itens (
              preco,
              categoria,
              nome
       )
       SELECT 25.90,
              'L',
              'Hambúrguer Artesanal'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   itens
                          WHERE  nome = 'Hambúrguer Artesanal');
       INSERT INTO itens (
              preco,
              categoria,
              nome
       )
       SELECT 18.90,
              'L',
              'X-Bacon'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   itens
                          WHERE  nome = 'X-Bacon');
       INSERT INTO itens (
              preco,
              categoria,
              nome
       )
       SELECT 12.00,
              'B',
              'Batata Frita'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   itens
                          WHERE  nome = 'Batata Frita');
       INSERT INTO itens (
              preco,
              categoria,
              nome
       )
       SELECT 8.50,
              'B',
              'Refrigerante Lata'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   itens
                          WHERE  nome = 'Refrigerante Lata');
       INSERT INTO itens (
              preco,
              categoria,
              nome
       )
       SELECT 22.90,
              'S',
              'Milk Shake'
       WHERE  NOT EXISTS (SELECT 1
                          FROM   itens
                          WHERE  nome = 'Milk Shake');
       -- ============================================================
       -- 3. INGREDIENTES
       -- ============================================================
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Pão de hambúrguer',
              1,
              100
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Pão de hambúrguer');
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Carne bovina',
              1,
              100
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Carne bovina');
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Bacon',
              1,
              80
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Bacon');
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Queijo',
              1,
              100
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Queijo');
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Batata',
              1,
              200
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Batata');
       INSERT INTO Ingredientes (
              nome,
              unidade,
              quantidade
       )
       SELECT 'Leite',
              1,
              100
       WHERE  NOT EXISTS (SELECT 1
                          FROM   Ingredientes
                          WHERE  nome = 'Leite');
       -- ============================================================
       -- 4. CARDÁPIO
       -- ============================================================
       INSERT INTO cardapios (
              data,
              versao
       )
       SELECT CURRENT_DATE,
              1
       WHERE  NOT EXISTS (SELECT 1
                          FROM   cardapios
                          WHERE  data = CURRENT_DATE
                                 AND versao = 1);
       -- ============================================================
       -- 5. PEDIDOS
       -- ============================================================
       -- Pedido do João - Mesa 1
       INSERT INTO pedidos (
              idClientes,
              mesa
       )
       SELECT p.id,
              1
       FROM   clientes AS p
       WHERE  p.cpf = '11111111111'
              AND NOT EXISTS (SELECT 1
                              FROM   pedidos AS pe
                              WHERE  pe.idClientes = p.id
                                     AND pe.mesa = 1);
       -- Pedido da Maria - Mesa 2
       INSERT INTO pedidos (
              idClientes,
              mesa
       )
       SELECT p.id,
              2
       FROM   clientes AS p
       WHERE  p.cpf = '22222222222'
              AND NOT EXISTS (SELECT 1
                              FROM   pedidos AS pe
                              WHERE  pe.idClientes = p.id
                                     AND pe.mesa = 2);
       -- Pedido do Carlos - Mesa 3
       INSERT INTO pedidos (
              idClientes,
              mesa
       )
       SELECT p.id,
              3
       FROM   clientes AS p
       WHERE  p.cpf = '33333333333'
              AND NOT EXISTS (SELECT 1
                              FROM   pedidos AS pe
                              WHERE  pe.idClientes = p.id
                                     AND pe.mesa = 3);
       -- Pedido da Ana - Mesa 4
       INSERT INTO pedidos (
              idClientes,
              mesa
       )
       SELECT p.id,
              4
       FROM   clientes AS p
       WHERE  p.cpf = '44444444444'
              AND NOT EXISTS (SELECT 1
                              FROM   pedidos AS pe
                              WHERE  pe.idClientes = p.id
                                     AND pe.mesa = 4);
       -- ============================================================
       -- 6. ITENS DO CARDÁPIO
       -- ============================================================
       INSERT INTO itensCardapio (
              idCardapio,
              idItens
       )
       SELECT c.id,
              i.id
       FROM   cardapios AS c CROSS JOIN itens AS i
       WHERE  c.data = CURRENT_DATE
              AND c.versao = 1
              AND i.nome IN ('Hambúrguer Artesanal', 'X-Bacon', 'Batata Frita', 'Refrigerante Lata', 'Milk Shake')
              AND NOT EXISTS (SELECT 1
                              FROM   itensCardapio AS ic
                              WHERE  ic.idCardapio = c.id
                                     AND ic.idItens = i.id);
       -- ============================================================
       -- 7. ITENS + INGREDIENTES
       -- ============================================================
       -- Hambúrguer Artesanal -> Pão
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Pão de hambúrguer'
              AND i.nome = 'Hambúrguer Artesanal'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- Hambúrguer Artesanal -> Carne
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Carne bovina'
              AND i.nome = 'Hambúrguer Artesanal'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- Hambúrguer Artesanal -> Queijo
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Queijo'
              AND i.nome = 'Hambúrguer Artesanal'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- X-Bacon -> Pão
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Pão de hambúrguer'
              AND i.nome = 'X-Bacon'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- X-Bacon -> Carne
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Carne bovina'
              AND i.nome = 'X-Bacon'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- X-Bacon -> Bacon
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Bacon'
              AND i.nome = 'X-Bacon'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- X-Bacon -> Queijo
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Queijo'
              AND i.nome = 'X-Bacon'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- Batata Frita -> Batata
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Batata'
              AND i.nome = 'Batata Frita'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- Milk Shake -> Leite
       INSERT INTO itensIngredientes (
              idIngredientes,
              idItens
       )
       SELECT ing.id,
              i.id
       FROM   Ingredientes AS ing CROSS JOIN itens AS i
       WHERE  ing.nome = 'Leite'
              AND i.nome = 'Milk Shake'
              AND NOT EXISTS (SELECT 1
                              FROM   itensIngredientes AS ii
                              WHERE  ii.idIngredientes = ing.id
                                     AND ii.idItens = i.id);
       -- ============================================================
       -- 8. PEDIDOS + ITENS
       -- ============================================================
       -- João / Mesa 1
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'Hambúrguer Artesanal'
              AND pe.cpf = '11111111111'
              AND p.mesa = 1
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'Batata Frita'
              AND pe.cpf = '11111111111'
              AND p.mesa = 1
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
       -- Maria / Mesa 2
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'X-Bacon'
              AND pe.cpf = '22222222222'
              AND p.mesa = 2
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'Refrigerante Lata'
              AND pe.cpf = '22222222222'
              AND p.mesa = 2
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
       -- Carlos / Mesa 3
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'Milk Shake'
              AND pe.cpf = '33333333333'
              AND p.mesa = 3
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
       -- Ana / Mesa 4
       INSERT INTO itensPedidos (
              idItens,
              idPedidos,
              quantidade,
              observacao
       )
       SELECT i.id,
              p.id,
              1,
              NULL
       FROM   itens AS i CROSS JOIN pedidos AS p
              INNER JOIN
              clientes AS pe
              ON pe.id = p.idClientes
       WHERE  i.nome = 'Hambúrguer Artesanal'
              AND pe.cpf = '44444444444'
              AND p.mesa = 4
              AND NOT EXISTS (SELECT 1
                              FROM   itensPedidos AS ip
                              WHERE  ip.idItens = i.id
                                     AND ip.idPedidos = p.id);
END

COMMIT TRANSACTION;