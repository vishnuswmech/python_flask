from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("db_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

@app.route('/create', methods=['POST'])
def db_storage():

    name =  request.form.get("employee_name")
    employee_id= request.form.get("employee_id")
    employee_mail = request.form.get("employee_mail")
    frontend_con_name = os.environ.get("frontend_con_name")
    custom_network_name = os.environ.get("custom_network_name")
    frontend_port = os.environ.get("frontend_port")
    read_con_name = os.environ.get("read_con_name")
    read_port = os.environ.get("read_port")
    redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
    #output = redis.hgetall(f"{name}")
    output = f"The User <b>{name}</b> with Employee ID <b>{employee_id}</b> and Employee mail <b>{employee_mail}</b> was successfully updated to Redis host"
    #return render_template("create.html",name=name,employee_id=employee_id,employee_mail=employee_mail)

    return render_template("db.html",employee_id=employee_id,employee_mail=employee_mail,employee_name=name,read_port=read_port,frontend_con_name=frontend_con_name,custom_network_name=custom_network_name,frontend_port=frontend_port,read_con_name=read_con_name)
if __name__ == "__main__":
    port=os.environ.get("backend_port")
    app.run(debug=True, host="0.0.0.0", port=port)
