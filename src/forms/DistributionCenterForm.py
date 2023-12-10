from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional, Length, Regexp


class DistributionCenterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Add Distribution Center")


class UpdateDistributionCenterForm(FlaskForm):
    def __init__(self, data=None):
        super().__init__(data=data)

    id = IntegerField("ID")
    name = StringField("Name", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Update Distribution Center")
