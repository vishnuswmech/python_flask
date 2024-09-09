from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_create_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")
custom_network_name = os.environ.get("custom_network_name")
read_con_name = os.environ.get("read_con_name")
read_port = os.environ.get("read_port")
create_con_name=os.environ.get("create_con_name")
create_port=os.environ.get("create_port")
home_con_name=os.environ.get("home_con_name")
home_port=os.environ.get("home_port")
update_con_name=os.environ.get("update_con_name")
update_port=os.environ.get("update_port")


@app.route("/form",methods=["POST","GET"])
def form():
    return render_template("form.html",port=port,create_con_name=create_con_name,custom_network=custom_network_name,create_port=create_port,home_port=home_port,home_con_name=home_con_name)

@app.route('/create', methods=['POST'])
def create():
    name =  request.form.get("employee_name")
    employee_id= request.form.get("employee_id")
    employee_mail = request.form.get("employee_mail")
    check_name=redis.hget(f"user:{name}","name")
    print(check_name)
    print(name)
    if check_name==None:
      redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
      output = f"The User <b>{name}</b> with Employee ID <b>{employee_id}</b> and Employee mail <b>{employee_mail}</b> was successfully updated to Redis host"
      return render_template("create.html",employee_id=employee_id,employee_mail=employee_mail,employee_name=name,read_port=read_port,home_con_name=home_con_name,custom_network_name=custom_network_name,home_port=home_port,read_con_name=read_con_name)
    else:
      return render_template("error.html",employee_id=employee_id,employee_mail=employee_mail,employee_name=name,update_con_name=update_con_name,update_port=update_port,custom_network_name=custom_network_name,create_con_name=create_con_name,create_port=create_port)


      

if __name__ == "__main__":
    port=os.environ.get("create_port")
    app.run(debug=True, host="0.0.0.0", port=port)
