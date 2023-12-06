from flask import Blueprint, request, render_template, session, redirect, url_for
from blueprints.OrdersBlueprint import OrdersBlueprint
from blueprints.UsersBlueprint import UsersBlueprint
from blueprints.ProductsBlueprint import ProductsBlueprint
from blueprints.DistributionCentersBlueprint import DistributionCentersBlueprint

def AdminBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)

    bp.register_blueprint(OrdersBlueprint("orders", __name__, services["order"]), url_prefix="/orders")
    bp.register_blueprint(UsersBlueprint("users",__name__, services["user"]), url_prefix="/users")
    bp.register_blueprint(ProductsBlueprint("products", __name__, services["product"]), url_prefix="/products")
    bp.register_blueprint(DistributionCentersBlueprint("distributionCenters", __name__, services["distributionCenter"]), url_prefix="/distribution-centers")

    @bp.route('/', methods = ['GET'])
    def homePage():
        return render_template('index.html', session = session)
    
    @bp.route('/login', methods=["GET","POST"])
    def loginPage():
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            if email == 'admin@admin.net' and password == 'admin':
                session["user"] = 'admin'
                session["logged_in"] = True
                return redirect(url_for('admin.homePage'))
            else:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/logout', methods=["GET"])
    def logoutPage():
        if request.method == "GET":
            session.clear()
            return redirect(url_for('admin.homePage'))

    return bp
