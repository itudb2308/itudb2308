class OrderItem:
    def __init__(self, data) -> None:
        self.id = data[0]
        self.order_id = data[1]
        self.user_id = data[2]
        self.product_id = data[3]
        self.inventory_item_id = data[4]
        self.status = data[5]
        self.created_at = data[6]
        self.shipped_at = data[7]
        self.delivered_at = data[8]
        self.returned_at = data[9]
        self.sale_price = data[10]
