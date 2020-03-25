
from starwars.models import (
    ModelFilm, ModelPeople, ModelPlanet,
    ModelSpecies, ModelVehicle, ModelStarship,
)
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

field_filters = ['eq', 'ilike', 'like','contains']

class PeoplesFilter(FilterSet):
    class Meta:
        model = ModelPeople
        fields = {'name': field_filters}

class PlanetsFilter(FilterSet):
    class Meta:
        model = ModelPlanet
        fields = {'name': field_filters}

class SpeciesFilter(FilterSet):
    class Meta:
        model = ModelSpecies
        fields = {'name': field_filters, 'language': field_filters}
class FilmFilter(FilterSet):
    class Meta:
        model = ModelFilm
        fields = {'episode_id': field_filters}
class VehicleFilter(FilterSet):
    class Meta:
        model = ModelVehicle
        fields = {'name': field_filters}
class StarshipFilter(FilterSet):
    class Meta:
        model = ModelStarship
        fields = {'name': field_filters}

class ConnectionFilter(FilterableConnectionField):
    filters = {ModelPeople: PeoplesFilter(), ModelPlanet: PlanetsFilter(), ModelSpecies: SpeciesFilter(), ModelFilm: FilmFilter(), ModelVehicle: VehicleFilter(), ModelStarship: StarshipFilter()}