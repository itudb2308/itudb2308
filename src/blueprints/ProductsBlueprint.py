from flask import Blueprint, request, render_template
from repository.ProductsRepository import ProductsRepository
from dto.Product import Product

def ProductsBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = ProductsRepository(connection)
    columnNames = [s[0] for s in repository.getColoumnNames()]
    categories =  [c[0] for c in repository.getCategories() ]

    @bp.route('/', methods = ["POST","GET"])
    def productsPage():
        settings = request.args.to_dict()
        fetchedProducts = repository.getAll(**settings)
        products = [Product(p) for p in fetchedProducts]

        return render_template('products.html', products = products , columnNames = columnNames , categories = categories  )
    
    @bp.route('/<int:id>', methods = ["GET"])
    def productDetailPage(id):
        return render_template('productDetailPage.html',product = Product(repository.findById(int(id))) )

    return bp

    
