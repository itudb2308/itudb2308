from flask import Blueprint, request, render_template, session, redirect, url_for
from service.OrderService import OrderService


def CustomerOrdersBlueprint(name: str, importName: str, service: OrderService):
    bp = Blueprint(name, importName)

    @bp.route("/<int:id>", methods=["GET"])
    def orderDetailPage(id: int):
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
        if request.method == "POST":
            user_id = session["user_id"]
            cart = session["cart"]
            orderId = service.giveOrderPage(cart, user_id)
            session["cart"] = {}
            return redirect(url_for("customer.orders.orderDetailPage", id=orderId))
        cart = session["cart"]
        products = service.cartPage(cart)
        return render_template("cart.html", cart=cart, products=products)

    @bp.route('/addToCart', methods=["POST"])
    def addToCartPage():
        form = request.form

        product_id = form.get("product_id")
        oldQuantity = int(session["cart"][product_id]) if product_id in session["cart"] else 0
        quantity = int(form.get("quantity"))

        userProduct = service.addToCartPage(int(product_id))
        newQuantity = oldQuantity + quantity
        newQuantity = newQuantity if newQuantity < userProduct.total_stock else userProduct.total_stock
        session["cart"][product_id] = newQuantity

        # TODO: return error

        return redirect(url_for("customer.products.productDetailPage", id=product_id))

    @bp.route('/emptyCart', methods=["GET"])
    def emptyCartPage():
        session["cart"] = {}
        return redirect(url_for("customer.orders.cartPage"))

    return bp
