ADMIN_NOT_AUTHORIZED = "Not authorized"


def adminAuth(session: dict):
    user = session.get("user")
    if user != "admin":
        raise Exception(ADMIN_NOT_AUTHORIZED)
