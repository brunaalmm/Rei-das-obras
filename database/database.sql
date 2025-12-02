CREATE DATABASE erp_db;

USE erp_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    nome varchar(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    cpf_cnpj VARCHAR(20),
    tipo_cliente VARCHAR(20),
    data_nascimento DATE,
    endereco VARCHAR(200),
    cep VARCHAR(9)
);

CREATE TABLE fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    razao_social VARCHAR(100) NOT NULL,
    nome_fantasia VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    cpf_cnpj VARCHAR(20),
    tipo_fornecedor VARCHAR(20),
    endereco VARCHAR(200),
    cep VARCHAR(9)
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO categorias (nome) VALUES
('Materiais básicos'),
('Tintas'),
('EPI’s'),
('Pisos e revestimentos');

CREATE TABLE unidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO unidades (nome) VALUES
('kg'),
('m²'),
('cx'),
('un');

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fornecedor_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT DEFAULT NULL,
    preco float NOT NULL,
    estoque INT NOT NULL,
    categoria_id INT,
    unidade_id INT,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (unidade_id) REFERENCES unidades(id)
);

CREATE TABLE pedidos (
    id int(11) NOT NULL AUTO_INCREMENT,
    cliente_id int(11) NOT NULL,
    data_pedido datetime DEFAULT NULL,
    status varchar(20) DEFAULT NULL,
    PRIMARY KEY (id),
    KEY cliente_id (cliente_id),
    CONSTRAINT pedidos_ibfk_1 FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

CREATE TABLE itens_pedido (
    id int(11) NOT NULL AUTO_INCREMENT,
    pedido_id int(11) NOT NULL,
    produto_id int(11) NOT NULL,
    quantidade int(11) NOT NULL,
    preco_unitario float NOT NULL,
    PRIMARY KEY (id),
    KEY pedido_id (pedido_id),
    KEY produto_id (produto_id),
    CONSTRAINT itens_pedido_ibfk_1 FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
    CONSTRAINT itens_pedido_ibfk_2 FOREIGN KEY (produto_id) REFERENCES produtos (id)
);

CREATE TABLE logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data_login DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);