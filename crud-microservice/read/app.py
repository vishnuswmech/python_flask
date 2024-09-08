from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_read_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")
frontend_con_name = os.environ.get("frontend_con_name")
custom_network_name = os.environ.get("custom_network_name")
frontend_port = os.environ.get("frontend_port")
@app.route('/list', methods=['POST'])
def db_storage():

    name =  request.form.get("employee_name")
    print(f"the name is {name}")
    #employee_id= request.form.get("employee_id")
    #employee_mail = request.form.get("employee_mail")
    #redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
    output = redis.hgetall(f"user:{name}")
    print(output)
    decoded_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in output.items()}
    print(decoded_data)
    #output = f"The user {name} with employee ID {employee_id} was successfully updated to DB"
    print(decoded_data)
    #return render_template("create.html",name=name,employee_id=employee_id,employee_mail=employee_mail)
    return render_template("list.html",output=decoded_data,frontend_con_name=frontend_con_name,custom_network_name=custom_network_name,frontend_port=frontend_port)
if __name__ == "__main__":
    port=os.environ.get("read_port")
    app.run(debug=True, host="0.0.0.0", port=port)

