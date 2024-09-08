from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_delete_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

@app.route('/delete', methods=['POST'])
def db_storage():

    name =  request.form.get("delete_employee_name")
    print(name)
    delete_key= request.form.get("delete_key")
    print(delete_key)
    #update_value = request.form.get("update_value")
    #print(update_value)
    frontend_con_name = os.environ.get("frontend_con_name")
    custom_network_name = os.environ.get("custom_network_name")
    frontend_port = os.environ.get("frontend_port")
    read_con_name = os.environ.get("read_con_name")
    read_port = os.environ.get("read_port")
    if delete_key=="delete_employee_id":
        delete_key="Employee ID"
        redis.hdel(f"user:{name}","id")
    elif delete_key=="delete_employee_mail":
        delete_key="Employee Mail"
        redis.hdel(f"user:{name}","email")
    elif delete_key=="delete_user":
        delete_key="User"
        redis.delete(f"user:{name}")
    else:
      return "No Key is submitted to delete"
    
    #redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
    #output = redis.hgetall(f"{name}")
    output = f"The User <b>{name}</b> with delete Key <b>{delete_key}</b> is deleted successfully to Redis host"
    #return render_template("create.html",name=name,employee_id=employee_id,employee_mail=employee_mail)

    return render_template("db.html",delete_key=delete_key,employee_name=name,read_port=read_port,frontend_con_name=frontend_con_name,custom_network_name=custom_network_name,frontend_port=frontend_port,read_con_name=read_con_name)
if __name__ == "__main__":
    port=os.environ.get("delete_port")
    app.run(debug=True, host="0.0.0.0", port=port)

