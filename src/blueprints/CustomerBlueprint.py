from flask import Blueprint, request, redirect, render_template, session, url_for
from blueprints.CustomerOrdersBlueprint import CustomerOrdersBlueprint
from blueprints.CustomerProductsBlueprint import CustomerProductsBlueprint
from blueprints.CustomerUsersBlueprint import CustomerUsersBlueprint


def CustomerBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)

    bp.register_blueprint(CustomerOrdersBlueprint("orders", __name__, services["order"]), url_prefix="/orders")
    bp.register_blueprint(CustomerProductsBlueprint("products", __name__, services["product"]), url_prefix="/products")
    bp.register_blueprint(CustomerUsersBlueprint("users", __name__, services["user"]), url_prefix="")

    @bp.route('/', methods=['GET'])
    def homePage():
        return render_template('customerIndex.html', session=session)

    @bp.route('/login', methods=["GET", "POST"])
    def loginPage():
        if request.method == "GET":
            if session.get("user_logged_in") == True:
                return redirect(url_for('customer.homePage'))
            else:
                session["user_logged_in"] = False
                return render_template('customerLogin.html')
        elif request.method == "POST":
            email = request.form['email']
            password = request.form["password"]
            user = services["user"].findByEmail(email)
            if user.email != None and password == user.email:
                sessionHandleUserLogin(user)
                return redirect(url_for('customer.homePage'))
            else:
                return redirect(url_for('customer.loginPage'))

    @bp.route('/logout', methods=["GET"])
    def logoutPage():
        if request.method == "GET":
            session.clear()
            return redirect(url_for('customer.homePage'))

    def sessionHandleUserLogin(user):
        session["user"] = user.id
        session["name"] = user.first_name + " " + user.last_name
        session["user_logged_in"] = True
        session["id"] = services["user"].sessionIdGenerator()
        return session 
    return bp
