from dto.User import User
from dto.Event import Event
from repository.UserRepository import UserRepository
from repository.EventRepository import EventRepository
from service.Common import getPaginationObject, handleLimitAndOffset

class UserService:
    def __init__(self, userRepository: UserRepository,
                 eventRepository: EventRepository) -> None:
        self.userRepository = userRepository
        self.eventRepository = eventRepository
        self.orderService = None

    # PAGE METHODS
    def usersPage(self, settings: dict) -> dict:
        result = dict()
        users, count = self.getAllAndCount(settings)
        result["users"] = users
        result["pagination"] = getPaginationObject(count, settings)

        result["countryItems"] = self.getDistinctCountry()
        return result

    def userDetailPage(self, id: int) -> dict:
        result = dict()
        result["user"] = self.findById(id)
        result["orders"], _ = self.orderService.getAllAndCount({"user_id" : id})
        result["events"] = self.getAllEvents({"user_id" : id})
        return result

    def eventDetailPage(self, id: int) -> dict:
        result = dict()
        result["event"] = self.eventsFindById(id)
        return result

    # SERVICE METHODS
    def findById(self, id: int) -> User:
        return User(self.userRepository.findById(id))

    def eventsFindById(self, id : int) -> Event:
        return Event(self.eventRepository.findById(id))

    def getAllAndCount(self, settings: dict) -> ([User], int):
        settings = handleLimitAndOffset(settings)
        data = self.userRepository.getAllAndCount(**settings)
        users = [User(u) for u in data]
        count = data[0][-1] if len(data) > 1 else 0
        return users, count

    def getDistinctCountry(self) -> [str]:
        return [c[0] for c in self.userRepository.getDistinctCountry()]

    def getAllEvents(self, settings: dict) -> [Event]:
        if "limit" not in settings:
            settings["limit"] = 20
        if "p" in settings:
            p = int(settings["p"])
            settings["offset"] = (p - 1) * settings["limit"]
        return [Event(e) for e in self.eventRepository.getAll(**settings)]
