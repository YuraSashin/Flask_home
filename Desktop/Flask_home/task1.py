from flask import Flask, render_template
# Напишите простое веб-приложение на Flask, 
# которое будет выводить на экран текст "Hello, World!".
app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello World!'


# Добавьте две дополнительные страницы в ваше веб-приложение:
#  страницу "about" и страницу "contact".
@app.route('/contact/')
def contact():
    return 'My contact'

@app.route('/about/')
def about():
    return 'My about'

# Написать функцию, которая будет принимать на вход два числа 
# и выводить на экран их сумму.
@app.route('/<int:num1>/<int:num2>/')
def summa(num1: int, num2: int):
    return f'{num1} + {num2} = {num1 + num2}'

# Написать функцию, которая будет принимать на вход строку и выводить на экран ее длину.
@app.route('/<text>/')
def len_str(text):
    return f'{len(text)}'

# Написать функцию, которая будет выводить на экран HTML страницу с заголовком 
# "Моя первая HTML страница" и абзацем "Привет, мир!".
# @app.route('/')
# def index():
#     return (f'<h1>"Моя первая HTML страница"</h1> <p>Привет, мир!</p>')


# @app.route('/')
# def index():
#     context = [{ 'name': 'Ivan', 'last_name': 'Smirnov', 'age': '24'},{ 'name': 'Igor', 'last_name': 'Ivanov', 'age': '31'}]
#     return render_template('table.html', context=context)

@app.route('/')
def index():
    context = [
    {'name': 'Иван',
    'last_name': 'Иванов',
    'age' : 24},
    {'name': 'Пётр',
    'last_name': 'Петров',
    'age' : 48},
    {'name': 'Сергей',
    'last_name': 'Сидоров',
    'age' : 30},
    {'name': 'Мария',
    'last_name': 'Серова',
    'age' : 27},
    ]

    return render_template('table.html' , context=context)

if __name__ == "__main__":
    app.run(debug=True)