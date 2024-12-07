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


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    message = get_flashed_messages()
    input_data = {'url': ''}
    return render_template('index.html',
                           input_data=input_data,
                           message=message)


@app.post('/')
def url_post():
    input_data = request.form.to_dict()
    if validators.url(input_data) is not True:
        flash('Некорректный URL')
        return render_template(
            'index.html',
            input_data=input_data), 422
    flash('Страница успешно добавлена')
    return redirect(url_for('show_url'), code=302)



@app.route('/urls/<id>')
def show_url():
    message = get_flashed_messages()
    return render_template(
        'show.html',
        message=message
    )


@app.route('/urls')
def urls_get():
    return render_template(
        'urls.html'
    )
