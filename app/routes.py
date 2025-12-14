from app import app
from app.forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, CreateNewProjectForm, EditTaskForm
from flask import render_template, request, flash, redirect, url_for, abort
from flask import request
import psycopg
import datetime


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

        task = cur.execute('SELECT t.name, t.deadline, t.priority, t.status, t.description, p.name, t.task_id FROM task as t '
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


@app.route('/login', methods=['GET', 'POST'])
def login(): # залогиниться (ввести логин пароль)

    login_form = LoginForm()
    if login_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

            login = cur.execute('SELECT login FROM users WHERE login = %s', (login_form.login.data,)).fetchone()
            password = cur.execute ('SELECT password FROM users WHERE login = %s', (login_form.login.data, )).fetchone()

            if ((login == login_form.login.data) and (password == login_form.password.data)):
                flash(f'Добро пожаловать {login_form.login.data}!', category='success')
                return redirect (url_for('profile'))


    return render_template('login.html', form=login_form)



@app.route('/register', methods=['GET', 'POST'])
def register(): # зарегистрироваться (создать логин пароль)

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit(): # этот метод проверяет валидность данных и тип запроса (POST), поэтому
                    # можно явно не указывать, что эта часть представления обрабатывает пользовательские данные
        with get_db_connection() as con:
            cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

            cur.execute('INSERT INTO users (surname, name, last_name, login, password, birthday, email_adress) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (reg_form.surname.data, reg_form.name.data, reg_form.last_name.data, reg_form.login.data,
                         reg_form.password.data, reg_form.birthday.data, reg_form.email_adress.data),)

            flash(f'Пользователь {reg_form.login.data} зарегистрирован', category='success')
            return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile(): # изменить профиль (изменить логин пароль добавить электронную почту), выводим всю информацию о пользователе
    # затем добавляем кнопки для изменения данных
    user_id = 3

    with get_db_connection() as con:
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        profile_data = cur.execute('SELECT surname, name, last_name, login, birthday, email_adress FROM users '
                               'WHERE user_id = %s', (user_id,)).fetchone()
    profile_data_dictionary = { # оказалось что просто передать нельзя = надо преобразовать кортеж в словарь
        'surname': profile_data[0],
        'name': profile_data[1],
        'last_name': profile_data[2],
        'login': profile_data[3],
        'birthday': profile_data[4],
        'email_adress': profile_data[5]
    }

    edit_profile_form = EditProfileForm(data=profile_data_dictionary) # получили текущие данные и передаём их в форму для отображения


    if edit_profile_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute('UPDATE users SET surname = %s, name = %s, last_name = %s, login = %s, birthday = %s, email_adress = %s WHERE user_id = %s',
                        (edit_profile_form.surname.data, edit_profile_form.name.data, edit_profile_form.last_name.data,
                             edit_profile_form.login.data, edit_profile_form.birthday.data, edit_profile_form.email_adress.data, user_id))
            flash('Данные успешно обновлены', category='success')
            return redirect(url_for('check_profile'))

    return render_template('edit_profile.html', form=edit_profile_form)

@app.route('/projects/newproject', methods=['GET', 'POST'])
def create_project(): # создать проект (ввести название обязательно, дата создания, описание)
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

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id): # редактировать задачу (удалить, переименовать, переназначить исполнителя,
    # изменить приоритет, переназначить дедлайн, изменить статус, изменить описание задачи - что нужно сделать)
    with get_db_connection() as con:
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        task_data = cur.execute('SELECT name, deadline, priority, status, description, executor_id FROM task '
                                   'WHERE task_id = %s', (task_id,)).fetchone()
        # получаю логин исполнителя, чтобы В ФОРМЕ отобразить, кто исполняет задачу (как при просмотре задачи)
        executor_login = cur.execute('SELECT u.login FROM users as u JOIN task as t ON t.executor_id = u.user_id WHERE task_id = %s', (task_id, )).fetchone()

        get_status = cur.execute('SELECT name, name FROM status').fetchall() # получаем статусы, чтобы отобразить
                                                                   # их в выпадающем списке
        all_status = [(row[0], row[1]) for row in get_status]

        all_priority = [
            (1, 1),
            (2, 2),
            (3, 3)
        ]


    task_data_dictionary = {
        'name': task_data[0],
        'deadline': task_data[1],
        'executor_login': executor_login[0],
        'priority': task_data[2],
        'status': task_data[3],
        'description': task_data[4]
    }
    # передаю в форму ТЕКУЩИЕ данные задачи
    edit_task_form = EditTaskForm(data=task_data_dictionary)
    edit_task_form.status.choices = all_status
    edit_task_form.priority.choices = all_priority

    if edit_task_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()
            # получаем айди нового исполнителя по введённому логину
            new_exec_id = cur.execute('SELECT user_id FROM users WHERE login = %s', (edit_task_form.executor_login.data, )).fetchone()
            if new_exec_id is not None:
                new_exec_id = new_exec_id[0] # вытаскиваем число из кортежа (тк изначально оно выдаётся в формате (2) )
            else: new_exec_id = None

            if (new_exec_id is None) or (edit_task_form.deadline.data < datetime.date.today()):
                if new_exec_id is None:
                    flash(message='Пользователя с таким логином не существует', category='danger')
                    return redirect(url_for('edit_task', task_id=task_id))
                if edit_task_form.deadline.data < datetime.date.today():
                    flash(message='Дедлайн не может быть прошедшей датой', category='danger')
                    return redirect(url_for('edit_task', task_id=task_id))
            # на этом функция прекращает свою работу

            cur.execute(
                'UPDATE task SET name = %s, deadline = %s, executor_id = %s, priority = %s, status = %s, description = %s WHERE task_id = %s',
                (edit_task_form.name.data, edit_task_form.deadline.data, new_exec_id,
                 edit_task_form.priority.data, edit_task_form.status.data, edit_task_form.description.data,
                 task_id))

            # тут же создадим запись о новом изменении (нужно определить категорию изменения исходя из ОБНОВЛЁННЫХ ПОЛЕЙ
            # и записать логин, айди автора изменения, тип изменения, таск айди, текущую дату и время и айди типа изменения
            # при этом надо выводить ПОСЛЕДНЕЕ ИЗМЕНЕНИЕ ДЛЯ ПРОСМОТРА в задаче - сортирую по дате и вывожу первую
            # - то есть самое позднее изменение


            flash('Данные успешно обновлены', category='success')
            return redirect(url_for('check_task', task_id=task_id))

    return render_template('edit_task.html', form=edit_task_form)