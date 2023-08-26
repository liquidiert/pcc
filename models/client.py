from objectbox.model import *
from datetime import datetime

@Entity(id=1, uid=1)
class Client:
    id = Id(id=1, uid=1001)
    firstname = Property(str, id=2, uid=1002)
    lastname = Property(str, id=3, uid=1003)
    
    # address props
    country = Property(str, id=4, uid=1004)
    city = Property(str, id=5, uid=1005)
    zip = Property(str, id=6, uid=1006)
    street = Property(str, id=7, uid=1007)
    number = Property(str, id=8, uid=1008)

    birthdate = Property(int, id=9, uid=1009)

    @property
    def address(self):
        return f"{self.street} {self.number}, {self.city} {self.zip}, {self.country}"
    
    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    @property
    def human_readable_birthdate(self):
        return datetime.fromtimestamp(self.birthdate).strftime("%d.%m.%Y")