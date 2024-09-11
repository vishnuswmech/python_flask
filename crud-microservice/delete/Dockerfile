from ubuntu:latest
run apt update -y && apt install python3 python3-pip vim curl net-tools iputils-ping -y
run pip3 install flask redis loguru pytz --break-system-packages
workdir /root/flask
copy . ./
cmd python3 app.py
