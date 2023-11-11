from os.path import join as path_join


class RepositoryConstants:
    SQL_FOLDER_NAME = "sql"
    SQL_FOLDER_PATH = path_join("./src", SQL_FOLDER_NAME)

    class SQL_FILES:
        ORDER_FIND_BY_ID = "order_find_by_id.sql"
        ORDER_FIND_BY_IDS = "order_find_by_ids.sql"
        ORDER_ITEM_FIND_BY_ID = "order_item_find_by_id.sql"
        ORDER_ITEM_FIND_BY_IDS = "order_item_find_by_ids.sql"
        USER_FIND_BY_ID = "user_find_by_id.sql"
        USER_FIND_BY_IDS = "user_find_by_ids.sql"
        EVENTS_FIND_BY_ID = "events.find_by_id.sql"
        EVENTS_FIND_BY_IDS = "events_find_by_ids.sql"
