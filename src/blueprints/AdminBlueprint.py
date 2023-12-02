from flask import Blueprint, request, render_template
from blueprints.OrdersBlueprint import OrdersBlueprint
from blueprints.UsersBlueprint import UsersBlueprint
from blueprints.ProductsBlueprint import ProductsBlueprint
from blueprints.DistributionCentersBlueprint import DistributionCentersBlueprint

def AdminBlueprint(name: str, importName: str, connection):
    bp = Blueprint(name, importName)

    bp.register_blueprint(OrdersBlueprint("orders", __name__, connection), url_prefix="/orders")
    bp.register_blueprint(UsersBlueprint("users",__name__,connection), url_prefix="/users")
    bp.register_blueprint(ProductsBlueprint("products", __name__, connection), url_prefix="/products")
    bp.register_blueprint(DistributionCentersBlueprint("distributionCenters", __name__, connection), url_prefix="/distribution-centers")
    return bp
