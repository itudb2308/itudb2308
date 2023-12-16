from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.AdminAuth import adminAuth, ADMIN_NOT_AUTHENTICATED


def AdminOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHENTICATED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods=["GET"])
    def ordersPage():
        querySettings = request.args.to_dict()
        result = service.ordersPage(querySettings)
        return render_template("orders.html", querySettings=querySettings, **result)

    @bp.route("/<int:id>", methods=["GET", "PUT"])
    def orderDetailPage(id: int):
        if request.method == "PUT":
            orderStatus = request.form.get("order_status")
            service.setOrderStatus(id, orderStatus)
        result = service.orderDetailPage(id)
        return render_template("orderDetail.html", **result)

    return bp
