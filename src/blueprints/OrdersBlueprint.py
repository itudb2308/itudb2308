from sqlite3 import Connection
from flask import Blueprint, request, render_template
from repository.OrderRepository import OrderRepository

def OrdersBlueprint(name: str, importName: str, connection: Connection):
    bp = Blueprint(name, importName)
    repository = OrderRepository(connection)

    @bp.route('/', methods = ["GET", "POST"])
    def ordersPage():
        if request.method == "POST":
            settings = request.form.to_dict()
            orders = repository.getAll(**settings)
            return render_template("orders.html", orders = orders)
        else:
            return render_template("orders.html")

    @bp.route("/<id>", methods = ["GET"])
    def orderDetailPage(id: str):
        order = repository.findById(int(id))
        orderInfo = []
        for info in order:
            orderInfo.append(info)
        return orderInfo

    return bp
