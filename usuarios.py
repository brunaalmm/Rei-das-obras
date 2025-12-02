from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/usuarios')
def usuarios():
    usuarios_lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios_lista)

@usuarios_bp.route('/usuarios/novo')
def novo():
    return render_template('usuario_form.html', usuario=None)

@usuarios_bp.route('/usuarios/salvar', methods=['POST'])
def salvar():
    username = request.form['username']
    nome = request.form['nome']
    password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Validação opcional:
    if not nome:
        return "O campo nome é obrigatório!", 400

    usuario = Usuario(
        username=username,
        nome=nome,  
        password=hashed_password
    )

    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuarios_bp.usuarios'))

@usuarios_bp.route('/usuarios/editar/<int:id>')
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('usuario_form.html', usuario=usuario)

@usuarios_bp.route('/usuarios/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    usuario = Usuario.query.get_or_404(id)

    usuario.username = request.form['username']
    usuario.nome = request.form['nome']

    # Apenas atualiza a senha se preenchida
    if request.form['password']:
        usuario.password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    db.session.commit()
    return redirect(url_for('usuarios_bp.usuarios'))

@usuarios_bp.route('/usuarios/excluir/<int:id>')
def excluir(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios_bp.usuarios'))