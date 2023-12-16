from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.before_request
    def before_request():
        try:
            customerAuth(session)
        except Exception as e:
            if e.args[0] == CUSTOMER_NOT_AUTHENTICATED:
                return redirect(url_for('customer.loginPage'))

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: str):
        result = service.orderDetailPage(id)
        return render_template("customerOrderDetail.html", **result)

    return bp
