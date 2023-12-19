from flask import Blueprint, request, render_template, session, redirect, url_for
from blueprints.AdminOrdersBlueprint import AdminOrdersBlueprint
from blueprints.AdminUsersBlueprint import AdminUsersBlueprint
from blueprints.AdminProductsBlueprint import AdminProductsBlueprint
from blueprints.AdminDistributionCentersBlueprint import AdminDistributionCentersBlueprint

from validation.AdminAuth import adminAuth, ADMIN_NOT_AUTHENTICATED


def AdminBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)
    bp.register_blueprint(AdminOrdersBlueprint("orders", __name__, services["order"]), url_prefix="/orders")
    bp.register_blueprint(AdminUsersBlueprint("users", __name__, services["user"]), url_prefix="/users")
    bp.register_blueprint(AdminProductsBlueprint("products", __name__, services["product"]), url_prefix="/products")
    bp.register_blueprint(AdminDistributionCentersBlueprint("distributionCenters", __name__, services["distributionCenter"]), url_prefix="/distribution-centers")

    @bp.before_request
    def before_request():
        if request.endpoint != "admin.loginPage":
            try:
                adminAuth(session)
            except Exception as e:
                if e.args[0] == ADMIN_NOT_AUTHENTICATED:
                    return redirect(url_for('admin.loginPage'))

    @bp.route('/', methods=['GET'])
    def homePage():
        return render_template('index.html', session=session)

    @bp.route('/login', methods=["GET", "POST"])
    def loginPage():
        if request.method == "GET":
            if session.get("admin_logged_in") == True:
                return redirect(url_for('admin.homePage'))
            else:
                return render_template('login.html')
        elif request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            if email == 'admin@admin.net' and password == 'admin':
                session["user"] = 'admin'
                session["admin_logged_in"] = True
                return redirect(url_for('admin.homePage'))
            else:
                return redirect(url_for('admin.loginPage'))

    @bp.route('/logout', methods=["GET"])
    def logoutPage():
        if request.method == "GET":
            session.clear()
            return redirect(url_for('admin.homePage'))

    return bp
