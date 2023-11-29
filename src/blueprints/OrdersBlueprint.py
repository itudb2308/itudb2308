from flask import Blueprint, request, render_template
from dto.Order import Order
from repository.OrderRepository import OrderRepository

def OrdersBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)
    repository = OrderRepository(connection)
    statusItems = [s[0] for s in repository.getDistinctStatus()]
    genderItems = [g[0] for g in repository.getDistinctGender()]

    @bp.route('/', methods = ["GET"])
    def ordersPage():
        settings = request.args.to_dict()
        if "limit" not in settings:
            settings["limit"] = 20
        if "p" in settings:
            p = int(settings["p"])
            settings["offset"] = (p - 1) * settings["limit"]
        orders = [Order(o) for o in repository.getAll(**settings)]
        return render_template("orders.html", orders = orders, **settings, statusItems = statusItems, genderItems = genderItems)

    @bp.route("/<id>", methods = ["GET"])
    def orderDetailPage(id: str):
        return render_template("orderDetail.html", order = Order(repository.findById(int(id))))

    return bp
