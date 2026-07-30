from flask import Flask, request, jsonify
from calculator import add, subtract, multiply, divide

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"status": "Calculator API is running"})


@app.route('/add')
def route_add():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"result": add(a, b)})


@app.route('/subtract')
def route_subtract():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"result": subtract(a, b)})


@app.route('/multiply')
def route_multiply():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"result": multiply(a, b)})


@app.route('/divide')
def route_divide():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    try:
        return jsonify({"result": divide(a, b)})
    except ZeroDivisionError:
        return jsonify({"error": "Cannot divide by zero"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
