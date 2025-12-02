from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cpf_cnpj = db.Column(db.String(20))
    tipo_cliente = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    endereco = db.Column(db.String(200))
    cep = db.Column(db.String(9))

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(100), nullable=False)
    nome_fantasia = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cpf_cnpj = db.Column(db.String(20))
    tipo_fornecedor = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cep = db.Column(db.String(9))

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

class Unidade(db.Model):
    __tablename__ = 'unidades'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    codigo_barras = db.Column(db.String(50), unique=True)  # Alterado para 50 caracteres
    
    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='produtos')
    categoria = db.relationship('Categoria', backref='produtos')
    unidade = db.relationship('Unidade', backref='produtos')

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_pedido = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    
    cliente = db.relationship('Cliente', backref='pedidos')

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    
    pedido = db.relationship('Pedido', backref='itens')
    produto = db.relationship('Produto', backref='itens_pedido')

class Login(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_login = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    usuario = db.relationship('Usuario', backref='logins')