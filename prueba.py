from database.config import Base
from models import user, medic  # los que correspondan

print(Base.metadata.tables.keys())
