from repository.BaseRepository import BaseRepository

class ProductsRepository(BaseRepository):

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
            queryArguments["where"] =queryArguments["where"] + f" P.name = '{kwargs['name']}' "
        
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

        if "order_by" in kwargs.keys() and kwargs["order_by"] != "":
            columnName = kwargs["order_by"]["columnName"]
            ascOrDesc = "ASC" if kwargs["order_by"]["ascending"] else "DESC"
            queryArguments["order_by"] = f" ORDER BY P.{columnName} {ascOrDesc}"

        query = query.format(**queryArguments)

        print(f"query: {query}")
        self.cursor.execute(query)
        return self.cursor.fetchall()