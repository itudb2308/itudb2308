from flask import Blueprint, request, render_template
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
    return bp
