import typing
from repository.OrderRepository import OrderRepository
from repository.OrderItemRepository import OrderItemRepository
from dto.Order import Order
from dto.OrderItem import OrderItem
from dto.Product import Product
from dto.DistributionCenter import DistributionCenter
from service.Common import getPaginationObject, handleLimitAndOffset

if typing.TYPE_CHECKING:
    from service.UserService import UserService


class OrderService:
    def __init__(self, repositories: dict) -> None:
        self.orderRepository: OrderRepository = repositories["order"]
        self.orderItemRepository: OrderItemRepository = repositories["orderItem"]
        self.userService: UserService = None

    # PAGE METHODS
    def ordersPage(self, querySettings: dict) -> dict:
        result = dict()
        orders, count = self.getAllAndCount(querySettings)
        result["orders"] = orders
        result["pagination"] = getPaginationObject(count, querySettings)

        result["statusItems"] = self.getDistinctStatus()
        result["genderItems"] = self.getDistinctGender()
        return result

    def orderDetailPage(self, id: int):
        result = dict()
        result["order"] = self.findById(id)
        result["orderItems"] = self.getItemDetailsByOrderId(id)
        user_id = result["order"].user_id
        result["user"] = self.userService.findById(user_id)
        return result

    # SERVICE METHODS
    def getAllAndCount(self, settings: dict) -> ([Order], int):
        settings = handleLimitAndOffset(settings)
        data = self.orderRepository.getAllAndCount(**settings)
        orders = [Order(o) for o in data]
        count = data[0][-1] if len(data) > 1 else 0
        return orders, count

    def findById(self, id: int) -> Order:
        return Order(self.orderRepository.findById(id))

    def getDistinctStatus(self) -> [str]:
        return [s[0] for s in self.orderRepository.getDistinctStatus()]

    def getDistinctGender(self) -> [str]:
        return [g[0] for g in self.orderRepository.getDistinctGender()]

    def getItemDetailsByOrderId(self, orderId: int) -> [OrderItem]:
        data = self.orderItemRepository.getItemDetailsByOrderId(orderId)
        orderItems = [OrderItem(d[:11]) for d in data]
        for index, oi in enumerate(orderItems):
            oi.product = Product(data[index][11:20])
            oi.distributionCenter = DistributionCenter(data[index][20:])
        return orderItems

    def setOrderStatus(self, id: int, orderStatus: str):
        distinctStatus = self.getDistinctStatus()
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

        self.orderRepository.setOrderStatus(querySettings)
