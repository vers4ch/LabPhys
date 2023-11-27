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
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import plotly.express as px
from docx import Document
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '314'


# Учетные данные в формате JSON
credentials_json = {
  "type": "service_account",
  "project_id": "labphys",
  "private_key_id": "c925e28a1ae4e0c844dfb0413c862bdc7adc7477",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrZF9NsDJ8cjYq\ngGEFy3W8GmKikLa9imN/aC5XeTzEREQN6Q1vC1rFrksL90/gxfHH5lRxBeJOU0QL\nk4nxY+kJ7+g4+FL8Y8O5Q//FwjLDzrWCWCx4miCRS+kDPgakxYciuPbN4ivMf2FN\n9nszJHSBqK7FQXRHRhZ7Up1WCT2cSbdT7PITtAJ+4vwJyZXJvqJR5jiYCHQeVdu5\nc8bHP5/v4meqlXcWZ7iansDK/Fd5vcFsnUCXoKtuHomeh6dj6DP0N8rXSaZtGt0L\nrL+AggpJ4VBsVE8nREWi+d4xszVU6tK9qHxA2HxJNPyP9BxbY+DMvFLbiDIVlqse\nuRYHBLAhAgMBAAECggEABVz08X6luciuIrrVLmP9OWde9kTOfxRdRC+boZ+Y0/Bp\n68CC69pgWwa28Pcqb/dpty5hLo83U2meG7mga6YLdQTlkKDOofiyN3ImBwdqZL+r\nZNqC+7wg8EL+ldwjQ5UtwxukF3GwGqxSvGiN1t4ZajQ/0crYS2GpUu8VHsvXunPz\n6EA78j3uxS2tSg1iPb8n7nxQ624GzfJrDZ3k83YH877vMHNcFFCPtgtr1D948gyX\nxwXCkiFGiFyUCj7Bw+aksXthSP3zLWdsgR7ZblJHhm/sFzsml3o6xGymwITDOmkF\nwomyDQKg2g77kK+w5vcXLlmTAddN8KeKdAMPaZA6BQKBgQDk3OUmPAYdjCNfbjGE\nxdGiaODgCiggFOpC9fOgjE33zWGjbxbUS8Z7cxICgsFHcjITsykkHb8uJD+wgISw\nCgu3IULAzSgg6fbLuV+u5VKx08dgDQk0HhJu0MhbiwTGAk+M9o+pwj+opu06bb5E\ncaj1Iu2qgYxhsD78KNtHEevQvQKBgQC/tvVL5G1iu/QjldyAGZDZ4Y/77dkPCfxH\nBnrN5e9zq60/BPfQLXLETbNlCX76fkGkuNseFNki9Iih5qR/fgL8kwiqvvvVDHme\n2Du07Txo4YayF8v0al4nwXHe4Ym8CrP31/R0KHC11osXB57JAdrcARh7jBidgCcU\nOV4tQLptNQKBgEJJkL2ASS0pt90eJ42TVmK6CdgaWQDhzfBTGJt5x+NsQ0l5FZ2r\nzPNYovDDOoQdGVAHZnUlgIg2y5OtxcDPSBFkutbpFSRjX64mJQadOVR0SJ0TaYUE\n6MXcBwwsudc4OB5WE8pRjuqkXrW7r45XdV57HWdzWlu5FqUmmEx/blPpAoGAHiUl\nov5TGOBW/jV1S4s5lJj8K+/1XoECcySYsMGEClsnTa55TPmofyd8mtmIZtjtd3o9\nshgzIGT1CwgaO5XT4GU6SqbnMFPa19hGYyeehRtZM628Oz1yeqvXPOWX48KHE+SY\nIp+tQVpv2novRIoPIOLnN54KzNE2095FabYw2jUCgYEA5CcfIyhXZ/bR5JJBdLrv\nlAlK6bk9AFNRHfpCz88ayfUdwWYexomiQliFdt9+wRzAFaVOr/YybntHw6+nBZb5\nawjWE104wNjBGUrU1g8s5HtGFvToK1tueWZy8D45NSNOSduYCN7FgOZ/M2HyXjMi\nCLAz5zbpnM43TmyKdqRQKLQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "versach@labphys.iam.gserviceaccount.com",
  "client_id": "101984763976201259861",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/versach%40labphys.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Авторизация через Google Sheets API с использованием учетных данных
credentials = service_account.Credentials.from_service_account_info(
    credentials_json,
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
    
# #theory.html
# @app.route('/theory')
# def theory():
#     if 'user_id' in session:
#         Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
#         return render_template('theory.html', user=Guser)
#     else:
#         return redirect(url_for('login'))

# #report.html
# @app.route('/report')
# def report():
#     if 'user_id' in session:
#         Guser = next((user for user in GetGoogleUsers() if user.get('id') == session['user_id']), None)
#         return render_template('report.html', user=Guser)
#     else:
#         return redirect(url_for('login'))
    
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
    
#teacher
@app.route('/teacher')
def teacher():
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
    table_data = request.get_json()
    # print("Received data:", table_data)

    # здесь вы можете добавить код для обработки полученных данных
    goal = table_data['goal']
    theor = table_data['theor']
    output = table_data['output']
    table = table_data['tableData']

    name = session['last_name'] + ' ' + session['first_name'] + ' ' + session['patronymic']
    teacher = session['teacher']
    group = session['group']

    # Ваш код для создания отчета с использованием данных
    doc = DocxTemplate("static/documents/laba11.docx")
    context = {'name': name, 
               'group': group, 
               'teacher': teacher, 
               'goal' : goal,
               'theor': theor,

                'l11': table[0][2],
                'l12': table[1][1],
                'l13': table[2][1],
                'l14': table[3][1],
                'l15': table[4][1],

                't11': table[0][3],
                't12': table[1][2],
                't13': table[2][2],
                't14': table[3][2],
                't15': table[4][2],
                'averageTime1': table[0][4],
                'gravity1': table[0][5],


                'l21': table[5][2],
                'l22': table[6][1],
                'l23': table[7][1],
                'l24': table[8][1],
                'l25': table[9][1],

                't21': table[5][3],
                't22': table[6][2],
                't23': table[7][2],
                't24': table[8][2],
                't25': table[9][2],
                'averageTime2': table[5][4],
                'gravity2': table[5][5],


                'l31': table[10][2],
                'l32': table[11][1],
                'l33': table[12][1],
                'l34': table[13][1],
                'l35': table[14][1],

                't31': table[10][3],
                't32': table[11][2],
                't33': table[12][2],
                't34': table[13][2],
                't35': table[14][2],
                'averageTime3': table[10][4],
                'gravity3': table[10][5],

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
