from django.db import models

# Create your models here.
import datetime #<- will be used to set default dates on models
from imgscaler.meta import Base, get_session #<- we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     #<- will provide Unicode field
    UnicodeText, #<- will provide Unicode text field
    DateTime,    #<- time abstraction field
)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    orig_name = Column(Unicode(500), nullable=False)
    orig_content = Column(Unicode(500), nullable=False)
    resized_one = Column(Unicode(500), nullable=True)
    resized_two = Column(Unicode(500), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)