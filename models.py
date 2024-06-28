from database import Base
from sqlalchemy import Column, Integer, String


class Employees(Base):
    __tablename__ = "employees"

    e_id = Column(Integer, primary_key=True, index=True)
    e_name = Column(String)
    e_pos = Column(String)
    e_sal = Column(Integer)
