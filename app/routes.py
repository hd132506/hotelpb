from flask import render_template, flash, request, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Employee

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Welcome! DONGHotel')

@app.route('/reservelist')
def reserve_list():
    return render_template('reservation_list.html')

@app.route('/roomlist')
def room_list():
    return render_template('room_list.html')

@app.route('/tasklist')
def task_list():
    return render_template('task.html')

@app.route('/stafflist')
def staff_list():
    staffs = Employee.query.all()

    return render_template('staff.html', staffs=staffs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Employee.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            print('invalid', form.username.data)
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    else:
        print('something wrong')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
