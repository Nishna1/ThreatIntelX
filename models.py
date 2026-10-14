from sqlalchemy import Column, Integer, String
from database import Base

class IOC(Base):
    __tablename__ = "iocs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    value = Column(String, unique=True)
    source = Column(String)
    severity = Column(String)
