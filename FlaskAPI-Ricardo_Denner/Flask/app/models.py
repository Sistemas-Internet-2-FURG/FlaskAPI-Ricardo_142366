from app import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

    def __repr__(self):
        return f"Turma('{self.nome}')"


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)

    def __repr__(self):
        return f"Aluno('{self.nome}', Turma: '{self.turma.nome}')"
