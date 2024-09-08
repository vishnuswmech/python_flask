from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_update_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

@app.route('/update', methods=['POST'])
def db_storage():

    name =  request.form.get("update_employee_name")
    print(name)
    update_key= request.form.get("update_key")
    print(update_key)
    update_value = request.form.get("update_value")
    print(update_value)
    frontend_con_name = os.environ.get("frontend_con_name")
    custom_network_name = os.environ.get("custom_network_name")
    frontend_port = os.environ.get("frontend_port")
    read_con_name = os.environ.get("read_con_name")
    read_port = os.environ.get("read_port")

    if update_key=="employee_id":
      redis.hset(f"user:{name}",mapping={"id":f"{update_value}"})
    elif update_key=="employee_mail":
      redis.hset(f"user:{name}",mapping={"email":f"{update_value}"})
    else:
      return "No Key is submitted to update"
    #redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
    #output = redis.hgetall(f"{name}")
    output = f"The User <b>{name}</b> with Update Key <b>{update_key}</b> is updated with <b>{update_value}</b> successfully to Redis host"
    #return render_template("create.html",name=name,employee_id=employee_id,employee_mail=employee_mail)

    return render_template("db.html",update_value=update_value,update_key=update_key,employee_name=name,read_port=read_port,frontend_con_name=frontend_con_name,custom_network_name=custom_network_name,frontend_port=frontend_port,read_con_name=read_con_name)
if __name__ == "__main__":
    port=os.environ.get("update_port")
    app.run(debug=True, host="0.0.0.0", port=port)

