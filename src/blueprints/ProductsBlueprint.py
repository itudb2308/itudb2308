from flask import Blueprint, request, render_template, flash, redirect, url_for
from service.ProductService import ProductService

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError

def ProductsBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.route('/', methods = ["GET"])
    def productsPage():
        querySettings = request.args.to_dict()
        result = service.productsPage(querySettings)
        return render_template('products.html', querySettings=querySettings, **result)
    
    @bp.route('/<int:id>', methods = ["GET"])
    def productDetailPage(id):
        result = service.productDetailPage(id)
        return render_template('productDetail.html', **result)

    @bp.route('/add_product', methods = ["GET", "POST"])
    def addProductPage():
        if request.method == "GET":            
            form = AddProductForm()
            return render_template('addProduct.html', form=form)
        else :
            form = AddProductForm(request.form) 
            if form.validate_on_submit():
                product = form.data
                # add product to database
                result = service.addProductPage(product)
                # redirect to product detail page of the newly added product
                flash("Product added successfully", "success")
                return redirect(url_for('admin.products.productDetailPage', id=result))
            
            else :
                flash("Form data is invalid", "danger")
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        flash(f"{fieldName}: {err}", "danger")
                return render_template('addProduct.html', form = form)
    
    @bp.route('/update_product/<int:id>', methods = ["GET", "POST"])
    def updateProductPage(id):
        if request.method == "GET":
            product = service.findById(id)
            product = product.__dict__

            # change buttons text to "Update Product" instead of "Add Product"
            form = AddProductForm(data=product)
            form.submit.label.text = "Update Product"

            return render_template('updateProduct.html', form=form, id=id)
        else :
            form = AddProductForm(request.form) 
            form.submit.label.text = "Update Product"

            if form.validate_on_submit():
                product = form.data
                # add id to product such that repository can use it to update the product
                product["id"] = id

                # update product on database
                result = service.updateProductPage(product)
                # redirect to product detail page of the updated product
                flash("Product updated successfully", "success")
                return redirect(url_for('admin.products.productDetailPage', id=result))
            
            else :
                flash("Form data is invalid", "danger")
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        flash(f"{fieldName}: {err}", "danger")
                return render_template('updateProduct.html', form = form, id=id)


    class AddProductForm(FlaskForm):
        # get choices for form fields from database
        distribution_centers_choices = service.getDistributionCenters({"order_by_columnName": "name", "order_by_direction": "asc"})
        # convert DistributionCenter objects to mapping
        distribution_centers_choices = [(dc.id, dc.name) for dc in distribution_centers_choices]
        
        category_choices = service.getCategories()
        category_choices = [(c, c) for c in category_choices]

        brand_choices = service.getBrandNames()
        brand_choices = [(b, b) for b in brand_choices]

        name = StringField("Name", validators=[DataRequired()])
        cost = FloatField("Cost", validators=[DataRequired(), NumberRange(min=0)])
        category = SelectField("Category", validators=[DataRequired()], choices=category_choices)
        brand = SelectField("Brand", validators=[DataRequired()],choices=brand_choices)
        retail_price = FloatField("Retail Price", validators=[DataRequired(), NumberRange(min=0)])
        department = SelectField("Department", validators=[DataRequired()], choices=["Men","Women"])
        sku = IntegerField("SKU", validators=[DataRequired(), NumberRange(min=0)])
        distribution_center_id = SelectField("Distribution Center", validators=[DataRequired()], choices=distribution_centers_choices)
        submit = SubmitField("Add Product")

    return bp

    
