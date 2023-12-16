from math import ceil

from dto.Transaction import Transaction


def getPaginationObject(count: int, settings: dict) -> dict:
    result = {
        "count": count,
        "p": settings["p"] if "p" in settings else 1,
        "limit": int(settings["limit"]) if "limit" in settings else 20,
    }
    result["maxPage"] = ceil(result["count"] / result["limit"])
    return result


def handleLimitAndOffset(settings: dict) -> dict:
    if "limit" not in settings:
        settings["limit"] = 20
    if "p" in settings:
        p = int(settings["p"])
        limit = int(settings["limit"])
        settings["offset"] = (p - 1) * limit
    return settings


def transactional(func):
    def wrapper(*args, **kwargs):
        # Code to be executed before the original function is called
        print("\nExecuting code before the function")

        print(args, kwargs)
        if "transaction" not in kwargs:
            kwargs["transaction"]: Transaction = args[0].createNewTransaction()

        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e.args[0])
            kwargs["transaction"].rollback()
        finally:
            kwargs["transaction"].commit()

        # Code to be executed after the original function is called
        print("Executing code after the function\n")

        return result

    return wrapper
