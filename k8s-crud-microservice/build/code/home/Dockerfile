from alpine:latest
run apk add --no-cache python3 py3-pip
run pip3 install flask loguru pytz jsonify --break-system-packages
workdir /root/flask
copy . ./
cmd python3 app.py
