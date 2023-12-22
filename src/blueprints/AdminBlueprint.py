from flask import Blueprint, request, render_template, session, redirect, url_for
from blueprints.AdminOrdersBlueprint import AdminOrdersBlueprint
from blueprints.AdminUsersBlueprint import AdminUsersBlueprint
from blueprints.AdminProductsBlueprint import AdminProductsBlueprint
from blueprints.AdminDistributionCentersBlueprint import AdminDistributionCentersBlueprint
from service.TransactionService import TransactionService


def AdminBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)
    transactionService: TransactionService = services["transaction"]

    adminOrdersBP = AdminOrdersBlueprint("orders", __name__, transactionService, services["order"])
    adminUsersBP = AdminUsersBlueprint("users", __name__, transactionService, services["user"])
    adminProductsBP = AdminProductsBlueprint("products", __name__, transactionService, services["product"])
    adminDistributionCentersBP = AdminDistributionCentersBlueprint("distributionCenters", __name__, transactionService, services["distributionCenter"])

    bp.register_blueprint(adminOrdersBP, url_prefix="/orders")
    bp.register_blueprint(adminUsersBP, url_prefix="/users")
    bp.register_blueprint(adminProductsBP, url_prefix="/products")
    bp.register_blueprint(adminDistributionCentersBP, url_prefix="/distribution-centers")

    @bp.before_request
    def before_request():
        if request.endpoint != "admin.loginPage":
            user = session.get("user")
            if user != "admin":
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
