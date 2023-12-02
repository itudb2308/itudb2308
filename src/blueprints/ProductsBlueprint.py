from flask import Blueprint, request, render_template
from service.ProductService import ProductService

def ProductsBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    service = ProductService(connection)

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

    
