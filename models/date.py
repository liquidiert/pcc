from objectbox.model import *

@Entity(id=3, uid=3)
class Date:
    id = Id(id=1, uid=3001)
    title = Property(str, id=2, uid=3002)
    notes = Property(str, id=3, uid=3003)
    # simple date representation to connect date entry with date card
    date = Property(str, id=4, uid=3004)