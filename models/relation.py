from objectbox.model import *

@Entity(id=2, uid=2)
class Relation:
    id = Id(id=1, uid=2001)
    client_id = Property(int, id=2, uid=2002)
    firstname = Property(str, id=3, uid=2003)
    lastname = Property(str, id=4, uid=2004)
    
    # address props
    country = Property(str, id=5, uid=2005)
    city = Property(str, id=6, uid=2006)
    zip = Property(str, id=7, uid=2007)
    street = Property(str, id=8, uid=2008)
    number = Property(str, id=9, uid=2009)

    @property
    def address(self):
        return f"{self.street} {self.number}, {self.city} {self.zip}, {self.country}"
    
    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"