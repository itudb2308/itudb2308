from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional, Length, Regexp
from dto.Transaction import Transaction


class ProductForm(FlaskForm):
    def __init__(self, service, transaction: Transaction, data=None):
        super(ProductForm, self).__init__(data=data)

        # Get choices for form fields from the database
        distribution_centers_choices = service.getDistributionCenters(transaction, {"order_by_columnName": "name", "order_by_direction": "asc"})
        distribution_centers_choices = [(dc.id, dc.name) for dc in distribution_centers_choices]

        category_choices = service.getCategories(transaction)
        category_choices = [(c, c) for c in category_choices]

        brand_choices = service.getBrandNames(transaction)
        brand_choices = [(b, b) for b in brand_choices]

        # Set choices for form fields
        self.distribution_center_id.choices = distribution_centers_choices
        self.category.choices = category_choices
        self.brand.choices = brand_choices

    name = StringField("Name", validators=[DataRequired()])
    cost = FloatField("Cost", validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField("Category", validators=[DataRequired()])
    brand = SelectField("Brand", validators=[DataRequired()])
    retail_price = FloatField("Retail Price", validators=[DataRequired(), NumberRange(min=0)])
    department = SelectField("Department", validators=[DataRequired()], choices=["Men", "Women"])
    distribution_center_id = SelectField("Distribution Center", validators=[DataRequired()])
    submit = SubmitField("Add Product")
