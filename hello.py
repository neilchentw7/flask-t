from flask import Flask, request
app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {name}!'
app.run(host='0.0.0.0', port=8080)



