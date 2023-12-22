from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from service.TransactionService import TransactionService


def AdminOrdersBlueprint(name: str, importName: str, transactionService: TransactionService, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route('/', methods=["GET"])
    def ordersPage():
        querySettings = request.args.to_dict()
        result = service.ordersPage(querySettings)
        return render_template("orders.html", querySettings=querySettings, **result)

    @bp.route("/<int:id>", methods=["GET", "POST"])
    @transactionService.transactional()
    def orderDetailPage(id: int, **kwargs):
        transaction = kwargs["transaction"]

        if request.method == "POST":
            orderStatus = request.form.get("order_status")
            service.setOrderStatusPage(id, orderStatus, cancelSale=(orderStatus == "Cancelled"))
        # result = service.orderDetailPage(id)
        result = {}
        result["order"] = service.findById(transaction, id)
        result["orderItems"] = service.getItemDetailsByOrderId(transaction, id)
        user_id = result["order"].user_id
        result["user"] = service.getUserById(transaction, user_id)
        result["totalOrderPrice"] = sum(map(lambda oi: oi.quantity * oi.price, result["orderItems"]))
        return render_template("orderDetail.html", **result)

    return bp
