class Order:
    def __init__(self, data) -> None:
        self.id = data[0]
        self.user_id = data[1]
        self.status = data[2]
        self.gender = data[3]
        self.created_at = data[4]
        self.returned_at = data[5]
        self.shipped_at = data[6]
        self.delivered_at = data[7]
        self.num_of_items = data[8]
        if len(data) > 9:
            self.customer_name = data[9]
