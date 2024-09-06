from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
app = Flask("db_app")
CORS(app, resources={r"/*": {"origins": "*"}})


#os.makedirs(os.path.join(basedir, 'sqlite'), exist_ok=True)
basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'sqlite'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'sqlite/mydata.sqlite')}"

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite/mydata.sqlite'

db = SQLAlchemy(app)

class sappad(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    employee_id = db.Column(db.Integer)
    def __init__(self,name,employee_id):
        self.name=name
        self.employee_id=employee_id

def create_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")




@app.route('/db', methods=['POST'])
def db_storage():
    #if request.method == 'OPTIONS':
        # Handle CORS preflight
     #   response = jsonify({'message': 'CORS preflight successful'})
     #   response.headers.add("Access-Control-Allow-Origin", "*")
     #   response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
      #  response.headers.add("Access-Control-Allow-Headers", "Content-Type")
     #   return response
    #data = request.get_json()  # Make sure to use request.get_json() for POST JSON data
    name =  request.form.get("employee_name")
    employee_id= request.form.get("employee_id")
    #name = request.args.get("name")
    #employee_id = request.args.get("employee_id")
    instance = sappad(f"{name}",f"{employee_id}")
    db.session.add(instance)
    db.session.commit()
    output = f"The user {name} with employee ID {employee_id} was successfully updated to DB"
    return output

if __name__ == "__main__":
    create_db()  # Call this function before running the app
    app.run(debug=True, host="0.0.0.0", port=5556)
