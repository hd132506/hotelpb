from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, time

######### Employee Part #########

# Helper table for many-to-many relationship
languages = db.Table('languages', db.Model.metadata,
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
    )

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), index=True)
    job = db.Column(db.String(45), index=True)
    phone = db.Column(db.String(45))
    on_work = db.Column(db.Boolean, default=False)
    languages = db.relationship('Language', secondary=languages, lazy='subquery',
        backref=db.backref('employees'), cascade='all, delete-orphan', single_parent=True)
    work = db.relationship('Work', backref=db.backref('employee'), cascade='all, delete-orphan', single_parent=True)
    offduty = db.relationship('OffDuty', backref=db.backref('employee'), cascade='all, delete-orphan', single_parent=True)
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee {}>'.format(self.last_name)

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(15))

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    work_day = db.Column(db.String(10), nullable=False, index=True)
    puchin_time = db.Column(db.Time, nullable=False, index=True)
    puchout_time = db.Column(db.Time, nullable=False)

class OffDuty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_day = db.Column(db.DateTime, nullable=False, index=True)
    end_day = db.Column(db.DateTime, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow)

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))

######### Guest Part #########

class Room_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(10), nullable=False, index=True)
    room_class = db.Column(db.String(10), nullable=False, index=True)
    fee = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    rooms = db.relationship('Room', backref='room_info', cascade='all, delete-orphan')
    reservations = db.relationship('Reserve', backref='room_info')

class Room(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    room_info_id = db.Column(db.Integer, db.ForeignKey('room_info.id'), nullable=False)
    usuable = db.Column(db.Boolean, default=False)
    stay = db.relationship('Stay', backref='room', uselist=False, cascade='all, delete-orphan')

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45), nullable=False, index=True)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(1))
    head_cnt = db.Column(db.Integer, nullable=False)
    country_code = db.Column(db.String(3))
    check_in_date = db.Column(db.Date, nullable=False, index=True)
    check_out_date = db.Column(db.Date, nullable=False, index=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    reserve = db.relationship('Reserve', backref='guest', cascade='all, delete-orphan')
    stay = db.relationship('Stay', backref='guest', cascade='all, delete-orphan')

class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_info_id = db.Column(db.Integer, db.ForeignKey('room_info.id'), nullable=False)
    reserve_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    paid = db.Column(db.Boolean, nullable=False)

class Stay(db.Model):
    room_num = db.Column(db.Integer, db.ForeignKey('room.num'), primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), primary_key=True)
    absence = db.Column(db.Boolean)
    last_cleaning_time = db.Column(db.DateTime, index=True)
    message = db.relationship('Message', backref='stay', cascade='all, delete-orphan')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('stay.guest_id'), nullable=False)
    description = db.Column(db.Text)
