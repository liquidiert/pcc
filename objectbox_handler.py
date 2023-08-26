import objectbox
from models.client import Client

model = objectbox.Model()
model.entity(Client, last_property_id=objectbox.model.IdUid(9, 1009))
model.last_entity_id = objectbox.model.IdUid(1, 1)

ob = objectbox.Builder().model(model).directory("db").build()