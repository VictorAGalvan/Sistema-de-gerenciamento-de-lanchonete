CREATE TABLE clientes (
       id       SERIAL  PRIMARY KEY,
       nome     VARCHAR NOT NULL,
       cpf      VARCHAR NOT NULL,
       telefone VARCHAR,
       senha    VARCHAR NOT NULL DEFAULT 'trocar123',
       UNIQUE (cpf)
);

CREATE TABLE ingredientes (
       id         SERIAL  PRIMARY KEY,
       nome       VARCHAR NOT NULL,
       unidade    VARCHAR NOT NULL,
       quantidade INT     NOT NULL
);

CREATE TABLE itensCardapio (
       id        SERIAL          PRIMARY KEY,
       nome      VARCHAR         NOT NULL,
       preco     NUMERIC (10, 2) NOT NULL,
       categoria VARCHAR         NOT NULL
);

CREATE TABLE itensPedido (
       id              SERIAL  PRIMARY KEY,
       idpedido        INT,
       iditensCardapio INT     NOT NULL,
       quantidade      INT     NOT NULL,
       observacao      VARCHAR
);

CREATE TABLE pedidos (
       id         SERIAL PRIMARY KEY,
       idclientes INT   ,
       mesa       INT,
       estado     CHAR   NOT NULL
);

CREATE TABLE cardapios (
       id              SERIAL  PRIMARY KEY,
       iditensCardapio INT    ,
       data            DATE    NOT NULL,
       versao          VARCHAR NOT NULL
);

CREATE TABLE itemIngredienteCardapio (
       id              SERIAL PRIMARY KEY,
       iditensCardapio INT    NOT NULL,
       idingredientes  INT    NOT NULL
);

CREATE TABLE itemIngredienteItensPedido (
       id            SERIAL PRIMARY KEY,
       iditensPedido INT    NOT NULL,
       idingredientes INT   NOT NULL
);

ALTER TABLE pedidos
       ADD FOREIGN KEY (idclientes) REFERENCES clientes (id);

ALTER TABLE itensPedido
       ADD FOREIGN KEY (iditensCardapio) REFERENCES itensCardapio (id);

ALTER TABLE itensPedido
       ADD FOREIGN KEY (idpedido) REFERENCES pedidos (id);

ALTER TABLE cardapios
       ADD FOREIGN KEY (iditensCardapio) REFERENCES itensCardapio (id);

ALTER TABLE itemIngredienteCardapio
       ADD FOREIGN KEY (iditensCardapio) REFERENCES itensCardapio (id);

ALTER TABLE itemIngredienteCardapio
       ADD FOREIGN KEY (idingredientes) REFERENCES ingredientes (id);

ALTER TABLE itemIngredienteItensPedido
       ADD FOREIGN KEY (iditensPedido) REFERENCES itensPedido (id);

ALTER TABLE itemIngredienteItensPedido
       ADD FOREIGN KEY (idingredientes) REFERENCES ingredientes (id);