from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Produto, Categoria, Unidade, Fornecedor

# Cria o blueprint
produtos_bp = Blueprint('produtos_bp', __name__)

# -----------------------------
# API: Buscar produto por código de barras
# -----------------------------
@produtos_bp.route('/api/produtos/barcode/<codigo>', methods=['GET'])
def buscar_produto_codigo(codigo):
    produto = Produto.query.filter_by(codigo_barras=codigo).first()
    if produto:
        return jsonify({
            "id": produto.id,
            "nome": produto.nome,
            "descricao": produto.descricao,
            "preco": produto.preco,
            "estoque": produto.estoque,
            "codigo_barras": produto.codigo_barras,
            "categoria_id": produto.categoria_id,
            "unidade_id": produto.unidade_id,
            "fornecedor_id": produto.fornecedor_id
        })
    return jsonify({"erro": "Produto não encontrado"}), 404

# -----------------------------
# CRUD Produtos
# -----------------------------

# Listar produtos
@produtos_bp.route('/produtos')
def produtos():
    produtos_lista = Produto.query.all()
    return render_template('produtos.html', produtos=produtos_lista)

# Formulário para novo produto
@produtos_bp.route('/produtos/novo')
def novo_produto():
    categorias = Categoria.query.all()
    unidades = Unidade.query.all()
    fornecedores = Fornecedor.query.all()
    return render_template(
        'produto_form.html',
        produto=None,
        categorias=categorias,
        unidades=unidades,
        fornecedores=fornecedores
    )

# Salvar produto novo
@produtos_bp.route('/produtos/salvar', methods=['POST'])
def salvar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])
    codigo_barras = request.form.get('codigo_barras', '').strip()
    categoria_id = request.form.get('categoria_id')
    unidade_id = request.form.get('unidade_id')
    fornecedor_id = request.form.get('fornecedor_id')
    
    # Se não fornecer código de barras, gera automaticamente
    if not codigo_barras:
        # Pega o próximo ID disponível
        ultimo_produto = Produto.query.order_by(Produto.id.desc()).first()
        proximo_id = (ultimo_produto.id + 1) if ultimo_produto else 1
        codigo_barras = f"PB{proximo_id:04d}"

    produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco,
        estoque=estoque,
        codigo_barras=codigo_barras,
        categoria_id=categoria_id if categoria_id else None,
        unidade_id=unidade_id if unidade_id else None,
        fornecedor_id=fornecedor_id if fornecedor_id else None
    )
    db.session.add(produto)
    db.session.commit()
    
    # Gera imagem do código de barras automaticamente
    from barcode import get_barcode_class
    from barcode.writer import ImageWriter
    import os
    
    PASTA_BARCODES = "static/barcodes"
    os.makedirs(PASTA_BARCODES, exist_ok=True)
    
    barcode_class = get_barcode_class('code128')
    codigo_barra = barcode_class(codigo_barras, writer=ImageWriter())
    caminho_arquivo = os.path.join(PASTA_BARCODES, f"{codigo_barras}.png")
    codigo_barra.save(caminho_arquivo)
    
    return redirect(url_for('produtos_bp.produtos'))

# Formulário para editar produto
@produtos_bp.route('/produtos/editar/<int:id>')
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.all()
    unidades = Unidade.query.all()
    fornecedores = Fornecedor.query.all()
    return render_template(
        'produto_form.html',
        produto=produto,
        categorias=categorias,
        unidades=unidades,
        fornecedores=fornecedores
    )

# Atualizar produto existente
@produtos_bp.route('/produtos/atualizar', methods=['POST'])
def atualizar_produto():
    id = request.form['id']
    produto = Produto.query.get_or_404(id)

    produto.nome = request.form['nome']
    produto.descricao = request.form['descricao']
    produto.preco = float(request.form['preco'])
    produto.estoque = int(request.form['estoque'])
    
    # Preserva o código de barras existente se não fornecer novo
    novo_codigo = request.form.get('codigo_barras', '').strip()
    if novo_codigo and novo_codigo != produto.codigo_barras:
        produto.codigo_barras = novo_codigo
        
        # Gera nova imagem
        from barcode import get_barcode_class
        from barcode.writer import ImageWriter
        import os
        
        PASTA_BARCODES = "static/barcodes"
        os.makedirs(PASTA_BARCODES, exist_ok=True)
        
        barcode_class = get_barcode_class('code128')
        codigo_barra = barcode_class(novo_codigo, writer=ImageWriter())
        caminho_arquivo = os.path.join(PASTA_BARCODES, f"{novo_codigo}.png")
        codigo_barra.save(caminho_arquivo)
    
    produto.categoria_id = request.form.get('categoria_id') or None
    produto.unidade_id = request.form.get('unidade_id') or None
    produto.fornecedor_id = request.form.get('fornecedor_id') or None

    db.session.commit()
    return redirect(url_for('produtos_bp.produtos'))

# Excluir produto
@produtos_bp.route('/produtos/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    
    # Remove a imagem do código de barras se existir
    import os
    if produto.codigo_barras:
        caminho_imagem = os.path.join("static/barcodes", f"{produto.codigo_barras}.png")
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)
    
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos_bp.produtos'))