from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_update_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

home_con_name = os.environ.get("home_con_name")
custom_network_name = os.environ.get("custom_network_name")
home_port = os.environ.get("home_port")
read_con_name = os.environ.get("read_con_name")
read_port = os.environ.get("read_port")
home_con_name = os.environ.get("home_con_name")
home_port = os.environ.get("home_port")
update_con_name = os.environ.get("update_con_name")
update_port = os.environ.get("update_port")

@app.route("/form",methods=['POST','GET'])
def form():
    return render_template("form.html",port=port,update_con_name=update_con_name,home_con_name=home_con_name,home_port=home_port,custom_network=custom_network_name,update_port=update_port)

@app.route('/update', methods=['POST'])
def update():
    name =  request.form.get("update_employee_name")
    print(name)
    update_key= request.form.get("update_key")
    print(update_key)
    update_value = request.form.get("update_value")
    print(update_value)

    if update_key=="employee_id":
      update_key="Employee ID"
      redis.hset(f"user:{name}",mapping={"id":f"{update_value}"})
    elif update_key=="employee_mail":
      update_key="Employee Mail"
      redis.hset(f"user:{name}",mapping={"email":f"{update_value}"})
    else:
      return "No Key is submitted to update"
    return render_template("update.html",update_value=update_value,update_key=update_key,employee_name=name,read_port=read_port,home_con_name=home_con_name,custom_network_name=custom_network_name,home_port=home_port,read_con_name=read_con_name)


if __name__ == "__main__":
    port=os.environ.get("update_port")
    app.run(debug=True, host="0.0.0.0", port=port)

