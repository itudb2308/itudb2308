from os.path import join as path_join


class RepositoryConstants:
    SQL_FOLDER_NAME = "sql"
    SQL_FOLDER_PATH = path_join("./src", SQL_FOLDER_NAME)

    class SQL_FILES:
        ORDER_FIND_BY_ID = "order_find_by_id.sql"
        ORDER_FIND_BY_IDS = "order_find_by_ids.sql"
        ORDER_GET_ALL = "order_get_all.sql"
        ORDER_ITEM_FIND_BY_ID = "order_item_find_by_id.sql"
        ORDER_ITEM_FIND_BY_IDS = "order_item_find_by_ids.sql"
        USERS_FIND_BY_ID = "users_find_by_id.sql"
        USERS_FIND_BY_IDS = "users_find_by_ids.sql"
        USERS_GET_ALL = "users_get_all.sql"
        EVENTS_FIND_BY_ID = "events_find_by_id.sql"
        EVENTS_FIND_BY_IDS = "events_find_by_ids.sql"
        DISTRIBUTION_CENTERS_FIND_BY_ID = "distribution_centers_find_by_id.sql"
        DISTRIBUTION_CENTERS_FIND_BY_IDS = "distribution_centers_find_by_ids.sql"
        INVENTORY_ITEMS_FIND_BY_ID = "inventory_items_find_by_id.sql"
        INVENTORY_ITEMS_FIND_BY_IDS = "inventory_items_find_by_ids.sql"
        PRODUCTS_FIND_BY_ID = "products_find_by_id.sql" 
        PRODUCTS_FIND_BY_IDS = "products_find_by_ids.sql" 
        PRODUCTS_GET_ALL = "products_get_all.sql"
        

