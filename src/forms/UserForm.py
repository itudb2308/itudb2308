from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional, Length, Regexp
import subprocess
import random
import datetime


class UserForm(FlaskForm):
    def __init__(self, service, data=None):
        super(UserForm, self).__init__(data=data)

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    gender = SelectField("Gender", validators=[DataRequired()], choices=["M", "F"])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=0)])
    street_address = StringField("Street Address", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    postal_code = StringField("Postal Code", validators=[DataRequired()])
    submit = SubmitField("Register")
