#!/usr/bin/python
# -*- coding: utf-8 -*-

#from ..flaskr import flaskr
'''app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class Request():
	def adicionar(self,comodo):
		db.session.add(comodo)
		db.session.commit()
'''
class Rooms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	addresses = db.relationship('Devices', backref='device', lazy='dynamic')

class Devices(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pin = db.Column(db.String(50))
	name = db.Column(db.Integer)
	status = db.Column(db.String(30))
	id_room = db.Column(db.Integer, db.ForeignKey('device.id'))