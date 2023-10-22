from flask import Flask, render_template, request
from flask import jsonify
import plotly.express as px
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import os
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '314'


# Определение формы для ввода параметров маятника
class PendulumForm(FlaskForm):
    # Поле для ввода длины маятника
    length = FloatField('Длина нити(м., max: 1м.)', validators=[InputRequired(), NumberRange(min=0.001, max=1.0)], default=0.555)

    # Поле для ввода начального угла отклонения
    theta0 = FloatField('Начальное отклонение(градусы)', validators=[InputRequired(), NumberRange(min=-35, max=35)], default=0)

    # Поле для выбора единиц измерения (градусы или радианы)
    units = SelectField('Units', choices=[('degrees', 'Degrees'), ('radians', 'Radians')], default='degrees')

    # Кнопка для обновления графика
    submit = SubmitField('submit')


def pendulum_motion(length, theta0, units='degrees', damping_factor=0.01):
    g=9.81
    dt = 0.001 #критически сильно влияет на производительность
    t = np.arange(0, 60, dt)

    omega_natural = np.sqrt(g / length)
    omega_damped = np.sqrt(omega_natural**2 - (damping_factor / (2 * length))**2)

    if damping_factor < 1:
        theta = theta0 * np.exp(-damping_factor / (2 * length) * t) * np.cos(omega_damped * t)
    else:
        raise ValueError("Damping factor must be less than 1 for a damped system.")

    if units == 'radians':
        theta = np.degrees(theta)

    return t, theta


def create_plot(length, theta0, units):
    t, theta = pendulum_motion(length, theta0, units)

    fig = px.line(x=t, y=theta, labels={'x': 'Время (сек.)', 'y': 'Отклонение'}, title=f'Отклонение от времни')

    # Преобразование градусов в строковый формат для использования в метках оси Y
    y_labels = [f"{deg}°" for deg in range(-90, 91, 10)]

    # Установка меток оси Y в градусах
    fig.update_layout(yaxis=dict(tickvals=list(range(-90, 91, 10)), ticktext=y_labels, tickformat=".3f"))

    # Установка фиксированного масштаба оси Y
    # fig.update_yaxes(range=[-90, 90])

    # Установка максимального значения оси X на .. секунды
    fig.update_xaxes(range=[0, 30])

    # # Установка шага делений и формата меток оси X
    # x_ticks = np.arange(0, 3.1, 0.0001)
    # fig.update_xaxes(tickvals=x_ticks, tickformat=".4f")

    # Преобразование графика в HTML для вставки в шаблон
    # plot_html = fig.to_html()
    # Преобразование графика в HTML для вставки в шаблон
    return fig.to_html()








# Определение маршрута для главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    # Создание экземпляра формы
    form = PendulumForm()
    # Переменная для хранения HTML-кода графика
    graph_html = None

    # Если форма отправлена (POST) и прошла валидацию
    if form.validate_on_submit():
        # Получение данных из формы
        length = form.length.data
        theta0 = form.theta0.data
        units = form.units.data

        # Создание HTML-кода графика
        graph_html = create_plot(length, theta0, units)

    # Отображение шаблона index.html с передачей формы и HTML-кода графика
    return render_template('index.html', form=form, graph_html=graph_html)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    receivedAngle = data.get('Angle0')
    receivedLength = data.get('Length')
    # print(receivedAngle, receivedLength)
    
    # Ваш код для обработки переменной
    
    return "Данные успешно получены на сервере."

# Запуск приложения
if __name__ == '__main__':
    # Создание директории для сохранения графиков
    if not os.path.exists('graph'):
        os.makedirs('graph')

    # Запуск приложения в режиме отладки
    app.run(debug=True)
