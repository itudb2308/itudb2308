class OrderItem:
    def __init__(self, data) -> None:
        self.product_id = data[0]
        self.product_name = data[1]
        self.product_brand = data[2]
        self.product_category = data[3]
        self.quantity = data[4]
        self.product_distribution_id = data[5]
        self.product_distribution_name = data[6]
        self.price = data[7]
