#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################

#from subprocess import Popen, PIPE
#from classes.Home import Device
from flask import Flask, request, session, g, Markup, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import socket

###################################################################     
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clube.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
####################################################################
####################################################################
##############################Classes importantes##########################


class Pessoa(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    endereco = db.Column(db.String(50))
    contato = db.Column(db.String(50))
    data_nasc = db.Column(db.String(50))
    status = db.Column(db.String(50))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    rg = db.Column(db.String(50))
    profissao = db.Column(db.String(50))
    trabalho = db.Column(db.String(50))
    renda = db.Column(db.Integer)
    dependente = db.relationship('Dependente', backref='pessoa', lazy='dynamic')
    mensalidade = db.relationship('Mensalidade', backref='pessoa', lazy='dynamic')
    solicitacao = db.relationship('Solicitacao', backref='pessoa', lazy='dynamic')

class Dependente(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    name = db.Column(db.Integer)
    status = db.Column(db.Integer)
    id_room = db.Column(db.Integer, db.ForeignKey('pessoa.id_'))

class Mensalidade(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer)
    data_pagamento = db.Column(db.DateTime)
    valor_pago = db.Column(db.Integer)
    mensalidade = db.Column(db.String(50))
    id_room = db.Column(db.Integer, db.ForeignKey('pessoa.id_'))

class Solicitacao(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    mensagem = db.Column(db.String(50))
    status = db.Column(db.String(50)) #Status = aprovado, em andamento, recusado
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_'))

####################################################################
####################################################################
#########Funcao de render do template index###################################
'''@app.route('/')
def main():

	return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')'''

##################################################################
#########Funcao de Login###############


'''@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return 
		#<form method="post">
		#	<p><input type=text name=username>
		#	<p><input type=submit value=Login>
		#</form>
'''

@app.route('/login',  methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		senha = request.form['senha']
		email_data = None
		senha_data = None
		nome_data  = None
		#user = Pessoa.select().where(Pessoa.email == email).first()
		pessoa = Pessoa.query.filter_by(email=email).all()
		for i in pessoa:
			email_data = i.email
			senha_data = i.senha
			nome_data = i.nome

		if((email_data == email) and (senha_data == senha)):
			session['username'] = nome_data
			return render_template('teste.html', pessoa = pessoa)
		else:
			message = Markup("<h1>Login inválido</h1>")
			flash(message)
			return render_template('index.html')
		#login = Pessoa.query.filter_by(senha= senha)
		#if login.email == email and login.senha == senha:
		#	session['username'] = login.nome
		#return render_template('teste.html', pessoa = pessoa)
		return asd
	else:
		return render_template('index.html')

##################################################################
###################Funcao de teste#############################

@app.route('/logged')
def logged():
    if 'username' in session:
        return session['username']
    return 'You are not logged in'


##################################################################
##################Render Index########################################

@app.route('/')
def index():
	return render_template('index.html')


#################################################################################
#################################Logout##########################################

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('index.html')



#################################################################################
###############################Funcao solicitacao################################


@app.route('/solicitacao', methods=['POST', 'GET'])
def solicitacao():

	if request.method == 'POST':
		nome      = request.form['nome']
		email     = request.form['email']
		endereco  = request.form['endereco']
		contato   = request.form['contato']
		rg        = request.form['rg']
		cpf       = request.form['cpf']
		renda     = request.form['renda']
		profissao = request.form['profissao']
		trabalho  = request.form['trabalho']
		mensagem  = request.form['mensagem']

		pessoa = Pessoa(nome=nome,email=email,endereco=endereco, contato=contato, rg = rg, cpf = cpf, renda = renda, profissao = profissao, trabalho = trabalho)
		db.session.add(pessoa)
		db.session.commit()
		id_last = pessoa.id_
		solicitacao = Solicitacao(mensagem=mensagem, id_pessoa = id_last, status = "Pendente")
		db.session.add(solicitacao)
		db.session.commit()
		message = Markup("<div class='col alert alert-success alert-dismissible fade show' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><h4 class='alert-heading'>Cadastrado com sucesso!</h4><p>Iremos avaliar sua socilicitacao e enviaremos o resultado para seu e-mail.</p></div>")
		flash(message)
		return render_template('index.html')
	else:
		return render_template('index.html')

#######################################)#########################
##################Funcao para trocar o status do dispositivo#####################

'''@app.route('/swap',  methods=['POST', 'GET'])
def swap():
	if request.method == 'POST':
		id_device = request.form['id']
		device = Devices.query.filter_by(id_=id_device).all()
		status_device = request.form['estado']

		for i in device:
			pino = int(i.pin)
		home = Device(pino)

		if (status_device == '0'):
			home.offDevice(pino)
			for i in device:
				i.status = int(status_device)
				db.session.commit()
				status = i.status

		else:
			home.onDevice(pino)
			for i in device:
				i.status = int(status_device)
				db.session.commit()
				status = i.status



		# aqui entra a funcao para verificar o estado do pino na placa
		# return redirect(url_for('index'))
	return jsonify(status=status)


@app.route('/comodos')
def comdos():
	return render_template('comodos.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        dispositivos = Devices(name=request.form['dispositivo'],pin=request.form['pin'],status=0, id_room=request.form['cm'])
        db.session.add(dispositivos)
        db.session.commit() 
    return render_template('add_device.html', comodo = Rooms.query.all())

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
	if request.method == 'POST':
		comodos = Rooms(name=request.form['comodo'])
		db.session.add(comodos)
		db.session.commit()
	return render_template('add_room.html')		


#@app.cli.command('initpin')
def setPins():
	dispositivos = Devices.query.all()
	if dispositivos:
		for dispositivo in dispositivos:
			disp = Device(dispositivo.pin)
			if dispositivo.status == 0:
				disp.offDevice(dispositivo.pin)
			else:
				disp.onDevice(dispositivo.pin)
'''
if __name__ == '__main__':
    #app.run(debug = True)
    #Comando para buscar informações e filtrar o ip
    db.create_all()
    db.session.commit()
    #setPins()
    #cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
    #p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #Recebendo o IP que está na placa no eth0
    #AdressIP, err = p.communicate()
    AdressIP = socket.gethostbyname(socket.gethostname())
    app.run(host=AdressIP, port=5000, debug=True, threaded=True)