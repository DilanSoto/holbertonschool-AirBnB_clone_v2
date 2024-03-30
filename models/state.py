
#!/usr/bin/python3
"""Defines the State class."""
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")
    @property
    def cities(self):
        city_list = []
        for city in list(models.storage.all(City).values()):
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
    