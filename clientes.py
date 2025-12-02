from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Cliente

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route('/clientes')
def clientes():
    clientes_lista = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes_lista)

@clientes_bp.route('/clientes/novo')
def novo():
    return render_template('cliente_form.html', cliente=None)

@clientes_bp.route('/clientes/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cpf_cnpj = request.form.get('cpf_cnpj')
    tipo_cliente = request.form.get('tipo_cliente')
    data_nascimento = request.form.get('data_nascimento')
    endereco = request.form.get('endereco')
    cep = request.form.get('cep')

    # Convertendo data_nascimento para datetime.date se for informada
    from datetime import datetime
    if data_nascimento:
        data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    else:
        data_nascimento = None

    cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        cpf_cnpj=cpf_cnpj,
        tipo_cliente=tipo_cliente,
        data_nascimento=data_nascimento,
        endereco=endereco,
        cep=cep
    )
    db.session.add(cliente)
    db.session.commit()
    return redirect(url_for('clientes_bp.clientes'))

@clientes_bp.route('/clientes/editar/<int:id>')
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('cliente_form.html', cliente=cliente)

@clientes_bp.route('/clientes/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    cliente = Cliente.query.get_or_404(id)
    cliente.nome = request.form['nome']
    cliente.email = request.form['email']
    cliente.telefone = request.form['telefone']
    cliente.cpf_cnpj = request.form.get('cpf_cnpj')
    cliente.tipo_cliente = request.form.get('tipo_cliente')
    data_nascimento = request.form.get('data_nascimento')

    from datetime import datetime
    if data_nascimento:
        cliente.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    else:
        cliente.data_nascimento = None

    cliente.endereco = request.form.get('endereco')
    cliente.cep = request.form.get('cep')

    db.session.commit()
    return redirect(url_for('clientes_bp.clientes'))

@clientes_bp.route('/clientes/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get_or_404(id)

    if cliente.pedidos:
        flash("Não é possível excluir este cliente porque ele possui pedidos vinculados.", "danger")
        return redirect(url_for('clientes_bp.clientes'))

    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente excluído com sucesso!", "success")
    return redirect(url_for('clientes_bp.clientes'))