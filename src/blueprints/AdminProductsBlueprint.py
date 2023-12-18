from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from service.ProductService import ProductService
from validation.AdminAuth import adminAuth, ADMIN_NOT_AUTHENTICATED

from forms.AddProductForm import AddProductForm
from forms.UpdateProductForm import UpdateProductForm


def AdminProductsBlueprint(name: str, importName: str, service: ProductService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHENTICATED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods=["GET"])
    def productsPage():
        querySettings = request.args.to_dict()
        result = service.productsPage(querySettings)
        return render_template('products.html', querySettings=querySettings, **result)

    @bp.route('/<int:id>', methods=["GET"])
    def productDetailPage(id):
        result = service.productDetailPage(id)
        return render_template('productDetail.html', **result)

    @bp.route('/add_product', methods=["GET", "POST"])
    def addProductPage():
        method = request.method
        form = request.form

        result = service.addProductPage(method, form)

        if result["submitted_and_valid"] == True:
            showFlashMessages(result["flash"])
            return redirect(url_for('admin.products.productDetailPage', id=result["id"]))
        else:
            showFlashMessages(result["flash"])
            return render_template('addProduct.html', form=result["form"])

    @bp.route('/update_product/<int:id>', methods=["GET", "POST"])
    def updateProductPage(id):
        method = request.method
        form = request.form

        result = service.updateProductPage(method, form, id)

        if result["submitted_and_valid"] == True:
            showFlashMessages(result["flash"])
            return redirect(url_for('admin.products.productDetailPage', id=id))
        else:
            showFlashMessages(result["flash"])
            return render_template('updateProduct.html', form=result["form"], id=id)

    @bp.route('/delete_product/<int:id>', methods=["GET"])
    def deleteProductPage(id):
        result = service.deleteProductPage(id)
        showFlashMessages(result["flash"])
        return redirect(url_for('admin.products.productsPage'))

    @bp.route('/add_stock_to_inventory/<int:id>', methods=["POST"])
    def addStockToInventory(id):
        quantity = int(request.form["quantity"])

        service.addStockToInventoryPage(id, quantity)
        flash(f"{quantity} new product added to inventory ")
        return redirect(url_for('admin.products.productDetailPage', id=id))

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    return bp
