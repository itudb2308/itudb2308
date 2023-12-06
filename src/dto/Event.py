class Event:
    def __init__(self,data):
        self.id = data[0]
        self.user_id = data[1]
        self.sequence_number = data[2]
        self.session_id = data[3]
        self.created_at = data[4]
        self.ip_address = data[5]
        self.city = data[6]
        self.country = data[7]
        self.postal_code = data[8]
        self.browser = data[9]
        self.traffic_source = data[10]
        self.uri = data[11]
        self.event_type = data[12]

