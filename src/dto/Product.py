class Product:
    def __init__(self, data):
        self.id = data[0]
        self.cost = data[1]
        self.category = data[2]
        self.name = data[3]
        self.brand = data[4]
        self.retail_price = data[5]
        self.department = data[6]
        self.sku = data[7]
        self.distribution_center_id = data[8]
    def toDict(self):
        return {
            "id" : self.id,
            "cost" : self.cost,
            "category" : self.category,
            "name" : self.name,
            "brand" : self.brand,
            "retail_price" : self.retail_price,
            "department" : self.department,
            "sku" : self.sku,
            "distribution_center_id" : self.distribution_center_id
        }