import typing

from dto.Transaction import Transaction
from dto.User import User
from repository.OrderRepository import OrderRepository
from repository.OrderItemRepository import OrderItemRepository
from dto.Order import Order
from dto.OrderItem import OrderItem
from dto.Product import Product
from dto.DistributionCenter import DistributionCenter
from service.Common import getPaginationObject, handleLimitAndOffset, transactional

if typing.TYPE_CHECKING:
    from service.UserService import UserService
    from service.ProductService import ProductService


class OrderService:
    def __init__(self, repositories: dict) -> None:
        self._orderRepository: OrderRepository = repositories["order"]
        self._orderItemRepository: OrderItemRepository = repositories["orderItem"]
        self._userService: UserService = None
        self._productService: ProductService = None

    def setUserService(self, userService):
        self._userService = userService

    def setProductService(self, productService):
        self._productService = productService

    # PAGE METHODS
    @transactional
    def ordersPage(self, querySettings: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        orders, count = self.getAllAndCount(transaction, querySettings)
        result["orders"] = orders
        result["pagination"] = getPaginationObject(count, querySettings)

        result["statusItems"] = self.getDistinctStatus(transaction)
        result["genderItems"] = self.getDistinctGender(transaction)
        return result

    @transactional
    def orderDetailPage(self, id: int, **kwargs):
        transaction = kwargs["transaction"]
        result = dict()
        result["order"] = self.findById(transaction, id)
        result["orderItems"] = self.getItemDetailsByOrderId(transaction, id)
        user_id = result["order"].user_id
        result["user"] = self._userService.findById(transaction, user_id)
        result["totalOrderPrice"] = sum(map(lambda oi: oi.quantity * oi.price, result["orderItems"]))
        return result

    @transactional
    def cartPage(self, cart: dict, **kwargs) -> [Product]:
        transaction = kwargs["transaction"]
        productIds = [int(i) for i in cart.keys()]
        if len(productIds) == 0:
            return None
        products = self._productService.findByIds(transaction, productIds)
        return products

    @transactional
    def giveOrderPage(self, cart: dict, userId: int, **kwargs):
        transaction = kwargs["transaction"]
        orderedProducts = self._productService.sellProducts(transaction, cart)
        user = self._userService.findById(transaction, userId)
        orderId = self.createOrder(transaction, user, orderedProducts)
        return orderId

    @transactional
    def addToCartPage(self, productId: int, **kwargs):
        transaction = kwargs["transaction"]
        return self._productService.getUserProductById(transaction, productId)

    @transactional
    def setOrderStatusPage(self, id: int, orderStatus: str, **kwargs):
        transaction = kwargs["transaction"]
        self.setOrderStatus(transaction, id, orderStatus)
        if "cancelSale" in kwargs and kwargs["cancelSale"]:
            ids = self._orderItemRepository.getInventoryItemIdsByOrderId(transaction, id)
            print(ids)
            self._productService.cancelSale(transaction, ids)

    # SERVICE METHODS
    def getAllAndCount(self, transaction: Transaction, settings: dict) -> ([Order], int):
        settings = handleLimitAndOffset(settings)
        data = self._orderRepository.getAllAndCount(transaction, **settings)
        orders = [Order(o) for o in data]
        count = data[0][-1] if len(data) > 1 else 0
        return orders, count

    def findById(self, transaction: Transaction, id: int) -> Order:
        return Order(self._orderRepository.findById(transaction, id))

    def getDistinctStatus(self, transaction: Transaction) -> [str]:
        return [s[0] for s in self._orderRepository.getDistinctStatus(transaction)]

    def getDistinctGender(self, transaction: Transaction) -> [str]:
        return [g[0] for g in self._orderRepository.getDistinctGender(transaction)]

    def getItemDetailsByOrderId(self, transaction: Transaction, orderId: int) -> [OrderItem]:
        data = self._orderItemRepository.getItemDetailsByOrderId(transaction, orderId)
        return [OrderItem(d) for d in data]

    def setOrderStatus(self, transaction: Transaction, id: int, orderStatus: str):
        print("STATUS: ", orderStatus)
        distinctStatus = self.getDistinctStatus(transaction)
        if orderStatus not in distinctStatus:
            raise Exception("Invalid Order Status")

        querySettings = {
            "order_id": id,
            "order_status": orderStatus,
            "update_timestamp": False,
            "timestamp_column_name": "",
        }

        if orderStatus == "Shipped":
            querySettings["update_timestamp"] = True
            querySettings["timestamp_column_name"] = "shipped_at"
        elif orderStatus == "Complete":
            querySettings["update_timestamp"] = True
            querySettings["timestamp_column_name"] = "delivered_at"
        elif orderStatus == "Returned":
            querySettings["update_timestamp"] = True
            querySettings["timestamp_column_name"] = "returned_at"

        querySettings["update_timestamp"] = "" if querySettings["update_timestamp"] else "--"

        self._orderRepository.setOrderStatus(transaction, querySettings)

    def createOrder(self, transaction: Transaction, user: User, orderedProducts: dict) -> id:
        numOfProducts = sum(map(lambda k: len(k["ids"]), orderedProducts.values()))

        createOrderSettings = {
            "user_id": user.id,
            "user_gender": user.gender,
            "num_of_item": numOfProducts
        }
        orderId = self._orderRepository.createOrder(transaction, createOrderSettings)
        self._orderItemRepository.createOrderItems(transaction, orderId, user.id, orderedProducts)
        return orderId

    def createNewTransaction(self):
        return self._orderRepository.createNewTransaction()
