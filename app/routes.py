from flask import render_template, flash, request, redirect, url_for
from app import app, db, tempData
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from app.models import *
from app.dataParser import parseToDate
from datetime import datetime
from app.DBProcessor import *


##### Routes for Management part #####
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    rooms = Room.query.all()
    stays = db.session.query(Stay, Guest).filter(Stay.guest_id == Guest.id).all()
    reserves = db.session.query(Reserve, Guest).filter(Reserve.guest_id == Guest.id).all()

    if request.method == 'POST' and request.form['modal_type'] == 'check_out':
        s = Stay.query.filter(Stay.guest_id == int(request.form['guest_id'])).first()
        db.session.delete(s)
        db.session.commit()
        print('deleted')

    if request.method == 'POST' and request.form['modal_type'] == 'check_in' and (request.form.get('user_CheckBox') is not None):
        check_in_from_reservation(int(request.form['user_CheckBox']), int(request.form['room_num']))
        return redirect(url_for('index'))

    return render_template('manage/index.html', title='Welcome! DONGHotel', rooms=rooms, stays=stays, reserves=reserves)

@app.route('/reservelist')
@login_required
def reserve_list():
    reserve = db.session.query(Reserve, Room_info, Guest)\
    .filter(Reserve.room_info_id==Room_info.id).filter(Guest.id==Reserve.guest_id).all()
    
    return render_template('manage/reservation_list.html', reserve=reserve)

@app.route('/roomlist')
@login_required
def room_list():
    rooms = db.session.query(Room.num, Room_info.room_type, Room_info.room_class).filter(Room.room_info_id == Room_info.id).order_by(Room.num).all()
    return render_template('manage/room_list.html', rooms=rooms)

@app.route('/tasklist', methods=['GET', 'POST'])
@login_required
def task_list():
    if current_user.job_id != 1:
        return redirect(url_for('staff_task'))
    tasks = db.session.query(Task, Employee).outerjoin(Employee, Task.employee_id == Employee.id).all()
    staffs = db.session.query(Employee, Job).filter(Employee.job_id == Job.id).filter(Employee.on_work==True).all()
    if request.method=='POST' and request.form.get('modal_type') == 'add_task':
        db.session.add(Task(description=request.form.get('task')))
        db.session.commit()
        return redirect(url_for('task_list'))

    if request.method=='POST' and request.form.get('modal_type') == 'assign_staff':
        Employee.query.filter(Employee.id == int(request.form.get('staff'))).first()\
        .tasks.append(Task.query.filter(Task.id == int(request.form.get('task_id'))).first())
        db.session.commit()
        return redirect(url_for('task_list'))

    if request.method=='POST' and request.form.get('button_type') == 'remove_task':
        rlist = [ Task.query.filter(Task.id == int(l)).first() for l in request.form.getlist('task_list')]
        for r in rlist:
            db.session.delete(r)
        db.session.commit()
        return redirect(url_for('task_list'))

    return render_template('manage/task.html', tasks=tasks, staffs=staffs)

@app.route('/modify')
@login_required
def modify():
    return render_template('manage/modify.html')

@app.route('/staff_task', methods=['GET', 'POST'])
@login_required
def staff_task():
    tasks = Task.query.filter(Task.employee_id == current_user.id).all()
    if request.method=='POST':
        Task.query.filter(Task.id == int(request.form.get('task_id'))).first().done = True;
        db.session.commit()

    return render_template('manage/staff_task.html', tasks=tasks)


@app.route('/stafflist', methods=['GET', 'POST'])
@login_required
def staff_list():
    staffs = db.session.query(Employee, Job).filter(Employee.job_id == Job.id).all()
    languages = Language.query.all()
    jobs = Job.query.all()

    if request.method=='POST' and request.form.get('emp_fname') is not None:
        e = Employee(first_name=request.form.get('emp_fname'),
                    last_name=request.form.get('emp_lname'),
                    job_id=int(request.form.get('job')),
                    phone=request.form.get('phone')
                    )
        langlist = request.form.getlist('langs')
        langs = [ Language.query.filter(Language.id == int(l)).first() for l in langlist ]
        for l in langs:
            e.language.append(l)

        e.username = request.form.get('username')
        e.set_password(request.form.get('password'))
        db.session.add(e)
        db.session.commit()

        print('successfully added', e.first_name, e.last_name, e.id)
        return redirect(url_for('staff_list'))
    if request.method=='POST' and request.form.get('request_type') == 'remove':
        removelist = [ Employee.query.filter(Employee.id == int(l)).first() for l in request.form.getlist('staffs') ]
        for l in removelist:
            db.session.delete(l)
        db.session.commit()
        return redirect(url_for('staff_list'))


    return render_template('manage/staff.html', staffs=staffs, languages=languages, jobs=jobs)

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
    else:
        print('invalid', form.checkin_date.data)
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
    cform = customerInfoForm(request.form)

    if form.validate_on_submit():
        checkin_date = parseToDate(form.checkin_date.data)
        checkout_date = parseToDate(form.checkout_date.data)
        # Store form info into tempData
        tempData.CustomerData.checkin_date = checkin_date
        tempData.CustomerData.checkout_date = checkout_date
        tempData.CustomerData.n_people = int(form.people.data)
        availRooms, occupiedRooms = availableRooms(checkin_date, checkout_date, int(form.people.data))
        return render_template('customer/reserve.html', form=form, cform=cform, availRooms=availRooms, occupiedRooms=occupiedRooms, code=307)
    else:
        availRooms, occupiedRooms = availableRooms(datetime(1900, 1, 1), datetime(3000, 12, 31), 0)

    if cform.validate_on_submit():
        tempData.CustomerData.first_name = cform.first_name.data
        tempData.CustomerData.last_name = cform.last_name.data
        tempData.CustomerData.birthday = cform.birthday.data
        tempData.CustomerData.phone_number = cform.phone_number.data
        tempData.CustomerData.email = cform.e_mail.data
        tempData.RoomData.room_info_id = int(request.form['rinfo_id'])
        make_reservation()
        print('success!')

    return render_template('customer/reserve.html', form=form, cform=cform, availRooms=availRooms, occupiedRooms=occupiedRooms, code=307)

# @app.route('/customer/request_reservation', methods=['POST'])
# def request_reservation():
#     pass

@app.route('/customer/contact')
def contact():
    return render_template('customer/contact.html')

##### End - Routes for Customer part #####


##### Route for Room service #####
@app.route('/roomservice')
def roomservice():
    return render_template('roomservice/tablet_index.html')
