from service.UserService import UserService
CUSTOMER_NOT_AUTHENTICATED = "Customer not authenticated"


def customerAuth(session: dict):
    userId: str = session.get("userId")
    if userId == None or not userId.isnumeric():
        raise Exception(CUSTOMER_NOT_AUTHENTICATED)
