from flask import Blueprint, request, render_template, flash, redirect, url_for
from service.ProductService import ProductService

from forms.AddProductForm import AddProductForm
from forms.UpdateProductForm import UpdateProductForm

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
            form = AddProductForm(service)
            return render_template('addProduct.html', form=form)
        else :
            form = AddProductForm(service, data=request.form.to_dict())

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
            
            form = UpdateProductForm(service,data=product)
            
            return render_template('updateProduct.html', form=form, id=id)
        else :
            form = UpdateProductForm(service, data = request.form.to_dict()) 

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

    return bp

    
