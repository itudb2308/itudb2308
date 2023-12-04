from flask import Blueprint, request, render_template
from service.OrderService import OrderService

def OrdersBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.route('/', methods = ["GET"])
    def ordersPage():
        querySettings = request.args.to_dict()
        result = service.ordersPage(querySettings)
        return render_template("orders.html", querySettings=querySettings, **result)

    @bp.route("/<int:id>", methods = ["GET"])
    def orderDetailPage(id: str):
        result = service.orderDetailPage(id)
        return render_template("orderDetail.html", **result)

    return bp
