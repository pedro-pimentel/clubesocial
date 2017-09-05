#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################

from subprocess import Popen, PIPE
from classes.Home import Device
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

###################################################################     
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ihome.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
####################################################################
####################################################################
##############################Classes importantes##########################


class Rooms(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Devices', backref='rooms', lazy='dynamic')

class Devices(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer)
    name = db.Column(db.Integer)
    status = db.Column(db.Integer)
    id_room = db.Column(db.Integer, db.ForeignKey('rooms.id_'))

####################################################################
####################################################################
#########Funcao de render do template index###################################
@app.route('/')
def main():

	return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')

##################################################################
#########Funcao para mandar o json para o aplicativo com os dispositivos###############

@app.route('/devices',  methods=['POST', 'GET'])
def devices():
	if request.method == 'POST':
		dispositivos = []
		disp = Devices.query.filter_by(id_room= request.form['id']).all()
		comodo = Rooms.query.filter_by(id_= request.form['id']).all()
		for i in disp:
			dispositivos.append(dict(id=i.id_, name='{0} - [{1}]'.format(i.name, i.pin), status=i.status))
		return jsonify([{'comodo':c.__dict__.get('name') for c in comodo},{"aparelhos": dispositivos }])

##################################################################
###################Funcao para listar os comodos#############################

@app.route('/room')
def room():
    c = Rooms.query.all()
    comodos = []
    if c:
        for i in c:
            comodos.append(dict(id=i.id_,nome=i.name))
    return jsonify(comodos)

#######################################)#########################
##################Funcao para trocar o status do dispositivo#####################

@app.route('/swap',  methods=['POST', 'GET'])
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

if __name__ == '__main__':
    #app.run(debug = True)
    #Comando para buscar informações e filtrar o ip
    db.create_all()
    db.session.commit()
    setPins()
    cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #Recebendo o IP que está na placa no eth0
    AdressIP, err = p.communicate()
    app.run(host=AdressIP, port=5000, debug=True, threaded=True)