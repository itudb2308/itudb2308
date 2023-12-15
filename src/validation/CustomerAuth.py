from service.UserService import UserService
CUSTOMER_NOT_AUTHENTICATED = "Customer not authenticated"


def customerAuth(session: dict):
    isLogged: str = session.get("user_logged_in")
    if isLogged == None or False:
        raise Exception(CUSTOMER_NOT_AUTHENTICATED)
