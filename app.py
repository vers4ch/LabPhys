from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import plotly.express as px
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import os
import numpy as np
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '314'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(120), unique=False, nullable=True)
    group = db.Column(db.String(120), unique=False, nullable=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    patronymic = db.Column(db.String(120), unique=True, nullable=False)
    teacher = db.Column(db.String(120), unique=True, nullable=False)


def create_tables():
    db.create_all()


# Запуск create_tables() перед каждым запросом
@app.before_request
def before_request():
    with app.app_context():
        create_tables()

#register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        email = request.form['email']
        group = request.form['group']

        last_name = request.form['last_name']
        first_name = request.form['first_name']
        patronymic = request.form['patronymic']

        teacher = request.form['teacher']

        #security

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # new_user = User(username=username, password=hashed_password)

        # new_user = User(username=username, password=password)
        new_user = User(username=username, password=password, email=email, group=group, last_name = last_name, first_name = first_name, patronymic = patronymic, teacher=teacher)

        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # if user and check_password_hash(user.password, password):
        if user and user.password == password:
            session['user_id'] = user.id
            # flash('Вы уже авторизированны!', 'success')
            return redirect(url_for('laba11'))
        else:
            flash('Неверный логин или пароль. Пожалуйста, проверьте свои данные и повторите попытку.', 'danger')
    return render_template('login.html')

#lab11.html
@app.route('/laba11')
def laba11():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('lab11.html', user=user)
    else:
        return redirect(url_for('login'))
    
#labors.html
@app.route('/laboratories')
def labors():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('labors.html', user=user)
    else:
        return redirect(url_for('login'))
    
#theory.html
@app.route('/theory')
def theory():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('theory.html', user=user)
    else:
        return redirect(url_for('login'))

#report.html
@app.route('/report')
def report():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('report.html', user=user)
    else:
        return redirect(url_for('login'))
    
#profile.html
@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

#admin.html
@app.route('/admin')
def admin():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()

        # Check if the user is an admin (is_admin == 1)
        if user and user.is_admin == 1:
            return render_template('admin.html', user=user)
        else:
            # If the user is not an admin, you can redirect them to another page or display an error
            abort(403)  # HTTP status code 403 indicates forbidden access
    else:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))  # Перенаправление на главную страницу (или другую страницу)

#reset_password.html
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Проверьте, существует ли пользователь с таким email в вашей базе данных
        user = User.query.filter_by(email=email).first()

        if user:
            # Здесь может быть логика отправки email с инструкциями по сбросу пароля
            flash('Инструкции по сбросу пароля отправлены на вашу почту.', 'info')
        else:
            flash('Пользователь с данным адресом электронной почты не найден.', 'danger')

    return render_template('reset_password.html')




# Определение маршрута для главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    # Отображение шаблона index.html
    return render_template('login.html')

# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    webbrowser.open('http://127.0.0.1:5000')
    # Запуск приложения в режиме отладки
    app.run(debug=True)
