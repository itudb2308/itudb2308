import typing

from dto.Transaction import Transaction
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
        return result
    
    @transactional
    def cartPage(self, cart: dict, **kwargs):
        transaction = kwargs["transaction"]
        productIds = [int(i) for i in cart.keys()]
        products = self._productService.findByIds(transaction, productIds)
        return products



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
        orderItems = [OrderItem(d[:11]) for d in data]
        for index, oi in enumerate(orderItems):
            oi.product = Product(data[index][11:20])
            oi.distributionCenter = DistributionCenter(data[index][20:])
        return orderItems

    def setOrderStatus(self, transaction: Transaction, id: int, orderStatus: str):
        distinctStatus = self.getDistinctStatus(transaction)
        if orderStatus not in distinctStatus:
            print("Invalid Order Status")
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

    def createNewTransaction(self):
        return self._orderRepository.createNewTransaction()
