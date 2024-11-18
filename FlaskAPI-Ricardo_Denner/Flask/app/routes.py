from flask import render_template, request, redirect, url_for, flash,jsonify
from app import app, db
from app.models import Turma, Aluno


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastrar_turma", methods=['GET', 'POST'])
def cadastrar_turma():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nova_turma = Turma(nome=nome)
        db.session.add(nova_turma)
        db.session.commit()
        return redirect(url_for('cadastrar_turma'))  # Redirecionar para a mesma rota para recarregar a lista de turmas

    # Consulta todas as turmas e conta os alunos de cada turma
    turmas = db.session.query(
        Turma.id, Turma.nome, db.func.count(Aluno.id).label('quantidade_alunos')
    ).outerjoin(Aluno).group_by(Turma.id).all()

    return render_template('cadastrar_turma.html', turmas=turmas)

@app.route('/delete_turma/<int:turma_id>', methods=['POST'])
def delete_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if turma:
        # Verifica se a turma tem alunos
        if turma.alunos:  # Assume que você tem um relacionamento definido em Turma
            return jsonify({'message': 'A turma não pode ser excluída porque possui alunos.'}), 400
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma excluída com sucesso!'}), 200
    return jsonify({'message': 'Turma não encontrada.'}), 404


@app.route("/cadastrar_aluno", methods=['GET', 'POST'])
def cadastrar_aluno():
    # Quando o formulário for enviado via POST, cadastrar o aluno
    if request.method == 'POST':
        nome_aluno = request.form['nome']
        turma_id = request.form['turma_id']

        # Criação de um novo aluno
        novo_aluno = Aluno(nome=nome_aluno, turma_id=turma_id)
        db.session.add(novo_aluno)
        db.session.commit()

        return redirect(url_for('index'))

    # Se for um GET, carregar as turmas para exibir no formulário
    turmas = Turma.query.all()  # Busca todas as turmas cadastradas
    return render_template('cadastrar_aluno.html', turmas=turmas)

@app.route('/listar_alunos')
def listar_alunos():
    alunos = Aluno.query.all()  # Obtem todos os alunos do banco de dados
    return render_template('listar_alunos.html', alunos=alunos)

@app.route('/delete_aluno/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno excluído com sucesso!'}), 200
    return jsonify({'message': 'Aluno não encontrado.'}), 404

# Rota para criar uma nova turma
@app.route('/api/turmas', methods=['POST'])
def api_criar_turma():
    data = request.get_json()
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'message': 'O nome da turma é obrigatório.'}), 400
    
    nova_turma = Turma(nome=nome)
    db.session.add(nova_turma)
    db.session.commit()
    
    return jsonify({'message': 'Turma criada com sucesso!', 'id': nova_turma.id, 'nome': nova_turma.nome}), 201

# Rota para criar um novo aluno
@app.route('/api/alunos', methods=['POST'])
def api_criar_aluno():
    data = request.get_json()
    nome = data.get('nome')
    turma_id = data.get('turma_id')
    
    if not nome or not turma_id:
        return jsonify({'message': 'Nome do aluno e turma_id são obrigatórios.'}), 400
    
    nova_aluno = Aluno(nome=nome, turma_id=turma_id)
    db.session.add(nova_aluno)
    db.session.commit()
    
    return jsonify({'message': 'Aluno criado com sucesso!', 'id': nova_aluno.id, 'nome': nova_aluno.nome, 'turma_id': turma_id}), 201
