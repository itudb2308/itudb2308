import psycopg2
from flask import Flask
from blueprints.AdminBlueprint import AdminBlueprint
from blueprints.CustomerBlueprint import CustomerBlueprint
from repository.DistributionCenterRepository import DistributionCenterRepository
from repository.EventRepository import EventRepository
from repository.InventoryItemRepository import InventoryItemRepository
from repository.OrderItemRepository import OrderItemRepository
from repository.OrderRepository import OrderRepository
from repository.ProductRepository import ProductRepository
from repository.UserRepository import UserRepository
from service.DistributionCenterService import DistributionCenterService
from service.OrderService import OrderService
from service.ProductService import ProductService
from service.TransactionService import TransactionService
from service.UserService import UserService

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

# CREATE REPOSITORIES
repositories = {
    "distributionCenter": DistributionCenterRepository(connection),
    "event": EventRepository(connection),
    "inventoryItem": InventoryItemRepository(connection),
    "orderItem": OrderItemRepository(connection),
    "order": OrderRepository(connection),
    "product": ProductRepository(connection),
    "user": UserRepository(connection),
}

# CREATE SERVICES
services = {
    "distributionCenter": DistributionCenterService(repositories),
    "order": OrderService(repositories),
    "product": ProductService(repositories),
    "user": UserService(repositories),
    "transaction": TransactionService(connection)
}

# REFER BETWEEN SERVICES
services["order"].setUserService(services["user"])
services["order"].setProductService(services["product"])
services["user"].setOrderService(services["order"])
services["product"].setDistributionCenterService(services["distributionCenter"])

app = Flask(__name__)
app.register_blueprint(AdminBlueprint("admin", __name__, services), url_prefix="/admin")
app.register_blueprint(CustomerBlueprint("customer", __name__, services), url_prefix="")

app.config['SECRET_KEY'] = '048275bd7538e006d38094a22bf5e730'

if __name__ == "__main__":
    app.run(debug=True)
