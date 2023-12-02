from flask import Blueprint, request, render_template
from repository.ProductRepository import ProductRepository
from dto.Product import Product

def ProductsBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = ProductRepository(connection)
    columnNames = [s[0] for s in repository.getColoumnNames()]
    categories =  [c[0] for c in repository.getCategories() ]

    @bp.route('/', methods = ["GET"])
    def productsPage():
        querySettings = request.args.to_dict()
        fetchedProducts = repository.getAll(**querySettings)
        products = [Product(p) for p in fetchedProducts]

        return render_template('products.html', querySettings=querySettings, products = products , columnNames = columnNames , categories = categories  )
    
    @bp.route('/<int:id>', methods = ["GET"])
    def productDetailPage(id):
        return render_template('productDetailPage.html',product = Product(repository.findById(int(id))) )

    return bp

    
