from sqlite3 import Connection
from flask import Blueprint, request
from repository.OrderRepository import OrderRepository

def OrdersBlueprint(name: str, importName: str, connection: Connection):
    bp = Blueprint(name, importName)
    repository = OrderRepository(connection)

    @bp.route('/', methods = ["POST"])
    def ordersPage():
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            return repository.getAll(**request.get_json())
        else:
            return 'Content-Type not supported!'

    return bp
