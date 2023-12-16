from dto.User import User
from dto.Event import Event
from dto.NoneUser import NoneUser

from repository.UserRepository import UserRepository
from repository.EventRepository import EventRepository

from forms.AddUserForm import AddUserForm

from service.Common import getPaginationObject, handleLimitAndOffset

import string
import random
import datetime
import subprocess


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
        result["orders"], _ = self.orderService.getAllAndCount({"user_id": id})
        result["events"] = self.getAllEvents({"user_id": id})
        return result

    def eventDetailPage(self, id: int) -> dict:
        result = dict()
        result["event"] = self.eventsFindById(id)
        return result

    def signUpPage(self, method, form) -> int:
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = AddUserForm(self)
        else:
            form = AddUserForm(self, form)

            if form.validate_on_submit():
                user = form.data
                missing = self.generatorForForms()
                for i,j in missing.items():
                    user[i] = j
                result["submitted_and_valid"] = True
                result["id"] = self.addUser(user)
                result["flash"].append(("User registered successfully", "success"))

            else:
                result["submitted_and_valid"] = False
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    def addUser(self, user: dict) -> int:
        return self.userRepository.addUser(user)

    def deleteUserPage(self, id: int) -> dict:
        result = dict()
        result["id"] = self.deleteUser(id)
        result["flash"] = [("User deleted successfully", "success")]
        return result
    
    # SERVICE METHODS
    def findById(self, id: int) -> User:
        return User(self.userRepository.findById(id))

    def eventsFindById(self, id: int) -> Event:
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
    
    def findByEmail(self, mail) -> [User]: 
    # If email doesnt exists in the database
    # DTO makes the app crash. Because this function returns None.
        if self.userRepository.findByEmail(mail) == None:
            return NoneUser()
        else:
            return User(self.userRepository.findByEmail(mail))

    def deleteUser(self, id: int) -> int:
        return self.userRepository.deleteUserById(id)

    def sessionIdGenerator(self,chars= string.ascii_lowercase + string.digits) -> str:
        # 8 - 4 - 4 - 1
        first = ''.join(random.choice(chars) for _ in range(8))
        second = ''.join(random.choice(chars) for _ in range(4))
        third = ''.join(random.choice(chars) for _ in range(4))
        last = ''.join(random.choice(chars) for _ in range(1))
        return first + '-' + second + '-' + third + '-' + last
    
    def generatorForForms(self) -> dict:
        location = subprocess.run(args = ["curl", "ipinfo.io/loc"], universal_newlines=False, stdout=subprocess.PIPE)
        output = location.stdout.decode('utf-8')
        loc = [output[0:7],output[8:15]]
        sources = ["Search","Display","Facebook","Email"]
        latitude = loc[0]
        longitude = loc[1]
        traffic_source = random.choice(sources)
        created_at = datetime.datetime.now()
        missing = {"latitude" : latitude,
                   "longitude" : longitude,
                   "traffic_source" : traffic_source,
                   "created_at" : str(created_at)}
        return missing

