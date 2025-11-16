from flask import request
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'Hello, World! This is my first web-application! GET-запрос!'
    elif request.method == 'POST':
        return 'Hello, World! This is my first web-application! (POST-запрос)'
    else:
        return 'Неизвестный метод запроса'