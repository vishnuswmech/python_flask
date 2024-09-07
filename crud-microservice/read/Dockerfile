from ubuntu:latest
run apt update && apt install net-tools vim python3 python3-pip curl -y
run pip3 install flask redis --break-system-packages 
workdir /root/flask
copy . ./
cmd python3 app.py

