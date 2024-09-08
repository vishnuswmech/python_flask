from flask import Flask,render_template,request
import os

app = Flask("crud_form_app")
port=os.environ.get("frontend_port")




port=os.environ.get("frontend_port")
app.run(debug=True,host="0.0.0.0",port=port)

