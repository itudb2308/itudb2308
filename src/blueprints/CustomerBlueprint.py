from flask import Blueprint
from blueprints.CustomerOrdersBlueprint import CustomerOrdersBlueprint
from blueprints.CustomerProductsBlueprint import CustomerProductsBlueprint
from blueprints.CustomerUsersBlueprint import CustomerUsersBlueprint


def CustomerBlueprint(name: str, importName: str, services: dict):
    bp = Blueprint(name, importName)

    bp.register_blueprint(CustomerOrdersBlueprint("orders", __name__, services["order"]), url_prefix="/orders")
    bp.register_blueprint(CustomerProductsBlueprint("products", __name__, services["product"]), url_prefix="/products")
    bp.register_blueprint(CustomerUsersBlueprint("users", __name__, services["user"]), url_prefix="/users")

    @bp.route('/', methods=['GET'])
    def homePage():
        return "Customer Home Page"

    @bp.route('/login', methods=["GET", "POST"])
    def loginPage():
        pass

    @bp.route('/logout', methods=["GET"])
    def logoutPage():
        pass

    return bp
