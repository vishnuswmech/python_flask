from flask import Flask, render_template, request
import subprocess

app = Flask("cmd_app")


@app.route("/")
def form():
    data = render_template("cmd.html")
    return data


@app.route("/cmd",methods=["GET"])
def cmd():
    cmd = request.args.get("command")
    #output = render_template("cmd.html",command=cmd)
    return "<pre>" + subprocess.getoutput(cmd) + "</pre>"
