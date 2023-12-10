from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.auth import adminAuth, ADMIN_NOT_AUTHORIZED


def OrdersBlueprint(name: str, importName: str, service):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            adminAuth(session)
        except Exception as e:
            if e.args[0] == ADMIN_NOT_AUTHORIZED:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods=["GET"])
    def ordersPage():
        querySettings = request.args.to_dict()
        result = service.ordersPage(querySettings)
        return render_template("orders.html", querySettings=querySettings, **result)

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: str):
        result = service.orderDetailPage(id)
        return render_template("orderDetail.html", **result)

    return bp
