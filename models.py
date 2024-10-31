
from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# user_subject_relation = Table(
#     'user_subject_relation',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('subject_id', Integer, ForeignKey('subjects.id'))
# )

class MissionModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Float)
    attacking_aircraft = Column(Float)
    bombing_aircraft = Column(Float)
    aircraft_returned = Column(Float)
    aircraft_failed = Column(Float)
    aircraft_lost = Column(Float)

    # targets = relationship("TargeModel", back_populates="mission")

