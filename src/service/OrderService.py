from repository.OrderRepository import OrderRepository
from repository.OrderItemRepository import OrderItemRepository
from dto.Order import Order
from dto.User import User

class OrderService:
    def __init__(self, orderRepository: OrderRepository,
                 orderItemRepository: OrderItemRepository) -> None:
        self.orderRepository = orderRepository
        self.orderItemRepository = orderItemRepository
        self.userService = None

    # PAGE METHODS
    def ordersPage(self, querySettings: dict) -> dict:
        result = dict()
        result["orders"] = self.getAll(querySettings)
        result["statusItems"] = self.getDistinctStatus()
        result["genderItems"] = self.getDistinctGender()
        return result

    def orderDetailPage(self, id: int):
        result = dict()
        result["order"] = self.findById(id)
        user_id = result["order"].user_id
        result["user"] = self.userService.findById(user_id)
        return result

    # SERVICE METHODS
    def getAll(self, settings: dict) -> [Order]:
        if "limit" not in settings:
            settings["limit"] = 20
        if "p" in settings:
            p = int(settings["p"])
            settings["offset"] = (p - 1) * settings["limit"]
        return [Order(o) for o in self.orderRepository.getAll(**settings)]

    def findById(self, id: int) -> Order:
        return Order(self.orderRepository.findById(id))

    def getDistinctStatus(self) -> [str]:
        return [s[0] for s in self.orderRepository.getDistinctStatus()]

    def getDistinctGender(self) -> [str]:
        return [g[0] for g in self.orderRepository.getDistinctGender()]
