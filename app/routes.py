from app import app
from app.forms import (RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, CreateNewProjectForm,
                       AddUserToProjectForm, EditTaskForm, EditProjectForm, DeleteProjectForm, CreateTaskForm, DeleteTaskForm,
                        DeleteUserFromProjectForm, OutOfProjectForm)
from flask import render_template, request, flash, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from urllib.parse import urlsplit
import psycopg
import datetime


# это класс, в котором будут храниться данные вошедшего пользователя
# Для текущей сессии (поля - это инфа, которую будем использовать в любом месте кода
class User(UserMixin):
    def __init__(self, user_id, login, email_adress):
        self.user_id = user_id
        self.login = login
        self.email_adress = email_adress

    def get_id(self): # переопределим метод, чтобы в коде можно было обращаться к полю user_id а не id
        return str(self.user_id)

# Функция load_user(user_id) подгружает данные в current_user из бд, используя user_id - айдишник пользователя
# а она берёт айди из сессии


@login_manager.user_loader
def load_user(user_id):
    with get_db_connection() as con:
        cur = con.cursor()
        current_user_data = cur.execute('SELECT user_id, login, email_adress FROM users WHERE user_id = %s', (user_id, )).fetchone()
        # проверку на наличие данных можно не делать, так как сессия уже открыта. Значит юзер вошёл
        return User(current_user_data[0], current_user_data[1], current_user_data[2])

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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found_404.html'), 404


@app.route('/register', methods=['GET', 'POST'])
def register(): # зарегистрироваться (создать логин пароль)
    if current_user.is_authenticated:
        flash(message='Вы уже зарегистрированы', category='warning')
        return redirect(url_for('index'))

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit(): # этот метод проверяет валидность данных и тип запроса (POST), поэтому
                    # можно явно не указывать, что эта часть представления обрабатывает пользовательские данные

        with get_db_connection() as con:
            cur = con.cursor() #Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

            check_login = cur.execute('SELECT login FROM users WHERE login = %s', (reg_form.login.data, )).fetchone() # проверим, есть ли юзер с таким же именем
            if (check_login is not None) and (check_login != reg_form.login.data):
                flash(message=f'Пользователь с именем { reg_form.login.data } уже зарегистрирован!', category='warning')
                return render_template('register.html', form=reg_form)

            password_hash = generate_password_hash(reg_form.password.data)  # генерируем хеш пароля
            cur.execute('INSERT INTO users (surname, name, last_name, login, password, birthday, email_adress) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (reg_form.surname.data, reg_form.name.data, reg_form.last_name.data, reg_form.login.data,
                         password_hash, reg_form.birthday.data, reg_form.email_adress.data),)

            flash(f'Пользователь { reg_form.login.data } зарегистрирован. Вы перенаправлены на страницу для входа.', category='success')
            return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login(): # нужно залогинить юзера, подключить ему сессию
    if current_user.is_authenticated:
        flash(message='Вы уже вошли в систему', category='warning')
        return redirect(url_for('index')) # если юзер вдруг решит войти повторно

    login_form = LoginForm()
    if login_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
            # проверяем, существует ли такой логин, пытаясь взять его из бд
            user_data = cur.execute('SELECT user_id, login, password, email_adress FROM users WHERE login = %s', (login_form.login.data,)).fetchone()
            if user_data is None or not check_password_hash(user_data[2], login_form.password.data):
                if user_data is None:
                    flash(message='Логин введён неверно', category='danger')
                    return render_template('login.html', form=login_form)
                else:
                    flash(message='Неверное имя пользователя или пароль', category='danger')
                    return render_template('login.html', form=login_form)
            user_id = user_data[0]
            login = user_data[1]
            email_adress = user_data[3]

            user = User(user_id, login, email_adress)
            login_user(user, remember=login_form.remember_me.data)
            flash(message=f'Добро пожаловать, { current_user.login }' , category='success')
            next = request.args.get('next')
            if not next or urlsplit(next).netloc != '': # проверяем есть ли редирект на чужой ресурс
                next = url_for('index')
            return redirect(next)

    return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', category='info')
    return redirect(url_for('index'))


@app.route('/projects', methods=['GET'])
@login_required
def projects_list(): # просмотреть список проектов пользователя (список названий с возможностью перейти к каждому проекту (описание))
    # и свои проекты, и совместные
    with get_db_connection() as con:
        client_id = current_user.user_id
        cur = con.cursor()
        # надо вывести проекты пользователя и совместные проекты разделив их на две группы

        # Свои проекты = значит он создатель
        user_projects = cur.execute('SELECT p.name, p.project_id FROM users as u JOIN '
                                    'project as p ON u.user_id = p.creator_project_id WHERE user_id = %s', (client_id, )).fetchall()
        #print(user_projects, "юзер")

        role_names = cur.execute('SELECT role_name FROM role').fetchall()
        role_names = [role[0] for role in role_names] # вытаскиваем из кортежей названия [('владелец', ) итд]
        #print(role_names[0], role_names[1], "роли")

        # выводим совместные проекты именно для ТЕКУЩЕГО юзера = он НЕ создатель, и он либо админ, либо участник
        shared_projects = cur.execute('SELECT p.name, p.project_id FROM project as p JOIN part_in_project as pp ON  p.project_id = pp.project_id '
                                      'WHERE (p.creator_project_id != pp.user_id AND pp.user_id = %s) '
                                      'AND (pp.role_name = %s OR pp.role_name = %s)', (client_id, role_names[0], role_names[1], )).fetchall()
        #print(shared_projects, "общие")

        return render_template('projects.html', user_projects=user_projects, shared_projects=shared_projects)


@app.route('/allmytasks', methods=['GET'])
@login_required
def assigned_tasks(): # просмотреть список назначенных пользователю задач среди всех проектов (по ним можно перейти к самим задачам)
    with get_db_connection() as con:

        client_id = current_user.user_id # получаем айди клиента из сессии и передаём его в запрос
        cur = con.cursor()
        assigned_tasks = cur.execute('SELECT t.task_id, t.name FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s', (client_id, )).fetchall()

        return render_template ('all_my_tasks', assigned_tasks = assigned_tasks) # передаём в шаблон список задач


@app.route('/tasks/<int:task_id>/history', methods=['GET'])
@login_required
def history_task(task_id): # просмотреть историю задачи (название проекта откуда она, название задачи
                    # логин автора изменения, тип изменения и дата
    with get_db_connection() as con:
        cur = con.cursor()
        # сначала получаем инфо о задаче
        task = cur.execute('SELECT p.name, t.name FROM task as t JOIN '
                                    'project as p ON t.project_id = p.project_id WHERE task_id = %s',
                                    (task_id,)).fetchone()
        # теперь получаем инфо о последнем изменении этой задачи
        history = cur.execute('SELECT change_author, type, data_change FROM change WHERE task_id = %s ORDER BY change_id DESC LIMIT 1', (task_id, )).fetchone()
        # return [history for history in history]
        return render_template('task_history.html', task=task, history=history)


@app.route('/tasks/<int:task_id>', methods = (['GET']))
@login_required
def check_task(task_id): # Посмотреть информацию о конкретной задаче в проекте
    with get_db_connection() as con:
        cur = con.cursor() # курсор для выполнения запросов к бд

        task = cur.execute('SELECT t.name, t.deadline, t.priority, t.status, t.description, p.name, t.task_id FROM task as t '
                           'JOIN project as p ON t.project_id = p.project_id WHERE task_id = %s', (task_id,)).fetchone()

        login_owner = cur.execute('SELECT u.login FROM users as u JOIN task ON u.user_id = creator_id WHERE task_id = %s', (task_id,)).fetchone()
        login_exec = cur.execute('SELECT u.login FROM users as u JOIN task ON u.user_id = executor_id WHERE task_id = %s', (task_id,)).fetchone()
        return render_template('check_task.html', task=task, owner=login_owner, executor=login_exec)


@app.route('/projects/<int:project_id>', methods=['GET'])
@login_required
def check_user_project(project_id): # посмотреть проект (вывести инфо о нём без задач)
    with get_db_connection() as con:
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        description_project = cur.execute('SELECT login, p.name, date_of_creation, description, p.project_id FROM users as u JOIN '
                                    'project as p ON u.user_id = p.creator_project_id WHERE project_id = %s',
                                    (project_id,)).fetchone()
        # выведем роль пользователя в этом проекте (уровень доступа, его возможности в проекте)
        client_id = current_user.user_id
        role_in_project = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s', (project_id, client_id, )).fetchone()
        role_in_project = role_in_project[0] # вытаскиваем из кортежа строку с названием роли текущего пользователя
        role_owner = 'владелец' # с этой переменной будем сравнивать роль текущего пользователя при отображении кнопок

        return render_template('check_user_project.html', description_project=description_project,
                               role_in_project=role_in_project, role_owner=role_owner)

@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
@login_required
def tasks_list_project(project_id): # посмотреть список всех задач в конкретном проекте (выводим названия
                          # по которым можно перейти к конкретным задачам
    with get_db_connection() as con:

        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции
        user_tasks = cur.execute('SELECT name, task_id FROM task WHERE project_id = %s', (project_id,)).fetchall()

        project_name = cur.execute('SELECT name FROM project WHERE project_id = %s', (project_id, )).fetchone()

        return render_template('tasks_list_project.html', user_tasks=user_tasks,
                               project_name=project_name, project_id=project_id)

@app.route('/projects/<int:project_id>/assigned_tasks', methods=['GET'])
@login_required
def assigned_tasks_project(project_id): # посмотреть список назначенных пользователю задач в проекте
                              # выводим только названия, по которым можно перейти к самим задачам

    with get_db_connection() as con:
        user_id = current_user.user_id # зададим айди пользователя
        cur = con.cursor() # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        project_name = cur.execute('SELECT name FROM project WHERE project_id = %s', (project_id,)).fetchone()

        user_tasks = cur.execute('SELECT t.name, t.task_id FROM users as u JOIN '
                                    'task as t ON u.user_id = t.executor_id'
                                     ' WHERE user_id = %s AND project_id = %s', (user_id, project_id )).fetchall()
        # return user_tasks[0]
        return render_template('assigned_tasks_project.html', user_tasks=user_tasks,
                               project_name=project_name, project_id=project_id)

@app.route('/profile', methods=['GET'])
@login_required
def check_profile():  # посмотреть профиль юзера - выводим всю информацию о пользователе

    with get_db_connection() as con:
        user_id = current_user.user_id
        cur = con.cursor()  # Подключаем клиентский курсор. Он будет выполнять sql запросы и транзакции

        profile_data = cur.execute('SELECT surname, name, last_name, login, birthday, email_adress FROM users '
                                       'WHERE user_id = %s', (user_id, )).fetchone()

        return render_template('profile.html', profile_data=profile_data)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(): # изменить профиль (изменить логин пароль добавить электронную почту), выводим всю информацию о пользователе
    user_id = current_user.user_id

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

@app.route('/profile/edit/password', methods=['GET', 'POST'])
@login_required
def change_password():

    user_id = current_user.user_id
    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor() # получим хеш ТЕКУШЕГО ПАРОЛЯ пользователя
            hash_current_password = cur.execute('SELECT password FROM users WHERE user_id = %s', (user_id,)).fetchone()
            hash_current_password = hash_current_password[0]

            # проверка на соответствие хеша введённого пароля с хешем текущего пароля из базы
            if check_password_hash(hash_current_password, password_form.password.data):
                new_password = generate_password_hash(password_form.new_password.data) # генерим хеш для нового пароля

                # проверка на повтор старого пароля
                if check_password_hash(hash_current_password, password_form.new_password.data):

                    flash(message='Старый и новый пароль не должны повторяться!', category='danger')
                    return render_template('change_password.html', form=password_form)

                cur.execute('UPDATE users SET password = %s WHERE user_id = %s', (new_password, user_id))
                flash(message='Пароль обновлён', category='success')
                return redirect(url_for('check_profile'))
            else:
                flash(message='Текущий пароль введён неверно', category='danger')
                return render_template('change_password.html', form=password_form)

    return render_template('change_password.html', form=password_form)

@app.route('/projects/newproject', methods=['GET', 'POST'])
@login_required
def create_project(): # создать проект (ввести название обязательно, дата создания, описание)

    user_id = current_user.user_id
    new_project_form = CreateNewProjectForm()
    if new_project_form.validate_on_submit():

        with get_db_connection() as con:
            cur = con.cursor()
            # создаю запись о проекте в project
            cur.execute('INSERT INTO project (creator_project_id, name, description) VALUES (%s, %s, %s)',
                        (user_id, new_project_form.name.data, new_project_form.description.data))

            # получаю сгенерированный базой айдишник только что созданного проекта
            project_id = cur.execute('SELECT project_id FROM project WHERE creator_project_id = %s '
                                     'AND name = %s AND description = %s',
                                     (user_id, new_project_form.name.data, new_project_form.description.data)).fetchone()
            # получаю айди и имя роли для создателя проекта
            role_name = 'владелец'
            name_and_role_id = cur.execute('SELECT role_name, role_id FROM role WHERE role_name = %s', (role_name, )).fetchone()

            # добавим юзера и права в проекте в таблицу part_in_project (создатель проекта = владелец(админ))
            cur.execute('INSERT INTO part_in_project (user_id, role_name, project_id, role_id) VALUES (%s, %s, %s, %s)',
                        (user_id, name_and_role_id[0], project_id[0], name_and_role_id[1]))

            flash(message='Проект успешно создан', category='success')
            return redirect(url_for('projects_list'))

    return render_template('create_new_project.html', form=new_project_form)



@app.route('/projects/<int:project_id>/create_task', methods=['GET', 'POST'])
@login_required
def create_task(project_id): # создать задачу (ввести название и назначить исполнителя include)
    # только владелец может создать задачу для кого то кроме себя. При этом исполнитель должен
    # быть участником проекта, иначе = ошибка добавления
    user_id = current_user.user_id
    creator_id = user_id
    with get_db_connection() as con:
        cur = con.cursor()
        login_creator_default = cur.execute('SELECT login FROM users WHERE user_id = %s', (user_id, )).fetchone()
        # получаю роль юзера, который хочет создать задачу
        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id,)).fetchone()
        role_user = role_user[0] # вытаскиваю из кортежа
        # нужно сравнить её с ролью "владелец" в html шаблоне, чтобы отрисовать или скрыть поле с логином исполнителя
        role_owner = 'владелец'
    executor_login = {'executor_login' : login_creator_default[0]} # по умолчанию исполнитель = создатель задачи

    all_priority = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]

    create_task_form = CreateTaskForm(data=executor_login)
    create_task_form.priority.choices = all_priority

    if create_task_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor() # теперь берём айди по логину назначенного юзера
            executor_id = cur.execute('SELECT user_id FROM users WHERE login = %s',
                                     (create_task_form.executor_login.data,)).fetchone()

            if (executor_id is None) or (create_task_form.deadline.data < datetime.datetime.now()):
                if executor_id is None:
                    flash(message='Пользователя с таким логином не существует', category='danger')
                    return render_template('create_task.html', form=create_task_form, project_id=project_id)

                if create_task_form.deadline.data < datetime.datetime.now():
                    flash(message='Дедлайн не может быть прошедшей датой', category='danger')
                    return render_template('create_task.html', form=create_task_form, project_id=project_id)

            executor_id = executor_id[0]  # вытаскиваем айди из кортежа
            # проверяем, что указанный исполнитель ДОБАВЛЕН В ЭТОТ ПРОЕКТ
            check_executor = cur.execute(
                        'SELECT user_id FROM part_in_project WHERE project_id = %s and user_id = %s',
                        (project_id, executor_id)).fetchone()
            if check_executor is None:
                flash(message='Указанный пользователь не состоит в проекте', category='danger')
                return render_template('create_task.html', form=create_task_form, project_id=project_id)

            status = cur.execute('SELECT status_id FROM status WHERE name = %s', ('Новая',)).fetchone()
            status_name = 'Новая'
            status_id = status[0] # получаю из кортежа запроса айди статуса

            cur.execute('INSERT INTO task (name, deadline, creator_id, executor_id, priority, status, description, status_id, project_id) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (create_task_form.name.data, create_task_form.deadline.data,
            creator_id, executor_id, create_task_form.priority.data, status_name, create_task_form.description.data, status_id, project_id))
            flash(message='Задача успешно создана', category='success')
            return redirect(url_for('check_user_project', project_id=project_id))

    return render_template('create_task.html', form=create_task_form,
                           project_id=project_id, role_user=role_user, role_owner=role_owner)


@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id): # редактировать проект (удалить переименовать назначить дедлайн

    user_id = current_user.user_id
    with get_db_connection() as con:
        cur = con.cursor()
        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id, )).fetchone()
    if (role_user is None) or (role_user[0] != 'владелец'):
        # редактировать проект могут только юзеры с правами владельца (это и создатель, в том числе)
        flash(message='У Вас недостаточно прав для этого действия', category='danger')
        return redirect(url_for('check_user_project', project_id=project_id))

    with get_db_connection() as con:
        cur = con.cursor()
        project_data = cur.execute('SELECT name, description FROM project WHERE project_id = %s',
                                   (project_id,)).fetchone()

    project_data_dictionary = {
        'name': project_data[0],
        'description': project_data[1]
    }
    edit_project_form = EditProjectForm(data=project_data_dictionary) # передаю текущее название и описание проекта

    if edit_project_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()
            cur.execute('UPDATE project SET name = %s, description = %s WHERE project_id = %s',
                        (edit_project_form.name.data, edit_project_form.description.data, project_id))
            flash('Данные успешно обновлены', category='success')
            return redirect(url_for('check_user_project',project_id=project_id))

    return render_template('edit_project.html', form=edit_project_form)

@app.route('/projects/<int:project_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):

    user_id = current_user.user_id # получаю айдишник текущего юзера
    with get_db_connection() as con:
        cur = con.cursor()

        creator_project_id = cur.execute('SELECT creator_project_id FROM project WHERE project_id = %s', (project_id, )).fetchone()
        creator_project_id = creator_project_id[0]

    if creator_project_id != user_id: # удалить проект может только создатель проекта (он и владелец по умолчанию)
        flash(message='У Вас недостаточно прав для этого действия. Удалить проект может только создатель.', category='danger')
        return redirect(url_for('check_user_project', project_id=project_id))

    delete_project_form = DeleteProjectForm()

    if delete_project_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()

            # сначала удаляем ВСЕ ЗАДАЧИ ИЗ ЭТОГО ПРОЕКТА
            cur.execute('DELETE FROM task WHERE project_id = %s', (project_id, ))
            # а теперь сам проект
            cur.execute('DELETE FROM project WHERE project_id = %s', (project_id, ))
            flash(message='Проект удалён. Вы перенаправлены на страницу Ваших проектов', category='success')
            return redirect(url_for('projects_list'))

    return render_template('delete_project.html', form=delete_project_form, project_id=project_id)

@app.route('/project/<int:project_id>/add_user', methods=['GET', 'POST'])
@login_required
def add_user_to_project(project_id):

    user_id = current_user.user_id
    with get_db_connection() as con:
        cur = con.cursor()
        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id,)).fetchone()
    if (role_user is None) or (role_user[0] != 'владелец'):  # добавить пользователей могут только юзеры с правами владельца
        flash(message='У Вас недостаточно прав для этого действия', category='danger')
        return redirect(url_for('check_user_project', project_id=project_id))

    add_user_form = AddUserToProjectForm()

    with get_db_connection() as con:
        cur = con.cursor()

        roles = cur.execute('SELECT role_name FROM role ORDER BY role_name DESC').fetchall()
        roles = [(row[0]) for row in roles] # вытаскиваем из списка кортежей роли в проекте (desc - обратный порядок,
                                            # чтобы первым в списке была роль участник)
        add_user_form.role.choices = roles
        # добавил значения в выпадающий список и отправляю форму в шаблон на рендер
    if add_user_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()

            # достаём айдишник добавляемого пользователя, чтобы добавить его в бд
            add_user_id = cur.execute('SELECT user_id FROM users WHERE login = %s', (add_user_form.login.data, )).fetchone()
            if add_user_id is None:
                flash(message='Пользователя с таким логином не существует', category='danger')
                return render_template('add_user_to_project.html', project_id=project_id, form=add_user_form)

            add_user_id = add_user_id[0] # достаём из кортежа, чтобы правильно передать в insert
            # проверяем, есть ли такой юзер в проекте (если УЖЕ есть то не добавляем)
            check_user = cur.execute('SELECT user_id FROM part_in_project WHERE project_id = %s '
                                     'AND user_id = %s',(project_id, add_user_id)).fetchone()
            if check_user is not None:
                flash(message=f'Пользователь {add_user_form.login.data} уже состоит в проекте', category='warning')
                return redirect(url_for('check_user_project', project_id=project_id))

            role_id_add_user = cur.execute('SELECT role_id FROM role WHERE role_name = %s', (add_user_form.role.data,)).fetchone()
            role_id_add_user = role_id_add_user[0] # теперь это число, а не кортеж
            cur.execute('INSERT INTO part_in_project (user_id, role_name, project_id, role_id) '
                        'VALUES (%s, %s, %s, %s)', (add_user_id, add_user_form.role.data, project_id, role_id_add_user))
            flash (message=f'Пользователь {add_user_form.login.data} добавлен в проект', category='success')
            return redirect(url_for('check_user_project', project_id=project_id))

    return render_template('add_user_to_project.html', project_id=project_id, form=add_user_form)

@app.route('/project/<int:project_id>/del_user', methods=['GET', 'POST'])
@login_required
def del_user_from_project(project_id):

    user_id = current_user.user_id # айди того, кто осуществляет удаление из проекта
    with get_db_connection() as con:
        cur = con.cursor()
        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id,)).fetchone()
    if (role_user is None) or (role_user[0] != 'владелец'):  # удалять пользователей могут только юзеры с правами владельца
        # при этом создателя проекта удалить никто не сможет, проверка будет ниже
        flash(message='У Вас недостаточно прав для этого действия', category='danger')
        return redirect(url_for('check_user_project', project_id=project_id))

    del_user_form = DeleteUserFromProjectForm()

    if del_user_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()

            # достаём айдишник удаляемого пользователя, чтобы удалить его из бд
            user_id_del = cur.execute('SELECT user_id FROM users WHERE login = %s', (del_user_form.login.data, )).fetchone()
            if user_id_del is None:
                flash(message='Пользователя с таким логином не существует', category='danger')
                return render_template('del_user_from_project.html', project_id=project_id, form=del_user_form)

            user_id_del = user_id_del[0]

            # проверяем, есть ли такой юзер в проекте (если нет, то удалять некого)
            check_user = cur.execute('SELECT user_id FROM part_in_project WHERE project_id = %s '
                                         'AND user_id = %s', (project_id, user_id_del, )).fetchone()
            if check_user is None:
                flash(message=f'Пользователь {del_user_form.login.data} не состоит в проекте', category='warning')
                return redirect(url_for('check_user_project', project_id=project_id))

            # проверяем, не создателя ли хотят удалить из проекта (это недопустимо)
            check_user_creator_id = cur.execute('SELECT creator_project_id FROM project WHERE project_id = %s', (project_id, )).fetchone()
            if check_user_creator_id == user_id_del:
                flash(message='Создателя проекта удалить нельзя!', category='danger')
                return redirect(url_for('check_user_project', project_id=project_id))

            # проверяем, что пользователь не хочет удалить сам себя (владелец) - для этого есть кнопка выхода из проекта
            if user_id == user_id_del:
                flash(message='Вы не можете удалить себя из проекта. Воспользуйтесь кнопкой на странице просмотра проекта', category='warning')
                return redirect(url_for('check_user_project', project_id=project_id))

            # сначала удаляем все СВОИ задачи юзера (задачи для себя) в ДАННОМ проекте
            cur.execute('DELETE FROM task WHERE creator_id = %s AND creator_id = executor_id '
                        'AND project_id = %s', (user_id_del, project_id, ))
            # затем удаляем его самого из проекта
            cur.execute('DELETE FROM part_in_project WHERE user_id = %s', (user_id_del,))
            flash (message=f'Пользователь {{del_user_form.login.data}} удалён из проекта.', category='success')
            return redirect(url_for('check_user_project', project_id=project_id))

    return render_template('del_user_from_project.html', project_id=project_id, form=del_user_form)


@app.route('/project/<int:project_id>/out', methods=['GET', 'POST'])
@login_required
def out_of_project(project_id):
    user_id = current_user.user_id

    out_of_project_form = OutOfProjectForm()
    if out_of_project_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()
            # при выходе из проекта тоже удаляем все созданные пользователем задачи (в них он исполнитель)
            cur.execute('DELETE FROM task WHERE creator_id = %s AND creator_id = executor_id '
                        'AND project_id = %s', (user_id, project_id, ))
            # затем удаляем его самого из проекта
            cur.execute('DELETE FROM part_in_project WHERE user_id = %s', (user_id,))
            flash(message=f'Пользователь {{del_user_form.login.data}} удалён из проекта.', category='success')
            return redirect(url_for('check_user_project', project_id=project_id))
    return render_template('out_of_project.html', project_id=project_id, form=out_of_project_form)

@app.route('/project/<int:project_id>/members_of_project', methods=['GET'])
@login_required
def members_of_project(project_id):
    with get_db_connection() as con:
        cur = con.cursor()
        project_name = cur.execute('SELECT name FROM project WHERE project_id = %s', (project_id, )).fetchone()

        members_of_project = cur.execute('SELECT u.login, pp.role_name, pp.date_add_to_project, u.email_adress '
                                         'FROM users as u JOIN part_in_project as pp ON pp.user_id = u.user_id '
                                         'WHERE pp.project_id = %s', (project_id,)).fetchall()
        numbers = [i for i in range(len(members_of_project))] # чтобы вывести номера рядом со строками
        return render_template('members_of_project.html', members_of_project=members_of_project,
                               project_id=project_id, project_name=project_name, numbers=numbers)


@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id): # редактировать задачу (удалить, переименовать, переназначить исполнителя,
    # изменить приоритет, переназначить дедлайн, изменить статус, изменить описание задачи - что нужно сделать)

    user_id = current_user.user_id
    with get_db_connection() as con:
        cur = con.cursor()
        # получаю айди проекта, чтобы определить роль юзера в этом проекте
        project_id = cur.execute('SELECT project_id FROM task WHERE task_id = %s', (task_id,)).fetchone()
        project_id = project_id[0]

        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id,)).fetchone()
        creator_user_id = cur.execute('SELECT creator_id FROM task WHERE task_id = %s', (task_id,)).fetchone()
        # редактировать задачу могут только владельцы и создатель задачи (но он может быть участником в проекте)
        if (role_user is None) or (role_user[0] == 'участник' and creator_user_id != user_id):
            flash(message='У Вас недостаточно прав для этого действия', category='danger')
            return redirect(url_for('check_user_project', project_id=project_id))

        role_user = role_user[0]  # вытаскиваю из кортежа
        # нужно сравнить её с ролью "владелец" в html шаблоне, чтобы отрисовать или скрыть поле с логином исполнителя
        # так как участник не должен иметь возможность путём эдита СВОЕЙ задачи менять исполнителя
        role_owner = 'владелец'

    with get_db_connection() as con:
        cur = con.cursor()

        task_data = cur.execute('SELECT name, deadline, priority, status, description, executor_id FROM task '
                                   'WHERE task_id = %s', (task_id,)).fetchone()
        # получаю логин исполнителя, чтобы В ФОРМЕ отобразить, кто исполняет задачу (как при просмотре задачи)
        executor_login = cur.execute('SELECT u.login FROM users as u JOIN task as t ON t.executor_id = u.user_id WHERE task_id = %s', (task_id, )).fetchone()

        all_status = cur.execute('SELECT name, name FROM status').fetchall() # получаем статусы, чтобы отобразить
                                                                   # их в выпадающем списке
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


            if (new_exec_id is None) or (edit_task_form.deadline.data < datetime.datetime.now()):
                if new_exec_id is None:
                    flash(message='Пользователя с таким логином не существует', category='danger')
                    return render_template('edit_task.html', form=edit_task_form)
                if edit_task_form.deadline.data < datetime.datetime.now():
                    flash(message='Дедлайн не может быть прошедшей датой', category='danger')
                    return render_template('edit_task.html', form=edit_task_form)

            cur.execute(
                'UPDATE task SET name = %s, deadline = %s, executor_id = %s, priority = %s, status = %s, description = %s WHERE task_id = %s',
                (edit_task_form.name.data, edit_task_form.deadline.data, new_exec_id,
                 edit_task_form.priority.data, edit_task_form.status.data, edit_task_form.description.data,
                 task_id))

            # тут же создадим запись о новом изменении (нужно определить категорию изменения исходя из ОБНОВЛЁННЫХ ПОЛЕЙ
            # и записать логин, айди автора изменения, тип изменения, таск айди, текущую дату и время и айди типа изменения
            # при этом надо выводить ПОСЛЕДНЕЕ ИЗМЕНЕНИЕ ДЛЯ ПРОСМОТРА в задаче - сортирую по дате и вывожу первую
            # - то есть самое позднее изменение

            #'SELECT name, deadline, priority, status, description, executor_id
            result_change_type = ''
            executor_login = executor_login[0] # вытаскиваем логин из кортежа

            change_types = cur.execute('SELECT change_name FROM change_type').fetchall()
            change_types = [row[0] for row in change_types]

            if task_data[0] != edit_task_form.name.data:
                result_change_type = change_types[6]
            if task_data[1] != edit_task_form.deadline.data:
                result_change_type = change_types[3]
            if str(task_data[2]) != edit_task_form.priority.data: # из бд приоритет = int, а из формы = всё строки
                result_change_type = change_types[5]
            if task_data[3] != edit_task_form.status.data:
                result_change_type = change_types[1]
            if task_data[4] != edit_task_form.description.data:
                result_change_type = change_types[2]
            if executor_login != edit_task_form.executor_login.data:
                result_change_type = change_types[4]

            change_author_login = cur.execute('SELECT login FROM users WHERE user_id = %s', (user_id, )).fetchone()
            change_author_login = change_author_login[0] # достаю логин из кортежа

            change_type_id = cur.execute('SELECT type_id FROM change_type WHERE change_name = %s', (result_change_type,)).fetchone()
            change_type_id = change_type_id[0]

            cur.execute('INSERT INTO change (change_author, user_author_id, type, task_id, change_type_id) VALUES (%s, %s, %s, %s, %s)',
                        (change_author_login, user_id, result_change_type, task_id, change_type_id, ))

            flash('Данные успешно обновлены', category='success')
            return redirect(url_for('check_task', task_id=task_id))
            # на этом функция прекращает свою работу

    return render_template('edit_task.html', form=edit_task_form,
                           role_user=role_user, role_owner=role_owner)

@app.route('/tasks/<int:task_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):

    user_id = current_user.user_id  # получаю айдишник текущего юзера
    with get_db_connection() as con:
        cur = con.cursor()
        # получаю айди проекта, чтобы определить роль юзера в этом проекте
        project_id = cur.execute('SELECT project_id FROM task WHERE task_id = %s', (task_id,)).fetchone()
        project_id = project_id[0]

        role_user = cur.execute('SELECT role_name FROM part_in_project WHERE project_id = %s AND user_id = %s',
                                (project_id, user_id,)).fetchone()
        creator_user_id = cur.execute('SELECT creator_id FROM task WHERE task_id = %s', (task_id,)).fetchone()
        # удалить задачу могут только юзеры с правами владельца, а также создатель задачи (но участник проекта, например)
        if (role_user is None) or (role_user[0] == 'участник' and creator_user_id != user_id):
            flash(message='У Вас недостаточно прав для этого действия', category='danger')
            return redirect(url_for('check_user_project', project_id=project_id))

    delete_task_form = DeleteTaskForm()
    if delete_task_form.validate_on_submit():
        with get_db_connection() as con:
            cur = con.cursor()
            # узнаю айди проекта из которого удаляется задача, чтобы по нему вернуться в проект
            project_id = cur.execute('SELECT project_id FROM task WHERE task_id = %s', (task_id,)).fetchone()
            project_id = project_id[0] # вытаскиваю айдишник из кортежа запроса

            cur.execute('DELETE FROM task WHERE task_id = %s', (task_id,))
            flash(message='Задача удалена. Вы перенаправлены на страницу проекта', category='success')
            return redirect(url_for('check_user_project', project_id=project_id))

    return render_template('delete_task.html', form=delete_task_form, task_id=task_id)
