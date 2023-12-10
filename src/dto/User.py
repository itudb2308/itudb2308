from datetime import datetime


class User:
    def __init__(self, data):
        self.id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.email = data[3]
        self.age = data[4]
        self.gender = data[5]
        self.state = data[6]
        self.street_address = data[7]
        self.postal_code = data[8]
        self.city = data[9]
        self.country = data[10]
        self.latitude = data[11]
        self.longitude = data[12]
        self.traffic_source = data[13]
        self.created_at = data[14].strftime("%d %B %Y")
        self.fullAddress = self.street_address + ", " + self.city + ", " + self.state + ", " + self.country + ", " + self.postal_code
