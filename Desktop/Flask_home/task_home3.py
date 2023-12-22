# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email",
# "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных,
# а пароль должен быть зашифрован.

import os
from hashlib import pbkdf2_hmac
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm

class SingUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
csrf = CSRFProtect(app)

EXAMPLE_DB = {}

def hash_password(password: str) -> bytes:
    salt = os.urandom(32)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    hashed_password = salt + key
    return hashed_password

def check_password(password: str, hashed_password: bytes) -> bool:
    stored_salt, stored_key = hashed_password[:32], hashed_password[32:]
    new_key = pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100_000)
    return new_key == stored_key

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SingUpForm()
    form_notifications = []
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data
        EXAMPLE_DB[name] = {
            field.name: field.data
            for field in form
            if field.name not in ('name', 'password')
        }
        hashed_password = hash_password(password)
        # print(f'{password = }')
        # print(f'{hashed_password = }')
        # print(f'{check_password(password, hashed_password) = }')
        EXAMPLE_DB[name]['password'] = hashed_password
        form_notifications.append('User registered, password hashed!')

    return render_template('4.html', form=form, form_notifications=form_notifications,)

if __name__ == '__main__':
    app.run(debug=True)