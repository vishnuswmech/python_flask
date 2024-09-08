from flask import Flask,render_template,request
import os

app = Flask("db_app")

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite/mydata.sqlite'

#db = SQLAlchemy(app)

#class sappad(db.Model):
#    id = db.Column(db.Integer,primary_key = True)
#    name = db.Column(db.Text)
#    employee_id = db.Column(db.Integer)
#    def __init__(self,name,employee_id):
#        self.name=name
#        self.employee_id=employee_id
#db.create_all()
port=os.environ.get("frontend_port")
backend_con_name=os.environ.get("backend_con_name")
create_port=os.environ.get("backend_port")
custom_network=os.environ.get("custom_network_name")
read_con_name=os.environ.get("read_con_name")
read_port=os.environ.get("read_port")
update_con_name=os.environ.get("update_con_name")
update_port=os.environ.get("update_port")

@app.route("/")
def root():
    print(f"http://{update_con_name}.{custom_network}:{update_port}/read")
    return render_template("root.html",update_con_name=update_con_name,update_port=update_port,backend_con_name=backend_con_name,read_con_name=read_con_name,read_port=read_port,custom_network=custom_network,create_port=create_port)
@app.route("/form",methods=["POST"])
def form():
    return render_template("db.html",port=port,backend_con_name=backend_con_name,custom_network=custom_network,create_port=create_port )

port=os.environ.get("frontend_port")
app.run(debug=True,host="0.0.0.0",port=port)

