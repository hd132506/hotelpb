from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
    team = {'name': 'PB'}
    return render_template('index.html', title='Home', team=team)
