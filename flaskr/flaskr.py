#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################

#from subprocess import Popen, PIPE
#from classes.Home import Device
from flask import Flask, request, session, g, Markup, redirect, url_for, abort, \
	 render_template, flash, jsonify, escape
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
	hierarquia = db.Column(db.Integer)
	tipo = db.Column(db.String(50))
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
	status = db.Column(db.String(50)) #Status = aprovado, pendente, recusado
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
		'''email_data
		senha_data
		nome_data
		tipo_data'''
		#user = Pessoa.select().where(Pessoa.email == email).first()
		pessoa = Pessoa.query.filter_by(email=email).all()
		for i in pessoa:
			email_data 	= i.email
			senha_data 	= i.senha
			nome_data 	= i.nome
			tipo_data  = i.tipo

		if email_data and senha_data and nome_data and tipo_data and email_data == email and senha_data == senha:
			session['username'] = nome_data
			session['h'] = tipo_data
			#return nome_data
			return redirect(url_for('adm'))
		else:
			message = Markup("<h1>Login invalido</h1>")
			flash(message)
			return render_template('index.html')
	else:
		return render_template('index.html')

##################################################################
###################Funcao de teste#############################

@app.route('/logged')
def logged():
	if 'username' in session:
		return 'Logado como: %s' % escape(session['username'] + "\n Tipo: " + session['h'])
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

		pessoa = Pessoa(nome=nome,email=email,endereco=endereco, contato=contato, rg = rg, cpf = cpf, renda = renda, profissao = profissao, trabalho = trabalho, tipo = "associado")
		db.session.add(pessoa)
		db.session.commit()
		id_last = pessoa.id_
		solicitacao = Solicitacao(mensagem=mensagem, id_pessoa = id_last, status = "pendente")
		db.session.add(solicitacao)
		db.session.commit()
		message = Markup("<div class='col alert alert-success alert-dismissible fade show' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><h4 class='alert-heading'>Cadastrado com sucesso!</h4><p>Iremos avaliar sua socilicitacao e enviaremos o resultado para seu e-mail.</p></div>")
		flash(message)
		return render_template('index.html')
	else:
		return render_template('index.html')

#######################################)#########################
##################Funcao de aprovacao#####################

@app.route('/adm')
def adm():
	# remove the username from the session if it's there
	if 'username' in session and session['username'] != None and session['h'] == "adm":
		pessoa = Pessoa.query.filter_by(status="pendente").all()
		
		username = Markup(session['username'])
		flash(username)
		return render_template('lista.html', pessoa = pessoa)
	else:
		message = Markup("<h1>Voce precisa logar para acessar</h1>")
		flash(message)
		return render_template('index.html')

@app.route('/abrir/<idpessoa>', methods=['POST', 'GET'])
def abrir(idpessoa):
	# 
	if 'username' in session and session['username'] != None and session['h'] == "adm":
		if request.method == 'GET':
			id_pessoa = idpessoa

			pessoa = Pessoa.query.filter_by(id_ = id_pessoa).all()
			for i in pessoa:
				email_data 	= i.email
				senha_data 	= i.senha
				nome_data 	= i.nome
				tipo_data  = i.tipo

			socilicitacao = Solicitacao.query.filter_by(id_pessoa = id_pessoa).all()
			for j in pessoa:
				mensagem_data 	= j.email
				data_data 	= j.senha

			return render_template('abrir.html', pessoa = pessoa, solicitacao = solicitacao)
	else:
		message = Markup("<h1>Voce precisa logar para acessar</h1>")
		flash(message)
		return render_template('index.html')

@app.route('/analise', methods=['POST', 'GET'])
def analise():
	if 'username' in session and session['username'] != None and session['h'] == "adm":
		if request.method == 'GET':
			condicao = request.form['condicao']
			id_pessoa = request.form['id_pessoa']

			if condicao == 1:
				pessoa = Pessoa.query.filter_by(id_ = id_pessoa).all()
				pessoa.status = "aprovado"
				db.session.commit()

				solicitacao = Solicitacao.query.filter_by(id_pessoa = id_pessoa).all()
				solicitacao.status = "aprovado"
				db.session.commit()
			elif condicao == 0:
				pessoa = Pessoa.query.filter_by(id_ = id_pessoa).all()
				pessoa.status = "recusado"
				db.session.commit()

				solicitacao = Solicitacao.query.filter_by(id_pessoa = id_pessoa).all()
				solicitacao.status = "recusado"
				db.session.commit()

@app.route('/boleto')
def boleto():
	return render_template('acesso_boleto.html')


@app.route('/boleto/abrir', methods=['POST', 'GET'])
def abrirboleto():
	if request.method == 'POST':
		cpf = request.form['cpf']
		pessoa = Pessoa.query.filter_by(cpf=cpf).all()
		return render_template('boleto.html', pessoa = pessoa)

	else:
		message = Markup("<h1>Voce precisa logar para acessar</h1>")
		flash(message)
		return render_template('acesso_boleto.html')

'''
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
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
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
