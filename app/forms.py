from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

# class DatePickForm(FlaskForm):
#     checkin_date = DateField('Start', validators=[DataRequired()], format = '%d/%m/%Y', description = 'Check-in date', widget=widgets.DatePickerWidget)
#     checkout_date = DateField('Start', validators=[DataRequired()], format = '%d/%m/%Y', description = 'Check-out date', widget=widgets.DatePickerWidget)
