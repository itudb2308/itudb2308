from flask import Blueprint, request, render_template, session, redirect, url_for, flash
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
            showFlashMessages([("Your order is created successfully", "success")])
            return redirect(url_for("customer.orders.orderDetailPage", id=orderId))
        cart = session["cart"]
        products = service.cartPage(cart)

        if products != None:
            cartPrice = sum(map(lambda p: p.retail_price * cart[str(p.id)], products))
        else:
            cartPrice = 0

        return render_template("cart.html", cart=cart, products=products, cartPrice=cartPrice)

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

        showFlashMessages([(f"Product added to your cart. Current quantity: {newQuantity}", "success")])
        return redirect(url_for("customer.products.productDetailPage", id=product_id))

    @bp.route('/emptyCart', methods=["POST"])
    def emptyCartPage():
        if "product_id" in request.form.keys():
            session["cart"].pop(request.form["product_id"])
            showFlashMessages([("Product removed from your cart", "success")])
        else:
            session["cart"] = {}
            showFlashMessages([("All of the items in your cart removed!", "success")])
        return redirect(url_for("customer.orders.cartPage"))

    @bp.route('/changeOrderStatus/<int:id>', methods=["POST"])
    def changeOrderStatus(id: int):
        status = request.form["order_status"]
        if status in ["Returned", "Cancelled"]:
            service.setOrderStatusPage(id, status, cancelSale=True)
            showFlashMessages([(f"Your order {status.lower()} successfully", "success")])
        else:
            showFlashMessages([("New status is not permitted", "danger")])
        return redirect(url_for("customer.orders.orderDetailPage", id=id))

    def showFlashMessages(flashMessages):
        if flashMessages != None:
            for flashMessage in flashMessages:
                flash(flashMessage[0], flashMessage[1])

    return bp
