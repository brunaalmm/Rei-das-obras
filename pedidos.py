from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Pedido, ItemPedido, Cliente, Produto

pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route('/pedidos/novo', methods=['GET', 'POST'])
def novo_pedido():
    if request.method == 'POST':
        cliente_id = request.form.getlist('cliente_id')
        produtos_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')

        # Criar o pedido
        pedido = Pedido(cliente_id=cliente_id)
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID antes do commit

        # Adicionar os itens do pedido
        for pid, qtd in zip(produtos_ids, quantidades):
            qtd_int = int(qtd)
            produto = Produto.query.get_or_404(pid)

            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=pid,
                quantidade=qtd_int,
                preco_unitario=produto.preco
            )
            db.session.add(item)

        db.session.commit()
        flash("Pedido criado com sucesso!", "success")
        return redirect(url_for('pedidos_bp.pedidos'))

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('pedido_form.html', clientes=clientes, produtos=produtos, pedido=None)

@pedidos_bp.route('/pedidos/editar/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    if request.method == 'POST':
        pedido.cliente_id = request.form['cliente_id']
        produtos_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')

        # Remover itens antigos do pedido
        ItemPedido.query.filter_by(pedido_id=id).delete()

        # Adicionar novos itens
        for pid, qtd in zip(produtos_ids, quantidades):
            qtd_int = int(qtd)
            produto = Produto.query.get_or_404(pid)

            item = ItemPedido(
                pedido_id=id,
                produto_id=pid,
                quantidade=qtd_int,
                preco_unitario=produto.preco
            )
            db.session.add(item)

        db.session.commit()
        flash("Pedido editado com sucesso!", "success")
        return redirect(url_for('pedidos_bp.pedidos'))

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    itens_selecionados = {item.produto_id: item.quantidade for item in pedido.itens}
    return render_template('pedido_form.html', clientes=clientes, produtos=produtos, pedido=pedido, itens_selecionados=itens_selecionados)

@pedidos_bp.route('/pedidos/excluir/<int:id>')
def excluir_pedido(id):
    try:
        pedido = Pedido.query.get_or_404(id)
        
        # Conta quantos itens tem no pedido
        qtd_itens = ItemPedido.query.filter_by(pedido_id=id).count()
        
        # Excluir todos os itens do pedido antes de apagar o pedido
        ItemPedido.query.filter_by(pedido_id=id).delete()
        
        # Excluir o pedido
        db.session.delete(pedido)
        db.session.commit()
        
        flash(f"Pedido #{id} excluído com sucesso! {qtd_itens} itens foram removidos.", "success")
        return redirect(url_for('pedidos_bp.pedidos'))
    
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir pedido #{id}: {str(e)}", "error")
        return redirect(url_for('pedidos_bp.pedidos'))

@pedidos_bp.route('/pedidos')
def pedidos():
    pedidos_lista = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos_lista)