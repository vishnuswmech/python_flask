from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("db_app")

redis=redis.Redis(host='redis-service.vishnu-net', port=6379)

@app.route('/create', methods=['POST'])
def db_storage():

    name =  request.form.get("employee_name")
    employee_id= request.form.get("employee_id")
    employee_mail = request.form.get("employee_mail")
    redis.hset(f"user:{name}", mapping={"name": f"{name}", "id": f"{employee_id}", "email": f"{employee_mail}"})
    #output = redis.hgetall(f"{name}")
    output = f"The user {name} with employee ID {employee_id} was successfully updated to DB"
    #return render_template("create.html",name=name,employee_id=employee_id,employee_mail=employee_mail)
    return render_template("db.html",output=output,employee_name=name)
if __name__ == "__main__":
    port=os.environ.get("backend_port")
    app.run(debug=True, host="0.0.0.0", port=port)

