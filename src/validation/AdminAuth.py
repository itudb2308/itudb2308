ADMIN_NOT_AUTHENTICATED = "Admin not authenticated"


def adminAuth(session: dict):
    user = session.get("user")
    if user != "admin":
        raise Exception(ADMIN_NOT_AUTHENTICATED)
