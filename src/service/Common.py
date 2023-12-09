from math import ceil

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
