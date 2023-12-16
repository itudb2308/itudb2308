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

        self.statusText = self._setStatusText()
        self.adminNextStatus = self._getNextStatus()

    def _setStatusText(self) -> str:
        def formatDate(date) -> str:
            return date.strftime('%d %B %Y, %H:%M')
        if self.returned_at:
            return f"Returned at {formatDate(self.returned_at)}"
        if self.delivered_at:
            return f"Delivered at {formatDate(self.delivered_at)}"
        if self.shipped_at:
            return f"Shipped at {formatDate(self.shipped_at)}"
        if self.created_at:
            if self.status == "Processing":
                return f"Created at {formatDate(self.created_at)}"
            else:
                return "Canceled"

    def _getNextStatus(self) -> [str]:
        if self.status == "Processing":
            return ["Cancelled", "Shipped"]
        elif self.status == "Shipped":
            return ["Complete"]
        else:
            return []
