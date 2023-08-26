import objectbox
from models.client import Client
from models.relation import Relation

model = objectbox.Model()
model.entity(Client, last_property_id=objectbox.model.IdUid(9, 1009))
model.entity(Relation, last_property_id=objectbox.model.IdUid(9, 2009))
model.last_entity_id = objectbox.model.IdUid(2, 2)

ob = objectbox.Builder().model(model).directory("db").build()