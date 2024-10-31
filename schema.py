from calendar import error

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime, date
from database import db_session
from models import MissionModel, CityModel, CountryModel, TargetTypeModel, TargetModel


class Mission(SQLAlchemyObjectType):
    class Meta:
        model = MissionModel
        interfaces = (graphene.relay.Node,)


class City(SQLAlchemyObjectType):
    class Meta:
        model = CityModel
        interfaces = (graphene.relay.Node,)


class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel
        interfaces = (graphene.relay.Node,)


class TargetType(SQLAlchemyObjectType):
    class Meta:
        model = TargetTypeModel
        interfaces = (graphene.relay.Node,)


class Target(SQLAlchemyObjectType):
    class Meta:
        model = TargetModel
        interfaces = (graphene.relay.Node,)






class Query(graphene.ObjectType):
    mission_by_id = graphene.Field(Mission, id=graphene.Int(required=True))
    missions_by_range_dates = graphene.List(Mission, start_date=graphene.String(required=True), end_date=graphene.String(required=True))
    missions_by_country = graphene.List(Mission, country_id=graphene.Int(required=True))

    def resolve_mission_by_id(self, info, id):
        return (db_session.query(MissionModel).join(
            MissionModel.targets
        ).get(id))

    def resolve_missions_by_range_dates(self, info, start_date, end_date):
        try:
            start_date_obj = datetime.strptime(start_date.strip(), '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date.strip(), '%Y-%m-%d').date()
        except ValueError:
            return []
        return (db_session.query(MissionModel)
                .filter(MissionModel.mission_date.between(start_date_obj, end_date_obj))
                .all())

    def resolve_missions_by_country(self, info, country_id):
        return db_session.query(MissionModel).join(
            MissionModel.targets
        ).join(
            TargetModel.city
        ).join(
            CityModel.country
        ).filter(
            CountryModel.country_id == country_id
        )





schema = graphene.Schema(query=Query)