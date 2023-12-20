from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService
from validation.CustomerAuth import customerAuth, CUSTOMER_NOT_AUTHENTICATED


def CustomerOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: str):
        # if there occures TypeError, it means that order is None
        try:
            result = service.orderDetailPage(id)
        except TypeError:
            return render_template("404.html")

        if session["user_id"] != result["user"].id:
            return render_template("403.html")

        return render_template("customerOrderDetail.html", **result)
    
    @bp.route('/cart', methods=["GET", "POST"])
    def cartPage():
        if request.method == "GET":
            cart = session["cart"]
            products = service.cartPage(cart)
            return render_template("cart.html", cart=cart, products=products)

        elif request.method == "POST":
            #result = service.cartPage(cart)
            pass

    @bp.route('/addToCart', methods=["POST"])
    def addToCartPage():
        form = request.form
        print(form)
        if form.get("product_id") in session["cart"]:
            session["cart"][form.get("product_id")] = int(session["cart"][form.get("product_id")]) + int(form.get("quantity"))
        else:
            session["cart"][form.get("product_id")] = int(form.get("quantity"))
        return redirect(url_for("customer.products.productDetailPage", id = form.get("product_id")))

    return bp
