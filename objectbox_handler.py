import objectbox
from models.client import Client
from models.relation import Relation
from models.date import Date

model = objectbox.Model()
model.entity(Client, last_property_id=objectbox.model.IdUid(9, 1009))
model.entity(Relation, last_property_id=objectbox.model.IdUid(10, 2010))
model.entity(Date, last_property_id=objectbox.model.IdUid(4, 3004))
model.last_entity_id = objectbox.model.IdUid(3, 3)

ob = objectbox.Builder().model(model).directory("db").build()