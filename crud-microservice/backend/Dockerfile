from ubuntu:latest
run apt update && apt install net-tools vim python3 python3-pip curl -y
run pip3 install flask flask_sqlalchemy flask_cors --break-system-packages 
expose 5556
workdir /root/flask
copy . ./
cmd python3 app.py

