
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
    missions_by_range_dates = graphene.List(Mission, start_date=graphene.Date(), end_date=graphene.Date())
    missions_by_country = graphene.List(Mission, country_id=graphene.Int(required=True))

    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionModel).get(id)

    def resolve_missions_by_range_dates(self, info, start_date, end_date):
        return db_session.query(MissionModel).filter(
            start_date <= MissionModel.mission_date >= end_date,
        ).all()

    # def resolve_missions_by_country(self, info, country_id):
    #     return db_session.query(MissionModel).join(
    #         TargetsModel.mission
    #     ).join(
    #         CountryModel.Tar
    #     )
    #     )





schema = graphene.Schema(query=Query)