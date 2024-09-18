from alpine
run apk add python3 py3-pip curl
run pip3 install flask redis loguru pytz --break-system-packages 
workdir /root/flask
copy . ./
cmd python3 app.py