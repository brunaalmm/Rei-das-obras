from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Fornecedor

fornecedores_bp = Blueprint('fornecedores_bp', __name__)

@fornecedores_bp.route('/fornecedores')
def fornecedores():
    fornecedores_lista = Fornecedor.query.all()
    return render_template('fornecedores.html', fornecedores=fornecedores_lista)

@fornecedores_bp.route('/fornecedores/novo')
def novo():
    return render_template('fornecedor_form.html', fornecedor=None)

@fornecedores_bp.route('/fornecedores/salvar', methods=['POST'])
def salvar():
    razao_social = request.form['razao_social']
    nome_fantasia = request.form.get('nome_fantasia')
    email = request.form['email']
    telefone = request.form.get('telefone')
    cpf_cnpj = request.form.get('cpf_cnpj')
    tipo_fornecedor = request.form.get('tipo_fornecedor')
    endereco = request.form.get('endereco')
    cep = request.form.get('cep')

    fornecedor = Fornecedor(
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        email=email,
        telefone=telefone,
        cpf_cnpj=cpf_cnpj,
        tipo_fornecedor=tipo_fornecedor,
        endereco=endereco,
        cep=cep
    )
    db.session.add(fornecedor)
    db.session.commit()
    return redirect(url_for('fornecedores_bp.fornecedores'))

@fornecedores_bp.route('/fornecedores/editar/<int:id>')
def editar(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    return render_template('fornecedor_form.html', fornecedor=fornecedor)

@fornecedores_bp.route('/fornecedores/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    fornecedor = Fornecedor.query.get_or_404(id)

    fornecedor.razao_social = request.form['razao_social']
    fornecedor.nome_fantasia = request.form.get('nome_fantasia')
    fornecedor.email = request.form['email']
    fornecedor.telefone = request.form.get('telefone')
    fornecedor.cpf_cnpj = request.form.get('cpf_cnpj')
    fornecedor.tipo_fornecedor = request.form.get('tipo_fornecedor')
    fornecedor.endereco = request.form.get('endereco')
    fornecedor.cep = request.form.get('cep')

    db.session.commit()
    return redirect(url_for('fornecedores_bp.fornecedores'))

@fornecedores_bp.route('/fornecedores/excluir/<int:id>')
def excluir(id):
    fornecedor = Fornecedor.query.get_or_404(id)

    db.session.delete(fornecedor)
    db.session.commit()
    flash("Fornecedor excluído com sucesso!", "success")
    return redirect(url_for('fornecedores_bp.fornecedores'))