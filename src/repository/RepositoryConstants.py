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
        ORDER_GET_DISTINCT_STATUS = "order_get_distinct_status.sql"
        ORDER_GET_DISTINCT_GENDER = "order_get_distinct_gender.sql"
        USERS_FIND_BY_ID = "users_find_by_id.sql"
        USERS_FIND_BY_IDS = "users_find_by_ids.sql"
        USERS_GET_ALL = "users_get_all.sql"
        EVENTS_FIND_BY_ID = "events_find_by_id.sql"
        EVENTS_FIND_BY_IDS = "events_find_by_ids.sql"
        EVENTS_GET_ALL = "events_get_all.sql"
        DISTRIBUTION_CENTERS_FIND_BY_ID = "distribution_centers_find_by_id.sql"
        DISTRIBUTION_CENTERS_FIND_BY_IDS = "distribution_centers_find_by_ids.sql"
        DISTRIBUTION_CENTERS_GET_ALL = "distribution_centers_get_all.sql"
        DISTRIBUTION_CENTERS_ADD_DISTRIBUTION_CENTER = "distribution_centers_add_distribution_center.sql"
        DISTRIBUTION_CENTERS_UPDATE_DISTRIBUTION_CENTER = "distribution_centers_update_distribution_center.sql"
        DISTRIBUTION_CENTERS_DELETE_DISTRIBUTION_CENTER = "distribution_centers_delete_distribution_center.sql"
        INVENTORY_ITEMS_FIND_BY_ID = "inventory_items_find_by_id.sql"
        INVENTORY_ITEMS_FIND_BY_IDS = "inventory_items_find_by_ids.sql"
        PRODUCTS_FIND_BY_ID = "products_find_by_id.sql"
        PRODUCTS_FIND_BY_IDS = "products_find_by_ids.sql"
        PRODUCTS_GET_ALL = "products_get_all.sql"
        PRODUCTS_GET_COLUMN_NAMES = "products_get_column_names.sql"
        PRODUCTS_GET_CATEGORIES = "products_get_categories.sql"
        PRODUCTS_ADD_PRODUCT = "products_add_product.sql"
        PRODUCTS_UPDATE_PRODUCT = "products_update_product_by_id.sql"
        PRODUCTS_DELETE_PRODUCT_BY_ID = "products_delete_product_by_id.sql"
        PRODUCTS_GET_BRAND_NAMES = "products_get_brand_names.sql"
        GET_DISTINCT_COUNTRY = "get_distinct_country.sql"
