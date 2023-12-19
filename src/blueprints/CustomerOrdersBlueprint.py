from flask import Blueprint, render_template, session, redirect, url_for
from service.OrderService import OrderService


def CustomerOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: id):
        result = service.orderDetailPage(id)
        if result["user"].id != session["user_id"]:
            return render_template("401.html")
        return render_template("customerOrderDetail.html", **result)

    return bp
