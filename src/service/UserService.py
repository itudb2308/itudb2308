from dto.User import User
from repository.UserRepository import UserRepository

class UserService:
    def __init__(self, connection) -> None:
        self.repository = UserRepository(connection)

    # PAGE METHODS
    def usersPage(self, settings: dict) -> dict:
        result = dict()
        result["users"] = self.getAll(settings)
        result["countryItems"] = self.getDistinctCountry()
        return result

    def userDetailPage(self, id: int) -> dict:
        result = dict()
        result["user"] = self.findById(id)
        return result

    # SERVICE METHODS
    def findById(self, id: int) -> User:
        return User(self.repository.findById(id))

    def getAll(self, settings: dict) -> [User]:
        if "limit" not in settings:
            settings["limit"] = 20
        if "p" in settings:
            p = int(settings["p"])
            settings["offset"] = (p - 1) * settings["limit"]
        return [User(u) for u in self.repository.getAll(**settings)]

    def getDistinctCountry(self) -> [str]:
        return [c[0] for c in self.repository.getDistinctCountry()]