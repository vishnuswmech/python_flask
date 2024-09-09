from flask import Flask,render_template,request,jsonify
import os,redis

app = Flask("crud_read_app")

redis_host=os.environ.get("redis_host")
redis=redis.Redis(host=redis_host, port="6379")
home_con_name = os.environ.get("home_con_name")
custom_network_name = os.environ.get("custom_network_name")
home_port = os.environ.get("home_port")
read_port = os.environ.get("read_port")
read_con_name = os.environ.get("read_con_name")


@app.route("/form",methods=["POST"])
def form():
    return render_template("form.html",port=port,read_con_name=read_con_name,home_con_name=home_con_name,home_port=home_port,custom_network=custom_network_name,read_port=read_port)


@app.route('/list', methods=['POST'])
def list():
    name =  request.form.get("employee_name")
    print(f"the name is {name}")
    output = redis.hgetall(f"user:{name}")
    print(output)
    decoded_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in output.items()}
    print(decoded_data)
    print(decoded_data)
    return render_template("list.html",output=decoded_data,home_con_name=home_con_name,custom_network_name=custom_network_name,home_port=home_port)


if __name__ == "__main__":
    port=os.environ.get("read_port")
    app.run(debug=True, host="0.0.0.0", port=port)

