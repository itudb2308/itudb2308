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