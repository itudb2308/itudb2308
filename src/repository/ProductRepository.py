from repository.BaseRepository import BaseRepository

class ProductRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)
        self.defaultArguments = {
            "where": "",
            "order_by": "ORDER BY P.id ASC",
            "limit": 20,
            "offset": 0
        }

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.PRODUCTS_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.PRODUCTS_FIND_BY_IDS)

    def getAll(self, **kwargs) : 
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)
        
        queryArguments = self.defaultArguments.copy()
        
        # ! Assuming all kwargs key will be the same as corresponding columns name 
        if "limit" in kwargs.keys() and kwargs["limit"] != "":
            queryArguments["limit"] = kwargs["limit"]

        if "offset" in kwargs.keys() and kwargs["offset"] != "":
            queryArguments["offset"] = kwargs["offset"]
        if "id" in kwargs and kwargs["id"] != "" :
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.id = '{kwargs['id']}' "
        
        if ("costLowerBound" in kwargs) or ("costUpperBound" in kwargs): 
            if "costLowerBound" in kwargs.keys() and kwargs["costLowerBound"] != "" :
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.cost >= {kwargs['costLowerBound']} "    
            if "costUpperBound" in kwargs.keys() and kwargs["costUpperBound"] != "" :
                self.handleWhereStatement(queryArguments)
                queryArguments["where"] = queryArguments["where"] + f" P.cost <= {kwargs['costUpperBound']} "    

        if "category" in kwargs and kwargs["category"] != "" : 
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.category = '{kwargs['category']}' "

        if "name" in kwargs and kwargs["name"] != "": 
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.name ILIKE '%{kwargs['name']}%' "
        
        if "brand" in kwargs and kwargs["brand"] != "" : 
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.brand = '{kwargs['brand']}' "
        
        if "retail_price" in kwargs and kwargs["retail_price"] != "" : 
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.retail_price BETWEEN {kwargs['retail_price']} - {self.floatPrecision} AND {kwargs['retail_price']} + {self.floatPrecision}"


        if "department" in kwargs and kwargs["department"] != "": 
            self.handleWhereStatement(queryArguments)
            # add requested condition
            queryArguments["where"] = queryArguments["where"] + f" P.department = '{kwargs['department']}' "
        
        if "sku" in kwargs and  kwargs["sku"] != "": 
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

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getColumnNames(self):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_COLUMN_NAMES
        query = self._getSqlQueryFromFile(queryFileName)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def getCategories(self):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_CATEGORIES
        query = self._getSqlQueryFromFile(queryFileName)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # returns the id of the newly added product
    def addProduct(self, product: dict):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_ADD_PRODUCT
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(product)
        query = query.format(**product)
        try:
            self.cursor.execute(query, product)
            self.connection.commit()
        except Exception as e:
            print(f" query: {query}")
            print(e)
            self.connection.rollback()
            raise e

        product_id = self.cursor.fetchone()[0]
        return product_id

    def updateProduct(self, product: dict):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_UPDATE_PRODUCT
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(product)
        query = query.format(**product)
        try:
            self.cursor.execute(query, product)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

        product_id = self.cursor.fetchone()[0]
        return product_id
    
    def deleteProductById(self, id: int):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_DELETE_PRODUCT_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def getBrandNames(self):
        queryFileName = self._constants.SQL_FILES.PRODUCTS_GET_BRAND_NAMES
        query = self._getSqlQueryFromFile(queryFileName)
        self.cursor.execute(query)
        return self.cursor.fetchall()
    