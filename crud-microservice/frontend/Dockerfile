from ubuntu:latest
run apt update -y && apt install python3 python3-pip vim curl net-tools iputils-ping -y
run pip3 install flask flask_sqlalchemy --break-system-packages
expose 5555
copy . /root/
cmd python3 /root/app.py
