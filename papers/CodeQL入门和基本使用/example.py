from flask import Flask
from flask import request

app = Flask(__name__)

def exec_system(cmd):
    import os
    result = os.popen(cmd).read()
    return result

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/command_execution")
def command_execution():
    param = request.values.get("param")
    cmd = "echo %s | base64" %  param
    result = exec_system(cmd)
    return result

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True)

# curl "http://127.0.0.1:5000/command_execution?param=123;whoami"
# 123
# dWJ1bnR1Cg==
