from flask import Flask, jsonify, render_template, flash, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from models import AccessLog,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nazarnhb3334@localhost:5432/nuker'
db.init_app(app)

logs = [
    {'ip': '127.0.0.1', 'start_date': '2022-01-01 00:00:00', 'end_date': '2022-01-01 00:01:00', 'query': 'login'},
    {'ip': '127.0.0.1', 'start_date': '2022-01-01 00:05:00', 'end_date': '2022-01-01 00:06:00', 'query': 'logout'},
    {'ip': '127.0.0.2', 'start_date': '2022-01-01 00:10:00', 'end_date': '2022-01-01 00:11:00', 'query': 'login'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Получить данные из формы на странице регистрации
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        # Проверка на корректность данных (например, совпадение паролей)
        if not (username and password and confirm) or password != confirm:
            flash('Ошибка! Проверьте введенные данные.')
        else:
            # Обработка успешной регистрации
            flash('Регистрация прошла успешно!')
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logs')
def show_logs():

    sort_key = request.args.get('sort')
    if sort_key == 'ip':
        logs_sorted = sorted(logs, key=lambda log: log['ip'])
    elif sort_key == 'start_date':
        logs_sorted = sorted(logs, key=lambda log: log['start_date'])
    elif sort_key == 'end_date':
        logs_sorted = sorted(logs, key=lambda log: log['end_date'])
    elif sort_key == 'query':
        logs_sorted = sorted(logs, key=lambda log: log['query'])
    else:
        logs_sorted = logs
    return render_template('logs.html', logs=logs_sorted)


if __name__ == '__main__':
    with app.app_context:   
        db.create_all()
    app.run(debug=True)
