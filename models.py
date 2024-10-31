
from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MissionModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Numeric(10, 2))
    attacking_aircraft = Column(Numeric(10, 2))
    bombing_aircraft = Column(Numeric(10, 2))
    aircraft_returned = Column(Numeric(10, 2))
    aircraft_failed = Column(Numeric(10, 2))
    aircraft_lost = Column(Numeric(10, 2))

    targets = relationship("TargetModel", back_populates="mission")


class CityModel(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    country_id  = Column(Integer, ForeignKey('countries.country_id'))
    latitude = Column(Numeric(10, 2))
    longitude = Column(Numeric(10, 2))

    country = relationship("CountryModel", back_populates="cities")
    targets = relationship("TargetModel", back_populates="city")


class CountryModel(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)

    cities = relationship("CityModel", back_populates="country")


class TargetTypeModel(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    targets = relationship("TargetModel", back_populates="target_type")



class TargetModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    target_industry = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    target_type_id = Column(Integer, ForeignKey('targettypes.target_type_id'))
    target_priority = Column(Integer)

    mission = relationship("MissionModel", back_populates="targets")
    city = relationship("CityModel", back_populates="targets")
    target_type = relationship("TargetTypeModel", back_populates="targets")








