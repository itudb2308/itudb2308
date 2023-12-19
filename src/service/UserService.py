import typing

import psycopg2.errorcodes

from dto.Transaction import Transaction
from dto.User import User
from dto.Event import Event
from repository.UserRepository import UserRepository
from repository.EventRepository import EventRepository
from forms.AddUserForm import AddUserForm
from forms.UpdateUserForm import UpdateUserForm
from service.Common import getPaginationObject, handleLimitAndOffset, transactional
from requests import get

import string
import random
import datetime
import subprocess

if typing.TYPE_CHECKING:
    from service.OrderService import OrderService


class UserService:
    def __init__(self, repositories: dict) -> None:
        self._userRepository: UserRepository = repositories["user"]
        self._eventRepository: EventRepository = repositories["event"]
        self._orderService: OrderService = None

    def setOrderService(self, orderService):
        self._orderService = orderService

    # PAGE METHODS
    @transactional
    def usersPage(self, settings: dict, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        users, count = self.getAllAndCount(transaction, settings)
        result["users"] = users
        result["pagination"] = getPaginationObject(count, settings)

        result["countryItems"] = self.getDistinctCountry(transaction)
        return result

    @transactional
    def userDetailPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["user"] = self.findById(transaction, id)
        result["orders"], _ = self._orderService.getAllAndCount(transaction, {"user_id": id})
        result["events"] = self.getAllEvents(transaction, {"user_id": id})
        return result

    @transactional
    def eventDetailPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["event"] = self.eventsFindById(transaction, id)
        return result

    @transactional
    def customerLoginPage(self, mail, **kwargs) -> User:
        transaction = kwargs["transaction"]
        return self.findByEmail(transaction, mail)

    @transactional
    def signUpPage(self, method, form, **kwargs) -> int:
        transaction = kwargs["transaction"]
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            result["submitted_and_valid"] = False
            result["form"] = AddUserForm(self, transaction)
        elif method == "POST":
            form = AddUserForm(self, transaction, form)

            try:
                if not form.validate_on_submit():
                    raise Exception("Form data is invalid")

                user = form.data
                missing = self.generatorForForms()
                for i, j in missing.items():
                    user[i] = j
                result["submitted_and_valid"] = True
                try:
                    result["id"] = self.addUser(transaction, user)
                except psycopg2.IntegrityError as e:
                    raise Exception("User exists with given email")
                result["flash"].append(("User registered successfully", "success"))
            except Exception as e:
                result["submitted_and_valid"] = False
                result["flash"].append((e.args[0], "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    @transactional
    def updateUserPage(self, method, form, id, **kwargs) -> int:
        transaction = kwargs["transaction"]
        result = {"submitted_and_valid": False, "flash": [], "form": None}

        if method == "GET":
            user = self.findById(transaction, id).toDict()
            result["form"] = UpdateUserForm(self, transaction, user)
        else:
            form = UpdateUserForm(self, transaction, form)

            if form.validate_on_submit():
                user = form.data
                user["id"] = id
                id = self._userRepository.updateUser(transaction, user)
                result["submitted_and_valid"] = True
                result["flash"].append(("User profile updated.", "success"))

            else:
                result["flash"].append(("Form data is invalid", "danger"))
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        result["flash"].append((f"{fieldName}: {err}", "danger"))
                result["form"] = form
        return result

    @transactional
    def deleteUserPage(self, id: int, **kwargs) -> dict:
        transaction = kwargs["transaction"]
        result = dict()
        result["id"] = self.deleteUser(transaction, id)
        result["flash"] = [("User deleted successfully", "success")]
        return result

    @transactional
    def addEvent(self, session, **kwargs):
        transaction = kwargs["transaction"]
        return self._addEvent(transaction, session)

    @transactional
    def deleteEventPage(self, id: int, **kwargs):
        transaction = kwargs["transaction"]
        self.deleteEvent(transaction, id)

    # SERVICE METHODS

    def findById(self, transaction: Transaction, id: int) -> User:
        return User(self._userRepository.findById(transaction, id))

    def eventsFindById(self, transaction: Transaction, id: int) -> Event:
        return Event(self._eventRepository.findById(transaction, id))

    def getAllAndCount(self, transaction: Transaction, settings: dict) -> ([User], int):
        settings = handleLimitAndOffset(settings)
        data = self._userRepository.getAllAndCount(transaction, **settings)
        users = [User(u) for u in data]
        count = data[0][-1] if len(data) > 1 else 0
        return users, count

    def getDistinctCountry(self, transaction: Transaction) -> [str]:
        return [c[0] for c in self._userRepository.getDistinctCountry(transaction)]

    def getAllEvents(self, transaction: Transaction, settings: dict) -> [Event]:
        if "limit" not in settings:
            settings["limit"] = 20
        if "p" in settings:
            p = int(settings["p"])
            settings["offset"] = (p - 1) * settings["limit"]
        return [Event(e) for e in self._eventRepository.getAll(transaction, **settings)]

    def findByEmail(self, transaction: Transaction, mail) -> User:
        if self._userRepository.findByEmail(transaction, mail) is None:
            raise Exception("User not found")
        else:
            return User(self._userRepository.findByEmail(transaction, mail))

    def deleteUser(self, transaction: Transaction, id: int) -> int:
        return self._userRepository.deleteUserById(transaction, id)

    def addUser(self, transaction: Transaction, user: dict) -> int:
        return self._userRepository.addUser(transaction, user)

    def _addEvent(self, transaction, session, **kwargs):
        event = self.generatorForEvents(transaction, session)
        self._eventRepository.addEvent(transaction, event)

    def deleteEvent(self, transaction: Transaction, id: int):
        return self._eventRepository.deleteEventById(transaction, id)

    def sessionIdGenerator(self, chars=string.ascii_lowercase + string.digits) -> str:
        # 8 - 4 - 4 - 1
        first = ''.join(random.choice(chars) for _ in range(8))
        second = ''.join(random.choice(chars) for _ in range(4))
        third = ''.join(random.choice(chars) for _ in range(4))
        last = ''.join(random.choice(chars) for _ in range(1))
        return first + '-' + second + '-' + third + '-' + last

    def generatorForForms(self) -> dict:
        location = subprocess.run(args=["curl", "ipinfo.io/loc"], universal_newlines=False, stdout=subprocess.PIPE)
        output = location.stdout.decode('utf-8')
        loc = [output[0:7], output[8:15]]
        sources = ["Search", "Display", "Facebook", "Email", "Adwords"]
        latitude = loc[0]
        longitude = loc[1]
        traffic_source = random.choice(sources)
        created_at = datetime.datetime.now()
        missing = {"latitude": latitude,
                   "longitude": longitude,
                   "traffic_source": traffic_source,
                   "created_at": str(created_at)}
        return missing

    def generatorForEvents(self, transaction, session) -> Event:
        created_at = str(datetime.datetime.now())
        ip = get('https://api.ipify.org').text.strip()
        sources = ["Search", "Display", "Facebook", "Email", "Adwords"]
        traffic_source = random.choice(sources)
        browsers = ["IE", "Chrome", "Safari", "Mozilla"]
        browser = random.choice(browsers)
        user = self.findById(transaction, session["user_id"])
        tempUri = session["uri"].split("/")
        event_type = tempUri[1]
        print(event_type)

        event = {
            "user_id": session["user_id"],
            "sequence_number": session["sequence_number"],
            "session_id": self.sessionIdGenerator(),
            "created_at": created_at,
            "ip_address": ip,
            "city": user.city,
            "country": user.country,
            "postal_code": user.postal_code,
            "traffic_source": traffic_source,
            "browser": browser,
            "uri": session["uri"],
            "event_type": event_type
        }
        return event

    def createNewTransaction(self):
        return self._userRepository.createNewTransaction()
