from app import app
from flask import render_template
from flask import request
import psycopg

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'Hello, World! This is my first web-application! GET-запрос! Вторая проверка '
    elif request.method == 'POST':
        return 'Hello, World! This is my first web-application! (POST-запрос)'
    else:
        return 'Неизвестный метод запроса'

def get_db_connection(): # вынесем подключение к бд в отдельную функцию
    return psycopg.connect(
        host=app.config['DB_SERVER'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        dbname=app.config['DB_NAME']
    )

@app.route('/projects', methods=['GET'])
def projects_list(): # просмотреть список проектов (список названий с кнопкой посмотреть или прям на него тапать)
    with get_db_connection() as con:
        client_id = 3 # зададим произвольный айди
        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s', (client_id, )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/projects/allmytasks', methods=['GET'])
def assigned_tasks(): # просмотреть список назначенных задач в проектах
    with get_db_connection() as con:

        client_id = 3
        cur = con.cursor() # подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        assigned_tasks = cur.execute('SELECT t.name FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s', (client_id, )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for task in assigned_tasks:
            result += f"<p> {counter} : {task[0]} </p>"
            counter += 1

        return result


@app.route('/projects/allmytasks/history', methods=['GET'])
def history_task(): # просмотреть историю задачи
    with get_db_connection() as con:
        cur = con.cursor()  # подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s',
                                    (client_id,)).fetchall()
        # result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/projects/project', methods=['GET'])
def check_user_project(): # посмотреть проект
    with get_db_connection() as con:
        cur = con.cursor()  # подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s',
                                    (client_id,)).fetchall()
        # result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/projects/project/tasks', methods=['GET'])
def tasks_list_project(): # посмотреть список всех задач в проекте
    with get_db_connection() as con:
        client_id = 3 # зададим произвольный айди
        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s', (client_id, )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/projects/project/assigned_tasks', methods=['GET'])
def assigned_tasks_project(): # посмотреть список назначенных пользователю задач в проекте
    with get_db_connection() as con:
        client_id = 3 # зададим произвольный айди
        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s', (client_id, )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/register', methods=['GET'])
def register(): # зарегистрироваться (создать логин пароль)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/profile', methods=['GET'])
def edit_profile(): # изменить профиль (изменить логин пароль добавить электронную почту), выводим всю информацию о пользователе
                    # затем добавляем кнопки для изменения и добавления данных
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/projects/newproject', methods=['GET'])
def create_project(): # создать проект (ввести название проекта include)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/projects/project/newtask', methods=['GET'])
def create_task(): # создать задачу (ввести название и назначить исполнителя include)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()



@app.route('/projects/newproject', methods=['GET'])
def edit_task(): # создать проект (ввести название)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/projects/project/edit', methods=['GET'])
def edit_project(): # редактировать проект (удалить переименовать назначить дедлайн добавить другого пользователя в проект)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()