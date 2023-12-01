from flask import Blueprint, request, render_template
from repository.ProductsRepository import ProductsRepository


def ProductsBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = ProductsRepository(connection)

    @bp.route('/', methods = ["POST","GET"])
    def productsPage():
        settings = request.args.to_dict()
        products = repository.getAll(**settings)
        return render_template('products.html', products = products )
    
    @bp.route('/<id>', methods = ["POST","GET"])
    def productDetailPage():
        return render_template('productDetailPage.html')

    return bp
