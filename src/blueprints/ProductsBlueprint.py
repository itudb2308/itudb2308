from flask import Blueprint, request, render_template, session, redirect, url_for
from service.ProductService import ProductService
from validation.auth import adminAuth, ADMIN_NOT_AUTHORIZED

def ProductsBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHORIZED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods = ["GET"])
    def productsPage():
        querySettings = request.args.to_dict()
        result = service.productsPage(querySettings)
        return render_template('products.html', querySettings=querySettings, **result)
    
    @bp.route('/<int:id>', methods = ["GET"])
    def productDetailPage(id):
        result = service.productDetailPage(id)
        return render_template('productDetail.html', **result)

    return bp

    
