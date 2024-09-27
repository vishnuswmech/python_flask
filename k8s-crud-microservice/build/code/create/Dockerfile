from alpine
run apk add python3 py3-pip
run pip3 install flask redis loguru pytz jsonify --break-system-packages 
workdir /root/flask
copy . ./
cmd python3 app.py

