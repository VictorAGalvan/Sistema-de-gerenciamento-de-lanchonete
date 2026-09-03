CREATE TABLE clientes 
( 
 id SERIAL PRIMARY KEY NOT NULL,
 nome VARCHAR NOT NULL,  
 cpf VARCHAR NOT NULL,  
 telefone VARCHAR NOT NULL,  
 email VARCHAR,  
 UNIQUE (cpf)
); 

CREATE TABLE pedidos 
( 
 id SERIAL PRIMARY KEY NOT NULL,
 idClientes INT,  
 mesa INT NOT NULL
); 

CREATE TABLE cardapios 
( 
 id SERIAL PRIMARY KEY NOT NULL,
 data DATE NOT NULL,  
 versao INT NOT NULL);

CREATE TABLE itens 
( 
 id SERIAL PRIMARY KEY NOT NULL,
 preco FLOAT NOT NULL,  
 categoria CHAR NOT NULL,  
 nome VARCHAR NOT NULL);

CREATE TABLE Ingredientes 
( 
 id SERIAL PRIMARY KEY NOT NULL,
 nome VARCHAR NOT NULL,  
 unidade INT NOT NULL,  
 quantidade INT NOT NULL);

CREATE TABLE itensPedidos 
( 
 -- id SERIAL PRIMARY KEY NOT NULL,
 idItens INT NOT NULL,  
 idPedidos INT NOT NULL
 );

CREATE TABLE itensCardapio 
( 
 -- id SERIAL PRIMARY KEY NOT NULL,
 idCardapio INT NOT NULL,  
 idItens INT NOT NULL  
); 

CREATE TABLE itensIngredientes 
( 
 -- id SERIAL PRIMARY KEY NOT NULL,
 idIngredientes INT NOT NULL,  
 idItens INT NOT NULL 
); 

ALTER TABLE pedidos ADD FOREIGN KEY(idClientes) REFERENCES clientes (id);
ALTER TABLE itensPedidos ADD FOREIGN KEY(idItens) REFERENCES itens (id);
ALTER TABLE itensPedidos ADD FOREIGN KEY(idPedidos) REFERENCES pedidos (id);
ALTER TABLE itensCardapio ADD FOREIGN KEY(idCardapio) REFERENCES cardapios (id);
ALTER TABLE itensCardapio ADD FOREIGN KEY(idItens) REFERENCES itens (id);
ALTER TABLE itensIngredientes ADD FOREIGN KEY(idIngredientes) REFERENCES Ingredientes (id);
ALTER TABLE itensIngredientes ADD FOREIGN KEY(idItens) REFERENCES itens (id);
