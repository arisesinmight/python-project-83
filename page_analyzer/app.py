import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, get_flashed_messages, flash


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def url_post():
    return render_template('urls.html')

