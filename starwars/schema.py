import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from pyramid_sqlalchemy import Session
from starwars.models import (
    ModelFilm, ModelPeople, ModelPlanet,
    ModelSpecies, ModelVehicle, ModelStarship,
)
from graphene import Node

import graphene
from graphene import relay
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from .filters import ConnectionFilter


class Connection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return self.length

class PeopleNode(SQLAlchemyObjectType):
    class Meta:
        model = ModelPeople
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory

class PeopleConnection(Connection):
    class Meta:
        node = PeopleNode

class PlanetNode(SQLAlchemyObjectType):
    '''A large mass, planet or planetoid in the Star Wars Universe,
    at the time of 0 ABY.'''
    climates = graphene.List(graphene.String)
    terrains = graphene.List(graphene.String)

    def resolve_climates(self, info):
        return [c.strip() for c in self.climate.split(',')]

    def resolve_terrains(self, info):
        return [c.strip() for c in self.terrain.split(',')]

    class Meta:
        model = ModelPlanet
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory

class PlanetConnection(Connection):
    class Meta:
        node = PlanetNode



class SpecieNode(SQLAlchemyObjectType):
    '''A type of person or character within the Star Wars Universe.'''
    eye_colors = graphene.List(graphene.String)
    hair_colors = graphene.List(graphene.String)
    skin_colors = graphene.List(graphene.String)


    def resolve_eye_colors(self, info):
        return [c.strip() for c in self.eye_colors.split(',')]

    def resolve_hair_colors(self, info):
        return [c.strip() for c in self.hair_colors.split(',')]

    def resolve_skin_colors(self, info):
        return [c.strip() for c in self.skin_colors.split(',')]

    class Meta:
        model = ModelSpecies
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory
class SpeciesConnection(Connection):
    class Meta:
        node = SpecieNode

class FilmNode(SQLAlchemyObjectType):
    '''A Single film.'''
    producers = graphene.List(graphene.String)

    def resolve_producers(self, info):
        return [c.strip() for c in self.producer.split(',')]
    class Meta:
        model = ModelFilm
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory
class FilmConnection(Connection):
    class Meta:
        node = FilmNode

class VehicleNode(SQLAlchemyObjectType):
    '''A single transport craft that does not have hyperdrive capability'''
    manufacturers = graphene.List(graphene.String)
    def resolve_manufacturers(self, info):
        return [c.strip() for c in self.manufacturer.split(',')]
    class Meta:
        model = ModelVehicle
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory
class VehicleConnection(Connection):
    class Meta:
        node = VehicleNode

class StarshipNode(SQLAlchemyObjectType):
    '''A single transport craft that has hyperdrive capability.'''
    manufacturers = graphene.List(graphene.String)

    def resolve_manufacturers(self, info):
        return [c.strip() for c in self.manufacturer.split(',')]

    def resolve_max_atmosphering_speed(self, info):
        if self.max_atmosphering_speed == 'n/a':
            return None
        return self.max_atmosphering_speed

    class Meta:
        model = ModelStarship
        interfaces = (Node,)
        connection_field_factory = ConnectionFilter.factory
        model = ModelStarship
        

class StarshipConnection(Connection):
    class Meta:
        node = StarshipNode
class Query(graphene.ObjectType):
    all_people = ConnectionFilter(PeopleConnection)
    all_planets = ConnectionFilter(PlanetConnection)
    all_films = ConnectionFilter(FilmConnection)
    all_species = ConnectionFilter(SpeciesConnection)
    all_vehicles = ConnectionFilter(VehicleConnection)
    all_starships = ConnectionFilter(StarshipConnection)
    
    node = relay.Node.Field()
    person = relay.Node.Field(PeopleNode)
    planet = relay.Node.Field(PlanetNode)
    film = relay.Node.Field(FilmNode)
    starship = relay.Node.Field(StarshipNode)
    specie = relay.Node.Field(SpecieNode)
    vehicle = relay.Node.Field(VehicleNode)
    viewer = graphene.Field(lambda: Query)

    def resolve_viewer(self, info):
        return self


schema = graphene.Schema(query=Query)

