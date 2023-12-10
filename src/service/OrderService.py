from repository.OrderRepository import OrderRepository
from repository.OrderItemRepository import OrderItemRepository
from dto.Order import Order
from dto.User import User
from service.Common import getPaginationObject, handleLimitAndOffset


class OrderService:
    def __init__(self, orderRepository: OrderRepository,
                 orderItemRepository: OrderItemRepository) -> None:
        self.orderRepository = orderRepository
        self.orderItemRepository = orderItemRepository
        self.userService = None

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
