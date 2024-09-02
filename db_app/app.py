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

@app.route("/form")
def form():
    return render_template("db.html")

@app.route("/db",methods=["GET"])
def db_storage():
    name = request.args.get("name")
    employee_id = request.args.get("employee_id")
    instance = sappad(f"{name}",f"{employee_id}")
    db.session.add(instance)
    db.session.commit()
    output = f"The user {name} with employee ID {employee_id} was successfully updated to DB"
    return output

app.run(debug=True,host="0.0.0.0",port=5555)
