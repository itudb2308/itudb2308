from flask import Blueprint, request, render_template
from repository.ProductsRepository import ProductsRepository


def ProductsBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = ProductsRepository(connection)
    columnNames = [s[0] for s in repository.getColoumnNames()]
    categories =  [c[0] for c in repository.getCategories() ]

    @bp.route('/', methods = ["POST","GET"])
    def productsPage():
        settings = request.args.to_dict()
        products = repository.getAll(**settings)
        return render_template('products.html', products = products , columnNames = columnNames , categories = categories  )
    
    @bp.route('/<id>', methods = ["POST","GET"])
    def productDetailPage():
        return render_template('productDetailPage.html')

    return bp
