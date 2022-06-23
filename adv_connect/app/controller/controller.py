#Bibliotecas
import smtplib

#Modulos init e model
from app import app, db
from app.models.models import Cadastro, User

#Modulos do Flask
from flask_login import login_user, logout_user
from flask import render_template, url_for, request, redirect
from datetime import datetime

#Email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Função para enviar e-mail: conexão com API do Google
def enviar_email():
     #Formata a data
     data_str = '%Y-%m-%d'
     datetime_obj = datetime.strptime(data, data_str)
     data_fmt = datetime_obj.strftime("%d/%m/%Y")
     #Composição do e-mail
     msg = MIMEMultipart()
     msg['Subject'] = servico
     msg['From'] = "ADV-Connect <adv.connect.contato@gmail.com>"
     msg['To'] = email
     texto = "Agendamento " + tipo.lower() + " confirmado para o dia: " +  data_fmt + ", às " + horario + " h."
     msg.attach(MIMEText(texto, 'plain'))
     #Login e envio
     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
     server.login("adv.connect.contato@gmail.com", "tdtclvbosqlzkxmn")
     server.sendmail(msg['From'], msg['To'], msg.as_string())
     server.quit()

#Rota página index
@app.route('/')
def index():
    return render_template('index.html')

#Rota página Política de privacidade
@app.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')

#Rota página conectar: escolha do serviço conforme área de atuação
@app.route('/conectar')
def conectar():
    return render_template('conectar.html')

#Rota para pagina agendar
@app.route('/agendar', methods=['GET','POST'])
def agendar():
        # Entrada do formulário área de atuação
        global servico
        if request.method == 'POST':
           servico = request.form['servico']
        return render_template('agendar.html')

#Rota para inserção no banco de dados, envio de e-mail e tela final
@app.route('/final', methods=['GET','POST'])
def final():
    if request.method == 'POST':
       global email, data, horario, tipo
       #Entrada do formulário agenda
       cliente = request.form['cliente']
       email = request.form['email']
       contato = request.form['contato']
       data = request.form['data']
       horario = request.form['horario']
       tipo = request.form['tipo']
       datahora = data + " " + horario
       
       #Adiciona ao banco de dados e envia e-mail
       if cliente and email and contato and data and horario and tipo and servico:
            temp = Cadastro(cliente, email, contato, data, horario, tipo, servico, datahora)
            try:
               db.session.add(temp)
               db.session.commit()
               enviar_email()
               return render_template('final.html')
            except:
               db.session.rollback()                     
               return render_template('aviso.html', cadastrado = temp)

#Rota para imprimir o cadastro
@app.route('/cadastro')
def cadastro():
    cadastrados = Cadastro.query.all()
    return render_template('cadastro.html', cadastrados=cadastrados)

#Rota para excluir informação o cadastro voltar para o cadastro
@app.route('/excluir_cadastro/<int:id>')
def excluir_cadastro(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()
    db.session.delete(cadastrado)
    db.session.commit()
    cadastrados = Cadastro.query.all()
    return render_template('cadastro.html', cadastrados=cadastrados)

#Rota para editar informação do cadastro, eviar e-mail e voltar para o cadastro
@app.route('/editar_cadastro/<int:id>', methods=['GET','POST'])
def editar_cadastro(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()
    #Entrada do formulário
    if request.method == 'POST':
        global servico, email, data, horario, tipo
        cliente = request.form['cliente']
        email = request.form['email']
        contato = request.form['contato']
        data = request.form['data']
        horario = request.form['horario']
        tipo= request.form['tipo']
        servico = request.form['servico']
        datahora = data + " " + horario
            
        # Adiciona ao banco de dados e envia e-mail
        if cliente and email and contato and data and data and horario and tipo and servico and datahora:
            cadastrado.cliente = cliente
            cadastrado.email = email
            cadastrado.contato = contato
            cadastrado.data = data
            cadastrado.horario = horario
            cadastrado.tipo = tipo
            cadastrado.servico = servico
            cadastrado.datahora = datahora
            try:
                db.session.commit()
                enviar_email()
                return redirect(url_for('cadastro'))
            except:
                db.session.rollback()
                temp_cd = Cadastro(cliente, email, contato, data, horario, tipo, servico, datahora)
                return render_template ('alerta.html', cadastrado = temp_cd)
    return render_template('editar.html', cadastrado=cadastrado)

# Consulta, retorna todos os agendamentos na data escolhida
@app.route('/consulta')
def consulta():
     try:
       date = data
       resultados = Cadastro.query.filter(Cadastro.data == date).order_by(Cadastro.data.asc(), Cadastro.horario.asc()).all()
       horas = db.session.query(Cadastro.horario).filter(Cadastro.data == date).order_by(Cadastro.horario.asc()).all()       
       return render_template('consulta.html', date = date, horas = horas, resultados = resultados)
     except:
       return redirect(url_for('index'))

#Agenda, retorna todos os agendamentos com data maior ou igual a data atual
@app.route('/agenda')
def agenda():
    hoje = (datetime.now()).strftime('%Y-%m-%d')
    resultados = Cadastro.query.filter(Cadastro.data >= hoje).order_by(Cadastro.data.asc(), Cadastro.horario.asc()).all()
    return render_template('agenda.html', resultados=resultados)

#Rota para excluir informação da agenda e voltar para agenda
@app.route('/excluir_agenda/<int:id>')
def excluir_agenda(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()
    db.session.delete(cadastrado)
    db.session.commit()
    hoje = datetime.now().strftime('%Y-%m-%d')
    resultados = Cadastro.query.filter(Cadastro.data >= hoje).order_by(Cadastro.data.asc(), Cadastro.horario.asc()).all()  
    return render_template('agenda.html', resultados=resultados)

#Rota para editar informação da agenda, eviar e-mail e voltar para agenda
@app.route('/editar_agenda/<int:id>', methods=['GET','POST'])
def editar_agenda(id):
    cadastrado = Cadastro.query.filter_by(_id=id).first()
    #Entrada do formulário agenda
    if request.method == 'POST':
        global servico, email, data, horario, tipo
        cliente = request.form['cliente']
        email = request.form['email']
        contato = request.form['contato']
        data = request.form['data']
        horario = request.form['horario']
        tipo = request.form['tipo']
        servico = request.form['servico']
        datahora = data + " " + horario
            
        #Adiciona ao banco de dados
        if cliente and email and contato and data and horario and tipo and servico and datahora:
           cadastrado.cliente = cliente
           cadastrado.email = email
           cadastrado.contato = contato
           cadastrado.data = data
           cadastrado.horario = horario
           cadastrado.tipo = tipo
           cadastrado.servico = servico
           cadastrado.datahora = datahora
           try:
                db.session.commit()
                enviar_email()
                return redirect(url_for('agenda'))
           except:
                db.session.rollback()
                temp_ag = Cadastro(cliente, email, contato, data, horario, tipo, servico, datahora)
                return render_template ('alerta.html', cadastrado = temp_ag)
    return render_template('editar.html', cadastrado=cadastrado)

#Rota para a tela gerenciar
@app.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        user = User(name, email, pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('gerenciar.html')

#Rota para a página login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(pwd):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

#Rota para página painel
@app.route('/painel')
def painel():
    return render_template('painel.html')

#Rota logout redireciona para a página de login
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
  
