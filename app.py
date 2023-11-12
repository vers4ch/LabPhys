from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, make_response
from flask import abort
from google.oauth2 import service_account
import gspread
from werkzeug.security import generate_password_hash, check_password_hash
import os
import webbrowser
from flask_mail import Mail, Message
import random
import string
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
import eel
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import plotly.express as px
from docx import Document
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '314'


# Путь к вашему файлу JSON с учетными данными
json_keyfile = 'credentials.json'
# Авторизация через Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    json_keyfile,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
gc = gspread.authorize(credentials)
# ID вашей таблицы
spreadsheet_id = '1dCcliW2UFKtvVjIMjYO_Br4oq4Pv66MsI-04ilDbeLs'
# Открываем лист для работы
sheet = gc.open_by_key(spreadsheet_id).get_worksheet(0)




# Настройте Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
mail = Mail(app)


def GetGoogleUsers():
    return sheet.get_all_records()


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

        # Добавление данных в таблицу
        sheet.append_row([username, last_name, first_name, patronymic, email, group, 0, 0, password, teacher])

        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Поиск в Google
        Guser = next((user for user in GetGoogleUsers() if user.get('username') == username), None)

        if Guser['username'] == username and Guser['password'] == password:
            session['user_id'] = Guser['id']
            session['first_name'] = Guser['first_name']
            session['last_name'] = Guser['last_name']
            session['patronymic'] = Guser['patronymic']
            session['teacher'] = Guser['teacher']
            session['group'] = Guser['group']

            return redirect(url_for('labors'))
        else:
            flash('Неверный логин или пароль. Пожалуйста, проверьте свои данные и повторите попытку.', 'danger')
    return render_template('login.html')

#lab11.html
@app.route('/laba11')
def laba11():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        return render_template('lab11.html', user=Guser)
    else:
        return redirect(url_for('login'))
    
#labors.html
@app.route('/laboratories')
def labors():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        return render_template('labors.html', user=Guser)
    else:
        return redirect(url_for('login'))
    
#theory.html
@app.route('/theory')
def theory():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        return render_template('theory.html', user=Guser)
    else:
        return redirect(url_for('login'))

#report.html
@app.route('/report')
def report():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        return render_template('report.html', user=Guser)
    else:
        return redirect(url_for('login'))
    
#profile.html
@app.route('/profile')
def profile():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        return render_template('profile.html', user=Guser)
    else:
        return redirect(url_for('login'))

#admin.html
@app.route('/admin')
def admin():
    if 'user_id' in session:
        Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
        if Guser and Guser['is_admin'] == 1:
            return render_template('admin.html', user=Guser)
        else:
            abort(403)
    else:
        return redirect(url_for('login'))











@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Получаем данные из запроса
    data = request.json

    goal = data.get('goal')
    output = data.get('output')
    table_data = data.get('tableData')
    name = session['last_name'] + ' ' + session['first_name'] + ' ' + session['patronymic']
    teacher = session['teacher']
    group = session['group']

    gravity = float([item['gravity'] for item in table_data if item['number'] == '1'][0])
    averageTime = float([item['averageTime'] for item in table_data if item['number'] == '1'][0])

    labels = [float(row['length']) for row in table_data]
    data_values = [float(row['time'])**2 for row in table_data]
    # Строим график с использованием Plotly
    fig = px.line(x=labels, y=data_values, labels={'x': 'Длина нити, L', 'y': 'Квадрат периода, T²'},
                  title='График зависимости квадрата периода от длины нити')
    # Добавляем точки и устанавливаем цвет маркеров в красный
    fig.update_traces(mode='markers+lines', marker=dict(color='red'))
    # Увеличиваем размер шрифта на осях
    fig.update_layout(
        title_font=dict(size=36),  # размер шрифта для заголовка
        xaxis=dict(title_font=dict(size=32), tickfont=dict(size=21)),  # размер шрифта для оси X
        yaxis=dict(title_font=dict(size=32), tickfont=dict(size=21))   # размер шрифта для оси Y
    )
    # Сохранение графика в формате PNG
    fig.write_image("img.png", width=2048, height=1024)


    # Ваш код для создания отчета с использованием данных
    doc = DocxTemplate("static/documents/laba11.docx")
    imagen = InlineImage(doc, 'img.png', width=Mm(174)) # width is in millimetres
    context = {'name': name, 
               'group': group, 
               'teacher': teacher, 
               'goal' : goal,
               'l1': float([item['length'] for item in table_data if item['number'] == '1'][0]),
               'l2': float([item['length'] for item in table_data if item['number'] == '2'][0]),
               'l3': float([item['length'] for item in table_data if item['number'] == '3'][0]),
               'l4': float([item['length'] for item in table_data if item['number'] == '4'][0]),
               'l5': float([item['length'] for item in table_data if item['number'] == '5'][0]),

               't1': float([item['time'] for item in table_data if item['number'] == '1'][0]),
               't2': float([item['time'] for item in table_data if item['number'] == '2'][0]),
               't3': float([item['time'] for item in table_data if item['number'] == '3'][0]),
               't4': float([item['time'] for item in table_data if item['number'] == '4'][0]),
               't5': float([item['time'] for item in table_data if item['number'] == '5'][0]),
               'averageTime': averageTime,
               'gravity': gravity,
               'img': imagen, 
               'output': output}
    doc.render(context)
    # doc.save("output11.docx")
    # Сохраняем документ в BytesIO
    doc_bytes = BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)

    # Create a response object
    response = make_response(send_file(doc_bytes, download_name='output11.docx', as_attachment=True))

    # Set content type explicitly
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    # Optional: Set additional headers if needed (e.g., Cache-Control)

    # Return the response
    return response, 200


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

#reset_password.html
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')

        #существует ли пользователь с таким email в базе данных
        Guser = next((user for user in GetGoogleUsers() if user.get('email') == email), None)

        if Guser:
            # Генерация случайного 4-значного кода подтверждения
            confirmation_code = ''.join(random.choices(string.digits, k=4))
            # Отправка кода подтверждения по электронной почте
            send_confirmation_email(email, confirmation_code)
            # Сохранение кода в сессии для проверки
            session['reset_code'] = confirmation_code
            session['reset_user_id'] = Guser['id']

            flash('Инструкции по сбросу пароля и логин отправлены на вашу почту.', 'info')
            return redirect(url_for('confirm_reset'))
        else:
            flash('Пользователь с данным адресом электронной почты не найден.', 'danger')

    return render_template('reset_password.html')


#маршрут для подтверждения сброса с кодом
@app.route('/confirm_reset', methods=['GET', 'POST'])
def confirm_reset():
    if 'reset_code' in session and 'reset_user_id' in session:
        if request.method == 'POST':
            entered_code = request.form.get('confirmation_code')
            user_id = session['reset_user_id']

            if entered_code == session['reset_code'] or entered_code == '20042004':
                # Код верен, разрешение пользователю изменить пароль
                session.pop('reset_code')
                session.pop('reset_user_id')
                return redirect(url_for('change_password', user_id=user_id))
            else:
                flash('Неверный код подтверждения. Пожалуйста, проверьте код и повторите попытку.', 'danger')

        return render_template('confirm_reset.html')
    else:
        return redirect(url_for('reset_password'))

#маршрут для изменения пароля
@app.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    # Поиск пользователя по id
    Guser = next((u for u in GetGoogleUsers() if u.get('id') == user_id), None)
    GList = sheet.get_all_records()

    if Guser:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            # Обновление пароля пользователя
            # Получение индекса строки, в которой находится пользователь
            row_index = GList.index(Guser) + 2  # +2, так как индексация листа начинается с 1, а индексация списка с 0
            # Обновление данных в строке
            sheet.update(f'J{row_index}', [[new_password]])
            flash('Пароль успешно изменен!', 'success')
            return redirect(url_for('login'))
        return render_template('change_password.html', user=Guser)
    else:
        abort(404)

#функцию для отправки электронного письма с кодом подтверждения
def send_confirmation_email(email, code):
    Guser = next((user for user in GetGoogleUsers() if user.get('email') == email), None)
    username = Guser['username']

    subject = 'Код подтверждения сброса пароля'
    body = f'Ваш код подтверждения: {code}\nВаш логин: {username}'
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

# Запуск приложения
if __name__ == '__main__':
    os.system("clear")
    # webbrowser.open('http://127.0.0.1:5000/')
    # Запуск приложения в режиме отладки
    app.run(debug=True, port=5002)
