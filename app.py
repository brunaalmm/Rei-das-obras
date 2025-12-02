from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Usuario, Cliente, Fornecedor
from flask_bcrypt import Bcrypt
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_123"

# Configuração do MySQL com URL encode para caracteres especiais
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/erp_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40118@localhost/erp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
bcrypt = Bcrypt(app)
db.init_app(app)

# Registra o blueprint do cliente
from clientes import clientes_bp
app.register_blueprint(clientes_bp)

# Registra o blueprint do usuário
from usuarios import usuarios_bp 
app.register_blueprint(usuarios_bp)

# Registra o blueprint dos produtos
from produtos import produtos_bp
app.register_blueprint(produtos_bp)

# Registra o blueprint do pedido
from pedidos import pedidos_bp
app.register_blueprint(pedidos_bp)

# Registra o blueprint do fornecedores
from fornecedores import fornecedores_bp
app.register_blueprint(fornecedores_bp)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Contagens básicas
    total_clientes = db.session.execute(text("SELECT COUNT(*) FROM clientes")).scalar()
    total_fornecedores = db.session.execute(text("SELECT COUNT(*) FROM fornecedores")).scalar()
    total_pedidos = db.session.execute(text("SELECT COUNT(*) FROM pedidos")).scalar()
    result = db.session.execute(text("SELECT COUNT(*) AS total_produtos, SUM(estoque) AS total_estoque FROM produtos")).first()

    total_produtos = result.total_produtos or 0

    # Consulta para gráfico de vendas por categoria
    vendas_categoria = db.session.execute(text("""
        SELECT c.nome AS categoria, SUM(ip.quantidade) AS total
        FROM itens_pedido ip
        JOIN produtos p ON ip.produto_id = p.id
        JOIN categorias c ON p.categoria_id = c.id
        GROUP BY c.nome
    """)).fetchall()

    categorias = [row[0] for row in vendas_categoria]
    totais_categoria = [row[1] or 0 for row in vendas_categoria]

    # Consulta para pegar produtos com estoque menor que 50
    estoque_baixo = db.session.execute(text("SELECT nome, estoque FROM produtos WHERE estoque < 50")).fetchall()

    return render_template(
    "index.html",
    total_clientes=total_clientes,
    total_pedidos=total_pedidos,
    total_produtos=total_produtos,
    total_estoque=result.total_estoque or 0,
    total_fornecedores=total_fornecedores,
    categorias=categorias,
    totais_categoria=totais_categoria,
    estoque_baixo=estoque_baixo,
    username_usuario=session.get('nome_completo') 
)

@app.route("/api/vendas_por_categoria")
def vendas_por_categoria_api():
    vendas_categoria = db.session.execute(text("""
        SELECT c.nome AS categoria, SUM(ip.quantidade) AS total
        FROM itens_pedido ip
        JOIN produtos p ON ip.produto_id = p.id
        JOIN categorias c ON p.categoria_id = c.id
        GROUP BY c.nome
    """)).fetchall()

    dados = {
        "categorias": [row[0] for row in vendas_categoria],
        "totais": [row[1] or 0 for row in vendas_categoria]
    }

    return jsonify(dados)

# Rotas de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = username
            session['nome_completo'] = user.nome  # <-- adiciona aqui o nome completo
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro="Usuário ou senha inválidos")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/perfil')
def perfil():
    user = {
        'nome': 'Administrador',
        'foto_url': url_for('static', filename='img/default-user-image.png') 
    }
    return render_template('perfil.html', user=user)

# Cria as tabelas e insere usuário admin
with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(username='admin').first():
        hashed_password = bcrypt.generate_password_hash('123456').decode('utf-8')
        admin = Usuario(username='admin', nome='Administrador', password=hashed_password)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)