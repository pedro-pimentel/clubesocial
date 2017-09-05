#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################
import os, sqlite3, socket
from subprocess import Popen, PIPE
from classes import Home
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ihome.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
####################################################################
####################################################################
####################################################################
home = Home.Device(13)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
##################################################################
#########Funcao de render do template index###################################
@app.route('/index')
def index():
    return render_template('index.html')
##################################################################
#########Funcao para inserir dados no banco####################################
@app.route('/add_room', methods=['POST'])
def add_rooms():
    #if not session.get('logged_in'):
       # abort(401)
    db = get_db()
    db.execute('insert into rooms (name, descricao) values (?, ?)',
                 [request.form['room'], request.form['description']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

##################################################################
#########Funcao de teste para retornar os dados do banco############################
@app.route('/show_room')
def show_rooms():
    db = get_db()
    cur = db.execute('select name, descricao from room order by id desc')
    room = cur.fetchall()
    return render_template('show_rooms.html', room=room)
##################################################################
#########Funcao para mandar o json para o aplicativo com os dispositivos###############

@app.route('/devices',  methods=['POST', 'GET'])
def devices():

	if request.method == 'POST':
      #aparelho = request.form['id_ap']
		id_ = int(request.form['id'])

      #estado = request.form['estado']

	if id_ == 1:
		dicionario = {"aparelhos": [{"pin": 13,"id":1, "nome": "Lampada 1", "status":0}, {"pin": 7,"id":2, "nome": "Lampada 2", "status":0}]}
	if id_ == 2:
		dicionario = {"aparelhos": [{"pin":7,"id": 3, "nome": "Lampada 3", "status":0}]}
	return jsonify(dicionario)	
        #return redirect(url_for('index'))
    #return jsonify(aparelhos=[dict(nome='teste',status=1,id=1),  dict(nome='teste2',status=0,id=2)])

##################################################################
###################Funcao para listar os comodos#############################

@app.route('/room')
def room():
	return jsonify(room=[dict(id=1,nome='sala'),  dict(id=2,nome='quarto')])

################################################################
##################Funcao para trocar o status do dispositivo#####################

@app.route('/swap',  methods=['POST', 'GET'])
def swap():

    if request.method == 'POST':
        #aparelho = request.form['id_ap']
        id_device = request.form['id']
        status_device = int(request.form['estado'])
        if (status_device):
            pino = 13
            home.onDevice(pino)


        if (status_device == 0):
            pino = 13
            home.offDevice(pino)


        #aqui entra a funcao para verificar o estado do pino na placa
        #return redirect(url_for('index'))
        return jsonify(status=status_device)

@app.route('/comodos')
def comdos():
	return render_template('comodos.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    #app.run(debug = True)
    #Comando para buscar informações e filtrar o ip
    cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #Recebendo o IP que está na placa no eth0
    AdressIP, err = p.communicate()
    app.run(host=AdressIP, port=5000, debug=True,threaded=True)

