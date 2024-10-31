

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
    missions_by_target_industry = graphene.List(Mission, target_industry=graphene.String(required=True))
    target_results_by_target_type_id = graphene.List(Mission, target_type_id=graphene.Int(required=True))

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

    def resolve_missions_by_target_industry(self, info, target_industry):
        return db_session.query(MissionModel).join(
            MissionModel.targets
        ).filter(
            TargetModel.target_industry == target_industry.strip()
        ).all()

    # def resolve_target_results_by_target_type_id(self, info, target_type_id):
    #     return db_session.query(MissionModel.aircraft_returned, MissionModel.aircraft_failed).join(
    #         MissionModel.targets
    #     ).filter(
    #         TargetModel.target_type_id == target_type_id
    #     ).all()




# Mutations

class AddMission(graphene.Mutation):
    class Arguments:
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float(required=True)
        attacking_aircraft = graphene.Float(required=True)
        bombing_aircraft = graphene.Float(required=True)
        aircraft_returned = graphene.Float(required=True)
        aircraft_failed = graphene.Float(required=True)
        aircraft_lost = graphene.Float(required=True)

    mission = graphene.Field(lambda: MissionModel)

    def mutate(self, info, mission_date, airborne_aircraft, attacking_aircraft,
               bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_lost):
        new_mission = MissionModel(mission_date=mission_date,
                                   airborne_aircraft=airborne_aircraft,
                                   attacking_aircraft=attacking_aircraft,
                                   bombing_aircraft=bombing_aircraft,
                                   aircraft_returned=aircraft_returned,
                                   aircraft_failed=aircraft_failed,
                                   aircraft_lost=aircraft_lost
                                   )
        db_session.add(new_mission)
        db_session.commit()
        return AddMission(mission=new_mission)


class AddTarget(graphene.Mutation):
    class Arguments:
        target_industry = graphene.String(required=True)
        target_priority = graphene.Int(required=True)  # Format: 'YYYY-MM-DD'
        mission_id = graphene.Int(required=True)

    target = graphene.Field(lambda: TargetModel)

    def mutate(self, info, target_industry, target_priority, mission_id):
        new_target = TargetModel(target_industry=target_industry,
                                 target_priority=target_priority,
                                 mission_id=mission_id)
        db_session.add(new_target)
        db_session.commit()
        return AddTarget(target=new_target)


class DeleteMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, mission_id):
        mission = db_session.query(MissionModel).get(mission_id)
        if not mission:
            return DeleteMission(ok=False)
        db_session.delete(mission)
        db_session.commit()
        return DeleteMission(ok=True)



class Mutation(graphene.ObjectType):
    add_mission = AddMission.Field()
    add_target = AddTarget.Field()








schema = graphene.Schema(query=Query, mutation=Mutation)