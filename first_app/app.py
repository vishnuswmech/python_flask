from flask import Flask,render_template
import subprocess


app=Flask("my_app")

@app.route("/search")
def search():
    return("Hi search")

@app.route("/vishnu")
def vishnu():
    return render_template("vishnu.html")
