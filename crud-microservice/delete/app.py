from flask import Flask,render_template,request,jsonify
import os,redis
app = Flask("crud_delete_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")

home_con_name = os.environ.get("home_con_name")
custom_network_name = os.environ.get("custom_network_name")
home_port = os.environ.get("home_port")
read_con_name = os.environ.get("read_con_name")
read_port = os.environ.get("read_port")
delete_con_name = os.environ.get("delete_con_name")
delete_port = os.environ.get("delete_port")
create_port = os.environ.get("create_port")
create_con_name = os.environ.get("create_con_name")

@app.route("/form",methods=['POST','GET'])
def form():
    return render_template("form.html",port=port,delete_con_name=delete_con_name,home_con_name=home_con_name,home_port=home_port,custom_network=custom_network_name,delete_port=delete_port)

@app.route('/delete', methods=['POST'])
def delete():

    name =  request.form.get("delete_employee_name")
    print(name)
    delete_key= request.form.get("delete_key")
    print(delete_key)
    check_name=redis.hget(f"user:{name}","name")
    print(check_name)
    print(name)
    if check_name!=None:
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
      return render_template("delete.html",delete_key=delete_key,employee_name=name,read_port=read_port,home_con_name=home_con_name,custom_network_name=custom_network_name,home_port=home_port,read_con_name=read_con_name)
    else:
      return render_template("error.html",name=name,read_con_name=read_con_name,read_port=read_port,custom_network_name=custom_network_name,create_con_name=create_con_name,create_port=create_port,home_port=home_port,home_con_name=home_con_name)
    

if __name__ == "__main__":
    port=os.environ.get("delete_port")
    app.run(debug=True, host="0.0.0.0", port=port)

