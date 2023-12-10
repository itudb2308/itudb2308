import psycopg2
from flask import Flask, render_template
from blueprints.AdminBlueprint import AdminBlueprint
from repository import DistributionCenterRepository, EventRepository, InventoryItemRepository, OrderItemRepository, OrderRepository, ProductRepository, UserRepository
from service import DistributionCenterService, OrderService, ProductService, UserService

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

# CREATE REPOSITORIES
repositories = {
    "distributionCenter": DistributionCenterRepository.DistributionCenterRepository(connection),
    "event": EventRepository.EventRepository(connection),
    "inventoryItem": InventoryItemRepository.InventoryItemRepository(connection),
    "orderItem": OrderItemRepository.OrderItemRepository(connection),
    "order": OrderRepository.OrderRepository(connection),
    "product": ProductRepository.ProductRepository(connection),
    "user": UserRepository.UserRepository(connection),
}

# CREATE SERVICES
services = {
    "distributionCenter": DistributionCenterService.DistributionCenterService(repositories["distributionCenter"]),
    "order": OrderService.OrderService(repositories["order"], repositories["orderItem"]),
    "product": ProductService.ProductService(repositories["product"], repositories["inventoryItem"]),
    "user": UserService.UserService(repositories["user"], repositories["event"]),
}

# REFER BETWEEN SERVICES
services["order"].userService = services["user"]
services["user"].orderService = services["order"]
services["product"].distributionCenterService = services["distributionCenter"]

app = Flask(__name__)
app.register_blueprint(AdminBlueprint("admin", __name__, services), url_prefix="/admin")

app.config['SECRET_KEY'] = '048275bd7538e006d38094a22bf5e730'

if __name__ == "__main__":
    app.run(debug=True)
