from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Cadastro(db.Model):

    __tablename__= 'agendamentos'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(86), nullable=False)
    contato = db.Column(db.String(14), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario= db.Column(db.String(6), nullable=False)
    tipo= db.Column(db.String(20), nullable=False)
    servico = db.Column(db.String(20), nullable=False)
    datahora= db.Column(db.String(16), unique=True)

    def __init__(self, cliente, email, contato, data, horario, tipo, servico, datahora):
        self.cliente = cliente
        self.email = email
        self.contato = contato
        self.data = data
        self.horario = horario
        self.tipo = tipo
        self.servico = servico 
        self.datahora = datahora 

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

db.create_all()
