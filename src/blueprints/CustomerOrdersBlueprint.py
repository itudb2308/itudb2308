from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: str):
        result = service.orderDetailPage(id)
        return render_template("customerOrderDetail.html", **result)

    return bp
