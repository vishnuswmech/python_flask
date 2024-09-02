from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy


app = Flask("db_app")

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite/mydata.sqlite'

db = SQLAlchemy(app)

class sappad(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    employee_id = db.Column(db.Integer)
    def __init__(self,name,employee_id):
        self.name=name
        self.employee_id=employee_id
db.create_all()

vishnu = sappad("srivishnu",13861)
db.session.add(vishnu)
db.session.commit()
