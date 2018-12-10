from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from app.dataParser import parseToDate
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')



class DatePickForm(FlaskForm):
    n_people = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4+')]
    checkin_date = StringField('Checkin date', validators=[DataRequired()])
    checkout_date = StringField('Checkout date', validators=[DataRequired()])
    people = SelectField('People', choices=n_people, validators=[DataRequired()])
    def validate(self):
        # check with original validator
        if not Form.validate(self):
            return False

        # check whether it has the format "%s %s, %s"
        if len(self.checkin_date.data.split(' ')) != 3 or len(self.checkout_date.data.split(' ')) != 3:
            return False

        # check whether it can be parsed to date format
        try :
            cindate = parseToDate(self.checkin_date.data)
            cotdate = parseToDate(self.checkout_date.data)
        except ValueError :
            return False

        # check whether the check-out date s later than check-in date
        if (cotdate - cindate).days < 1:
            return False

        # Return true if everything is fine
        return True

class customerInfoForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    e_mail = StringField('E-mail', validators=[DataRequired()])
