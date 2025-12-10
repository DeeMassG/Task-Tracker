from app import app
from flask import render_template
from flask import request
import psycopg


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



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
        client_id = 1 # зададим произвольный айди. Получим наверное из сессии (но точно не из предыдущего роута)
        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_projects = cur.execute('SELECT p.name, p.project_id FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE user_id = %s', (client_id, )).fetchall()

        return render_template('projects.html', user_projects=user_projects)

@app.route('/allmytasks', methods=['GET'])
def assigned_tasks(): # просмотреть список назначенных пользователю задач среди всех проектов (по ним можно перейти к самим задачам)
    with get_db_connection() as con:

        client_id = 3 # получаем айди клиента из сессии и передаём его в запрос
        cur = con.cursor()
        assigned_tasks = cur.execute('SELECT t.name, u.login FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s', (client_id, )).fetchall()
        #result = "<h1>Список моих проектов:</h1>"

        return render_template ('all_my_tasks', assigned_tasks = assigned_tasks) # передаём в шаблон логин

#---------------------------------------------------------
@app.route('/tasks/<int:task_id>/history', methods=['GET'])
def history_task(task_id): # просмотреть историю задачи (название проекта откуда она, название задачи
                    # логин автора изменения, тип изменения и дата
    with get_db_connection() as con:
        task_id = 2 # получаем айди задачи, информацию о которой хотим посмотреть
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        # сначала получаем инфо о задаче
        task = cur.execute('SELECT p.name, t.name FROM task as t JOIN '
                                    'project as p ON t.project_id = p.project_id WHERE task_id = %s',
                                    (task_id,)).fetchone()

        # теперь получаем инфо об изменениях этой задачи
        history = cur.execute('SELECT c.change_author, type, c.data_change FROM change as c WHERE task_id = %s', (task_id, )).fetchone()
        # выводим историю конкретной задачи с указанием названия проекта и задачи

        return render_template('task_history.html', task=task, history=history)

@app.route('/tasks/<int:task_id>', methods = (['GET']))
def check_task(task_id): # Посмотреть информацию о конкретной задаче в проекте
    with get_db_connection() as con:
        cur = con.cursor() # курсор для выполнения запросов к бд

        task = cur.execute('SELECT t.name, t.deadline, t.priority, t.status, t.description, p.name FROM task as t '
                           'JOIN project as p ON t.project_id = t.project_id JOIN users as u '
                           'ON t.creator_id = u.user_id  WHERE task_id = %s', (task_id,)).fetchone()

        login_owner = cur.execute('SELECT u.login FROM users as u JOIN task ON u.user_id = creator_id WHERE task_id = %s', (task_id,)).fetchone()
        login_exec = cur.execute('SELECT u.login FROM users as u JOIN task ON u.user_id = executor_id WHERE task_id = %s', (task_id,)).fetchone()

        return render_template('check_task.html', task=task, owner=login_owner, executor=login_exec)


@app.route('/projects/<int:project_id>', methods=['GET'])
def check_user_project(project_id): # посмотреть проект (вывести инфо о нём без задач)
    with get_db_connection() as con:
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        description_project = cur.execute('SELECT login, p.name, date_of_creation, description, p.project_id FROM users as u JOIN '
                                    'project as p ON u.user_id = p.owner_project_id WHERE project_id = %s',
                                    (project_id,)).fetchone()

        return render_template('check_user_project.html', description_project=description_project)

@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
def tasks_list_project(project_id): # посмотреть список всех задач в конкретном проекте (выводим названия
                          # по которым можно перейти к конкретным задачам
    with get_db_connection() as con:

        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_tasks = cur.execute('SELECT name, task_id FROM task WHERE project_id = %s', (project_id,)).fetchall()

        project_name = cur.execute('SELECT name FROM project WHERE project_id = %s', (project_id, )).fetchone()

        return render_template('tasks_list_project.html', user_tasks=user_tasks, project_name=project_name)

@app.route('/projects/<int:project_id>/assigned_tasks', methods=['GET'])
def assigned_tasks_project(project_id): # посмотреть список назначенных пользователю задач в проекте
                              # выводим только названия, по которым можно перейти к самим задачам

    with get_db_connection() as con:
        user_id = 3 # зададим айди пользователя
        project_id = 2 # зададим айди проекта в котором хотим посмотреть

        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        user_tasks = cur.execute('SELECT t.name FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s AND project_id = %s', (user_id, project_id )).fetchall()
        return render_template('assigned_tasks_project.html', user_tasks=user_tasks)

@app.route('/profile', methods=['GET'])
def check_profile():  # посмотреть профиль юзера - выводим всю информацию о пользователе

    with get_db_connection() as con:
        user_id = 3
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        profile_data = cur.execute('SELECT surname, name, last_name, login, birthday, email_adress FROM users '
                                       'WHERE user_id = %s', (user_id, )).fetchone()

        return render_template('profile.html', profile_data=profile_data)


@app.route('/login', methods=['GET'])
def login(): # залогиниться (ввести логин пароль)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        login_connect = cur.execute( ( )).fetchall()


@app.route('/register', methods=['GET'])
def register(): # зарегистрироваться (создать логин пароль)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_reg = cur.execute( ( )).fetchall()


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

        return render_template('')

@app.route('/projects/newproject', methods=['GET', 'POST'])
def create_project(): # создать проект (ввести название обязательно, дата создания, описание, )
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        if request.method == 'POST':
            # Получаем данные из формы
            project_name = request.form.get('name')

            name_project = cur.execute( ( )).fetchall()

        else: # выводим форму для заполнения данных
            cur = con.cursor()




@app.route('/projects/<int:project_id>/create_task', methods=['GET', 'POST'])
def create_task(project_id): # создать задачу (ввести название и назначить исполнителя include)
    with get_db_connection() as con:

        cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции


        return render_template('create_task.html', project_id=project_id)




@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(): # редактировать проект (удалить переименовать назначить дедлайн добавить другого пользователя в проект)
    with get_db_connection() as con:

        if request.method == 'POST':
            name = 0

        else:
            cur = con.cursor()
            projects = cur.execute( ( )).fetchall()

@app.route('/tasks/<int:task>/edit', methods=['GET', 'POST'])
def edit_task(): # редактировать задачу (удалить, переименовать, переназначить исполнителя,
    # изменить приоритет, переназначить дедлайн, изменить статус, изменить описание задачи - что нужно сделать)
    with get_db_connection() as con:

        if request.method == 'POST':
            name = 0

        else:
            cur = con.cursor()
            projects = cur.execute( ( )).fetchall()