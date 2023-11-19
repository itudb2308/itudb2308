from sqlite3 import Connection
from flask import Blueprint, request
from repository.ProductsRepository import ProductsRepository


def ProductsBlueprint(name: str, importName: str, connection: Connection):
    bp = Blueprint(name, importName)
    repository = ProductsRepository(connection)

    @bp.route('/', methods = ["POST"])
    def productsView():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            return repository.getAll(**request.get_json())
        else:
            return 'Content-Type not supported!'

    return bp
