from flask import render_template, flash, request, redirect, url_for
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from app.models import *
from app.dataParser import parseToDate
from datetime import datetime
from app.DBProcessor import *


##### Routes for Management part #####
@app.route('/')
@app.route('/index')
@login_required
def index():
    rooms = Room.query.all()
    return render_template('manage/index.html', title='Welcome! DONGHotel', rooms=rooms)

@app.route('/reservelist')
@login_required
def reserve_list():
    return render_template('manage/reservation_list.html')

@app.route('/roomlist')
@login_required
def room_list():
    return render_template('manage/room_list.html')

@app.route('/tasklist')
@login_required
def task_list():
    return render_template('manage/task.html')

@app.route('/stafflist')
@login_required
def staff_list():
    staffs = Employee.query.all()
    return render_template('manage/staff.html', staffs=staffs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Employee.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('manage/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

##### End - for Management part #####

##### Routes for Customer part #####

@app.route('/customer', methods=['GET', 'POST'])
@app.route('/customer/', methods=['GET', 'POST'])
@app.route('/customer/index', methods=['GET', 'POST'])
def cindex():
    form = DatePickForm(request.form)
    if form.validate_on_submit():
        return redirect(url_for('reserve'), code=307)
    return render_template('customer/index.html', form=form)

@app.route('/customer/room')
def croom():
    return render_template('customer/rooms.html')

@app.route('/customer/services')
def cservice():
    return render_template('customer/services.html')

@app.route('/customer/about')
def about():
    return render_template('customer/about.html')

@app.route('/customer/reserve', methods=['GET', 'POST'])
def reserve():
    form = DatePickForm(request.form)
    if form.validate_on_submit():
        checkin_date = parseToDate(form.checkin_date.data)
        checkout_date = parseToDate(form.checkout_date.data)
        availRooms, occupiedRooms = availableRooms(checkin_date, checkout_date, int(form.people.data))
        return render_template('customer/reserve.html', form=form, availRooms=availRooms, occupiedRooms=occupiedRooms)
    else:
        availRooms, occupiedRooms = availableRooms(datetime(1900, 1, 1), datetime(3000, 12, 31), 0)
    return render_template('customer/reserve.html', form=form, availRooms=availRooms, occupiedRooms=occupiedRooms)

@app.route('/customer/request_reservation', methods=['POST'])
def request_reservation():
    pass

@app.route('/customer/contact')
def contact():
    return render_template('customer/contact.html')

##### End - Routes for Customer part #####
