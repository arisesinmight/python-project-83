import os

import psycopg2

from dotenv import load_dotenv

from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

import validators

from urllib.parse import urlparse

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    message = get_flashed_messages()
    input_data = request.args.get('url', '')
    return render_template('index.html',
                           input_data=input_data,
                           message=message)


@app.post('/urls')
def url_post():
    input_data = request.form.to_dict()
    if validators.url(input_data['url']) is not True:
        message = 'Некорректный URL'
        return render_template(
            'index.html',
            input_data=input_data,
            message=message
            ), 422
    #номализуем урл
    #подключаемся к базе
    #сохраняем урл в базе
    #id = находим айди
    flash('Страница успешно добавлена')
    return redirect(url_for('show_url', id=id), code=302)


@app.route('/urls')
def urls_get():
    return render_template(
        'urls.html'
    )


@app.route('/urls/1') #айди 1 так как нет пока модели
def show_url(id):
    #подключаемся к базе
    user = '' #находим пользователя по айди
    return render_template(
        'show.html',
        user=user
    )
