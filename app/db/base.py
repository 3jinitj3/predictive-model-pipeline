from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# Establish sqlalchemy ORM for databes table mapping for CRUD operations.
class Base(DeclarativeBase, MappedAsDataclass):
    pass

# future use of mappedasdataclass return {feild: getattr(model, field) for field in model__dataclass_fields__}
# you can map data to dict for report or accepting values.


