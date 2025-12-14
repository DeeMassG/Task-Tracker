from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, DateField, IntegerField, PasswordField, SubmitField, TextAreaField, validators
from wtforms.fields.choices import SelectField


class RegistrationForm(FlaskForm):
    surname = StringField('Фамилия', [validators.Length(max=30), validators.InputRequired(message='Введите фамилию')])
    name = StringField('Имя', [validators.Length(max=20), validators.InputRequired(message='Введите имя')])
    last_name = StringField('Отчество', [validators.Length(max=30)])
    login = StringField('Логин',[validators.InputRequired(message='Введите логин'), validators.Length(max=30)])

    password = PasswordField('Пароль', [validators.InputRequired(message='Введите пароль'), validators.Length(min=6, max=15, message='Пароль должен содержать не менее 6 и не более 15 символов'),
                                        validators.EqualTo('confirm', message='Пароли должны совпадать!'), ])

    confirm  = PasswordField('Подтверждение пароля', [validators.InputRequired(message='Повторите пароль для подтверждения'), validators.EqualTo('password', message='Пароли должны совпадать!')])
    birthday = DateField('Дата рождения', format='%Y-%m-%d', validators = [validators.InputRequired(message='Введите дату рождения')])

    email_adress = StringField('E-mail', [validators.Length(min=6, max=100),
                                   validators.Email(message='Почта введена некорректно, повторите ввод'), validators.InputRequired(message='Введите E-mail')])

    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    login = StringField('Логин', [validators.InputRequired(message='Это поле обязательно для ввода')])
    password = PasswordField('Пароль', [validators.InputRequired(message='Это поле обязательно для ввода')])
    submit = SubmitField('Войти')

class EditProfileForm(FlaskForm):
    surname = StringField('Фамилия', [validators.Length(max=30)])
    name = StringField('Имя', [validators.Length(max=20)])
    last_name = StringField('Отчество', [validators.Length(max=30)])
    login = StringField('Логин', [validators.InputRequired(message='Введите логин'), validators.Length(max=30)])
    birthday = DateField('Дата рождения', format='%Y-%m-%d',
                         validators=[validators.InputRequired(message='Введите дату рождения')])

    email_adress = StringField('E-mail', [validators.Length(min=6, max=100),
                                          validators.Email(message='Почта введена некорректно, повторите ввод'),
                                          validators.InputRequired(message='Введите E-mail')])
    submit = SubmitField('Подтвердить изменения')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Введите текущий пароль', [validators.InputRequired('Это поле обязательно для ввода')])
    new_password = PasswordField('Введите новый пароль', [validators.Length(min=6, max=15, message='Пароль должен содержать не менее 6 и не более 15 символов'),
                                        validators.EqualTo('confirm', message='Пароли должны совпадать!')])
    confirm = PasswordField('Подтверждение пароля',
                            [validators.InputRequired(message='Повторите пароль для подтверждения'),
                             validators.EqualTo('password', message='Пароли должны совпадать!')])
    submit = SubmitField('Изменить пароль')

class CreateNewProjectForm(FlaskForm):
    name = StringField('Введите название проекта', [validators.Length(max=50),
                                                    validators.InputRequired(message='Введите название проекта')])
    description = TextAreaField('Описание', validators=[validators.Length(max=2000, message='Максимум 2000 символов')])
    submit = SubmitField('Создать')

class EditProjectForm(FlaskForm):
    name = StringField('Введите новое название проекта', [validators.Length(max=50),
                                                    validators.InputRequired(message='Введите название проекта')])
    description = TextAreaField('Изменение описания', validators=[validators.Length(max=2000, message='Максимум 2000 символов')])
    submit = SubmitField('Подтвердить изменения')

class AddUserToProjectForm(FlaskForm): # добавление нового участника в проект (он тоже владелец проекта)
    login = StringField('Введите логин пользователя, которого хотите добавить в проект',
                        [validators.Length(max=30), validators.InputRequired(message='Данные не введены, повторите')])
    submit = SubmitField('Добавить пользователя')

class DeleteUserFromProjectForm(FlaskForm):
    login = StringField('Введите логин пользователя, которого хотите удалить из проекта',
                        [validators.Length(max=30), validators.InputRequired(message='Данные не введены, повторите')])
    submit = SubmitField('Удалить пользователя')
# class DeleteProjectForm(FlaskForm):

class CreateTaskForm(FlaskForm):
    name = StringField('Введите название задачи', [validators.Length(max=50),
                                                    validators.InputRequired(message='Введите название проекта')])
    deadline = DateField('Введите дедлайн задачи', format='%Y-%m-%d') # validators = [validators.InputRequired(message='Введите дедлайн задачи')]
    executor_login = StringField('Введите логин исполнителя', [validators.Length(max=30)]) # исполнитель не обязателен для ввода
    # но должен быть у каждой задачи (по умолчанию сделать создателя)
    priority = SelectField('Выберите номер приоритета от 1 до 3 (высший - 1)') # необязателен при создании, можно потом изменить
    # статус задаю по умолчанию 'новая' - для созданной задачи, а затем можно будет выбрать из выпадающего списка
    description = TextAreaField('Введите описание задачи', [validators.Length(max=2000,message='Максимум 2000 символов'), validators.InputRequired(message='Описание задачи является обязательным полем для заполнения')])
    submit = SubmitField('Создать')

class EditTaskForm(FlaskForm):
    name = StringField('Введите новое название задачи', [validators.Length(max=50),
                                                    validators.InputRequired(message='Введите название проекта')])
    deadline = DateField('Введите дедлайн задачи',
                         format='%Y-%m-%d')  # validators = [validators.InputRequired(message='Введите дедлайн задачи')]
    executor_login = StringField('Введите логин нового исполнителя (если хотите переназначить)',
                              [validators.Length(max=30)])  # логин будет конвертирован в айдишник в самом роуте
    # но должен быть у каждой задачи (по умолчанию сделать создателя)
    priority = SelectField('Выберите номер приоритета от 1 до 3 (высший - 1)')  # необязателен при создании, можно потом изменить
    status = SelectField('Выберите статус задачи',[validators.InputRequired('У задачи должен быть статус')])
    description = TextAreaField('Введите описание задачи',
                                [validators.Length(max=2000, message='Максимум 2000 символов'),
                                 validators.InputRequired(
                                     message='Описание задачи является обязательным полем для заполнения')])
    submit = SubmitField('Подтвердить изменения')

class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Удалить задачу')

