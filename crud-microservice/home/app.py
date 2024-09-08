from flask import Flask,render_template,request
import os

app = Flask("crud_home_app")

port=os.environ.get("home_port")
create_con_name=os.environ.get("create_con_name")
create_port=os.environ.get("create_port")
custom_network=os.environ.get("custom_network_name")
read_con_name=os.environ.get("read_con_name")
read_port=os.environ.get("read_port")
update_con_name=os.environ.get("update_con_name")
update_port=os.environ.get("update_port")
delete_con_name=os.environ.get("delete_con_name") 
delete_port=os.environ.get("delete_port")
@app.route("/")
def root():
    print("hi")
    return render_template("index.html",delete_con_name=delete_con_name,delete_port=delete_port,update_con_name=update_con_name,update_port=update_port,create_con_name=create_con_name,read_con_name=read_con_name,read_port=read_port,custom_network=custom_network,create_port=create_port)

port=os.environ.get("home_port")
app.run(debug=True,host="0.0.0.0",port=port)

