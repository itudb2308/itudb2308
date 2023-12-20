from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository
import hashlib  # for generating sku


class ProductRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)
        self.defaultArguments = {
            "where": "",
            "order_by": "ORDER BY P.id ASC",
            "limit": 20,
            "offset": 0
        }

    def abbreviate(self, text):
        return text[:3].upper()

    def encode_number(self, number):
        return format(int(number), 'X')

    def generateSku(self, product: dict):

        category = product['category']
        brand = product['brand']
        department = product['department']

        category_abbr = self.abbreviate(category)
        brand_abbr = self.abbreviate(brand)
        department_abbr = self.abbreviate(department)

        # Encode numeric fields
        cost_encoded = self.encode_number(product['cost'])
        retail_price_encoded = self.encode_number(product['retail_price'])

        # Combine fields
        combined = f"{category_abbr}{brand_abbr}{department_abbr}{cost_encoded}{retail_price_encoded}{product['name']}"

        # Hash the combined string and take the first 32 characters
        sku_hash = hashlib.sha256(combined.encode()).hexdigest()[:32]

        return sku_hash.upper()

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.PRODUCTS_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.PRODUCTS_FIND_BY_IDS)

    def getAllAndCount(self, transaction: Transaction, **kwargs):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)

        queryArguments = self.defaultArguments.copy()

        # ! Assuming all kwargs key will be the same as corresponding columns name
        if "limit" in kwargs.keys() and kwargs["limit"] != "":
            queryArguments["limit"] = kwargs["limit"]

        if "offset" in kwargs.keys() and kwargs["offset"] != "":
            queryArguments["offset"] = kwargs["offset"]
        if "id" in kwargs and kwargs["id"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.id = '{kwargs['id']}' "

        if ("costLowerBound" in kwargs) or ("costUpperBound" in kwargs):
            if "costLowerBound" in kwargs.keys() and kwargs["costLowerBound"] != "":
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.cost >= {kwargs['costLowerBound']} "
            if "costUpperBound" in kwargs.keys() and kwargs["costUpperBound"] != "":
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.cost <= {kwargs['costUpperBound']} "

        if "category" in kwargs and kwargs["category"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.category = '{kwargs['category']}' "

        if "name" in kwargs and kwargs["name"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.name ILIKE '%{kwargs['name']}%' "

        if "brand" in kwargs and kwargs["brand"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.brand = '{kwargs['brand']}' "

        if "retail_price" in kwargs and kwargs["retail_price"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.retail_price = '{kwargs['retail_price']}'"

        if ("minRetailPrice" in kwargs) or ("maxRetailPrice" in kwargs):
            if "minRetailPrice" in kwargs.keys() and kwargs["minRetailPrice"] != "":
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.retail_price >= {kwargs['minRetailPrice']} "
            if "maxRetailPrice" in kwargs.keys() and kwargs["maxRetailPrice"] != "":
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.retail_price <= {kwargs['maxRetailPrice']} "

        if "department" in kwargs and kwargs["department"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.department = '{kwargs['department']}' "

        if "sku" in kwargs and kwargs["sku"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.sku = '{kwargs['sku']}' "

        if "distribution_center_id" in kwargs and kwargs["distribution_center_id"] != "":
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.distribution_center_id = '{kwargs['distribution_center_id']}' "

        if "order_by_columnName" in kwargs.keys() and kwargs["order_by_columnName"] != "":
            columnName = kwargs["order_by_columnName"]

            # set default order direction is ascending
            if "order_direction" not in kwargs.keys() or kwargs["order_direction"] == "":
                kwargs["order_direction"] = "Ascending"

            ascOrDesc = "ASC" if kwargs["order_direction"] == "Ascending" else "DESC"
            queryArguments["order_by"] = f" ORDER BY P.{columnName} {ascOrDesc}"

        query = query.format(**queryArguments)

        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def getColumnNames(self, transaction: Transaction):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_COLUMN_NAMES
        query = self._getSqlQueryFromFile(queryFileName)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def getCategories(self, transaction: Transaction):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_CATEGORIES
        query = self._getSqlQueryFromFile(queryFileName)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    # returns the id of the newly added product
    def addProduct(self, transaction: Transaction, product: dict):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_ADD_PRODUCT
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(product)

        # generate sku for the product from products atrributes
        product['sku'] = self.generateSku(product)

        query = query.format(**product)

        transaction.cursor.execute(query, product)
        product_id = transaction.cursor.fetchone()[0]
        return product_id

    def updateProduct(self, transaction: Transaction, product: dict):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_UPDATE_PRODUCT
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(product)
        query = query.format(**product)

        transaction.cursor.execute(query, product)
        product_id = transaction.cursor.fetchone()[0]
        return product_id

    def deleteProductById(self, transaction: Transaction, id: int):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_DELETE_PRODUCT_BY_ID
        return self._deleteById(transaction, id, queryFileName)

    def getBrandNames(self, transaction: Transaction):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_BRAND_NAMES
        query = self._getSqlQueryFromFile(queryFileName)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    # retrieve all of the brands that has products in the given category and department
    def getBrandNamesByCategoryDepartment(self, transaction: Transaction, category: str, department: str):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_BRAND_NAMES_BY_CATEGORY_DEPARTMENT
        query = self._getSqlQueryFromFile(queryFileName)
        queryArguments = {"category": category, "department": department}

        self.replaceDoubleApostrophes(queryArguments)  # To avoid the Brand'name case. That ' apostrophe char creates error in SQL ---> TEST
        query = query.format(**queryArguments)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()
