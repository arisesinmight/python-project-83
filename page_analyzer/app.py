import os
from urllib.parse import urlparse

import validators
from dotenv import load_dotenv
from flask import (Flask, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)

from page_analyzer.urls_repository import UrlsRepository

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


repo = UrlsRepository(app.config['DATABASE_URL'])


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
        error = 'Некорректный URL'
        return render_template(
            'index.html',
            input_data=input_data,
            error=error
            ), 422
    parsed_url = urlparse(input_data['url'])
    norm_url = parsed_url._replace(
        path="", params="", query="", fragment=""
    ).geturl()
    url_id = repo.get_id(norm_url)
    if url_id:
        flash('Страница уже существует')
        return redirect(url_for('show_url', id=url_id[0]))
    else:
        repo.save(norm_url)
        flash('Страница успешно добавлена')
        url_id = repo.get_id(norm_url)
        return redirect(url_for('show_url', id=url_id[0]), code=302)


@app.route('/urls')
def urls_get():
    urls = repo.get_summary_data()
    return render_template(
        'urls.html',
        urls=urls
    )


@app.route('/urls/<int:id>')
def show_url(id):
    message = get_flashed_messages()
    url = repo.find_by(id)
    check_results = repo.get_check_results(url)
    return render_template(
        'show.html',
        url=url,
        check_results=check_results,
        message=message
    )


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = repo.find_by(id)
    if repo.check_status(url) is not True:
        message = 'Произошла ошибка при проверке'
        return render_template(
            'show.html',
            url=url,
            check_results={},
            message=message
        ), 422
    repo.make_check(url)
    flash('Страница успешно проверена')
    return redirect(url_for('show_url', id=id))
