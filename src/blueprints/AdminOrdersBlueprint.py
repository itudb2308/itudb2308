from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.AdminAuth import adminAuth, ADMIN_NOT_AUTHENTICATED


def AdminOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route('/', methods=["GET"])
    def ordersPage():
        querySettings = request.args.to_dict()
        result = service.ordersPage(querySettings)
        return render_template("orders.html", querySettings=querySettings, **result)

    @bp.route("/<int:id>", methods=["GET", "POST"])
    def orderDetailPage(id: int):
        if request.method == "POST":
            orderStatus = request.form.get("order_status")
            service.setOrderStatusPage(id, orderStatus, cancelSale=(orderStatus == "Cancelled"))
        result = service.orderDetailPage(id)
        return render_template("orderDetail.html", **result)

    return bp
