from app import app
from flask import render_template
from flask import request
import psycopg


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def test_connection():
    return ''



def get_db_connection(): # вынесем подключение к бд в отдельную функцию
    return psycopg.connect(
        host=app.config['DB_SERVER'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        dbname=app.config['DB_NAME']
    )

@app.route('/projects', methods=['GET'])
def projects_list(): # просмотреть список проектов пользователя (список названий с возможностью перейти к каждому проекту (описание))
    with get_db_connection() as con:
        client_id = 3 # зададим произвольный айди
        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
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
def assigned_tasks(): # просмотреть список назначенных пользователю задач среди всех проектов (по ним можно перейти к самим задачам)
    with get_db_connection() as con:

        client_id = 3
        cur = con.cursor()
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

#---------------------------------------------------------
@app.route('/tasks/<int:task_id>/history', methods=['GET'])
def history_task(task_id): # просмотреть историю задачи (название проекта откуда она, название задачи
                    # логин автора изменения, тип изменения и дата
    with get_db_connection() as con:
        task_id = 2
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        # сначала получаем инфо о задаче
        task = cur.execute('SELECT p.name, t.name FROM task as t JOIN '
                                    'project as p ON t.project_id = p.project_id WHERE task_id = %s',
                                    (task_id,)).fetchone()

        # теперь получаем инфо об изменениях этой задачи
        history = cur.execute('SELECT change_author, type, data_change FROM change WHERE task_id = %s', (task_id, )).fetchone()
        result = ''

        # выводим историю конкретной задачи с указанием названия проекта и задачи

        result += f"<p> {task[0]} : {task[1]} : {history[0]} : {history[1]} : {history[2]} </p>"

        return result

@app.route('/tasks/int:<task_id>', methods = (['GET']))
def check_task(task_id):
    with get_db_connection() as con:
        cur = con.cursor() # курсор для выполнения запросов к бд
        task_id = 2
        task = cur.execute('SELECT p.name, t.name, t.creator_id, t.executor_id, t.deadline, t.priority, t.status, t.description FROM task as t '
                           'JOIN project as p ON t.project_id = t.project_id JOIN users as u '
                           'ON t.creator_id = u.user_id  WHERE task_id = %s', (task_id,)).fetchone()
    if not task:
        return "Задача не найдена", 404

    return render_template('base.html', task=task)

@app.route('/projects/<int:project_id>', methods=['GET'])
def check_user_project(project_id): # посмотреть проект (вывести инфо о нём без задач)
    with get_db_connection() as con:
        project_id = 2
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_project = cur.execute('SELECT login, p.name, date_of_creation, description FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE project_id = %s',
                                    (project_id,)).fetchall()

        result = ''
        counter = 1
        for project in user_project:
            result += (f"<p> {counter} Создатель:  {project[0]}  Название:  {project[1]} "
                       f": Дата создания:  {project[2]}  Описание :  {project[3]}  </p>")

            counter += 1

        return result

@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
def tasks_list_project(project_id): # посмотреть список всех задач в конкретном проекте (выводим названия
                          # по которым можно перейти к конкретным задачам
    with get_db_connection() as con:

        project_id = 2
        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT name FROM task WHERE project_id = %s', (project_id,)).fetchall()

        result = ''
        counter = 1
        for name in user_projects:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/projects/project/assigned_tasks', methods=['GET'])
def assigned_tasks_project(): # посмотреть список назначенных пользователю задач в проекте
                              # выводим только названия, по которым можно перейти к самим задачам

    with get_db_connection() as con:
        user_id = 3 # зададим айди пользователя
        project_id = 2 # зададим айди проекта в котором хотим посмотреть

        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        user_tasks = cur.execute('SELECT t.name FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s AND project_id = %s', (user_id, project_id )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"
        result = ''
        counter = 1
        for name in user_tasks:
            result += f"<p> {counter} : {name[0]} </p>"
            counter += 1

        return result

@app.route('/profile', methods=['GET'])
def check_profile():  # посмотреть профиль юзера - выводим всю информацию о пользователе

    with get_db_connection() as con:
        user_id = 3
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        profile_data = cur.execute('SELECT surname, name, last_name, login, password, birthday, email_adress FROM users '
                                       'WHERE user_id = %s', (user_id, )).fetchone()

        result = ''

        result += f"<p>Фамилия: {profile_data[0]}</p>"
        result += f"<p>Имя: {profile_data[1]}</p>"
        result += f"<p>Отчество: {profile_data[2]}</p>"
        result += f"<p>Логин: {profile_data[3]}</p>"
        result += f"<p>Пароль: {profile_data[4]}</p>"
        result += f"<p>Дата рождения: {profile_data[5]}</p>"
        result += f"<p>Адрес электронной почты: {profile_data[6]}</p>"

    return result

@app.route('/register', methods=['GET'])
def register(): # зарегистрироваться (создать логин пароль)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile(): # изменить профиль (изменить логин пароль добавить электронную почту), выводим всю информацию о пользователе
                    # затем добавляем кнопки для изменения данных
    with get_db_connection() as con:

        user_id = 3
        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        # Обработка POST запроса (изменение данных)
        if request.method == 'POST':
            # Получаем данные из формы
            new_surname = request.form.get('surname')
            new_name = request.form.get('name')
            new_lastname = request.form.get('last_name')
            new_login = request.form.get('login')
            new_password = request.form.get('password')
            new_birthday = request.form.get('birthday')
            new_email = request.form.get('email')

            # Обновляем данные в базе
            cur.execute('UPDATE users SET surname = %s, name = %s, last_name = %s, login = %s, password = %s, '
                        'birthday = %s, email_adress = %s WHERE user_id = %s', (new_surname, new_name, new_lastname, new_login, new_password, new_birthday, new_email, user_id)).fetchall()
        else:
            profile_data = cur.execute('SELECT surname, name, last_name, login, password, birthday, email_adress FROM users '
                                       'WHERE user_id = %s', (user_id, )).fetchone()

            result = ''

            result += f"<p>Фамилия: {profile_data[0]}</p>"
            result += f"<p>Имя: {profile_data[1]}</p>"
            result += f"<p>Отчество: {profile_data[2]}</p>"
            result += f"<p>Логин: {profile_data[3]}</p>"
            result += f"<p>Пароль: {profile_data[4]}</p>"
            result += f"<p>Дата рождения: {profile_data[5]}</p>"
            result += f"<p>Адрес электронной почты: {profile_data[6]}</p>"

        return result

@app.route('/projects/create_project', methods=['GET', 'POST'])
def create_project(): # создать проект (ввести название проекта include)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        if request.method == 'POST':
            # Получаем данные из формы
            project_name = request.form.get('name')

            name_project = cur.execute( ( )).fetchall()

        else: # выводим форму для заполнения данных
            cur = con.cursor()




@app.route('/projects/project/create_task', methods=['GET', 'POST'])
def create_task(): # создать задачу (ввести название и назначить исполнителя include)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()



@app.route('/projects/newproject', methods=['GET', 'POST'])
def edit_task(): # создать проект (ввести название)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute( ( )).fetchall()


@app.route('/projects/project/edit', methods=['GET', 'POST'])
def edit_project(): # редактировать проект (удалить переименовать назначить дедлайн добавить другого пользователя в проект)
    with get_db_connection() as con:

        if request.method == 'POST':
            name = 0

        else:
            cur = con.cursor()
            projects = cur.execute( ( )).fetchall()