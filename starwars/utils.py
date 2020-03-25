import os
import re
import sys
import json
import requests
import fileinput

from .models import (
    ModelFilm, ModelPeople, ModelPlanet,
    ModelSpecies, ModelVehicle, ModelStarship
)

resources = ['planets', 'films', 'people',
             'species', 'starships', 'vehicles']
resource_map = {'planets': 'ModelPlanet', 'films': 'ModelFilm',
                'people': 'ModelPeople', 'species': 'ModelSpecies',
                'starships': 'ModelStarship', 'vehicles': 'ModelVehicle'}


def load_swapi_data(db_session):
    for resource in resources:
        #print(resource)
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures', f'{resource}.json')) as f:
            data = json.load(f)
            for rec in data:
                res_obj = eval(resource_map[resource] + '()')
                obj_fields = vars(eval(resource_map[resource]))
                for field in rec:
                    if field in obj_fields:
                        setattr(res_obj, field, rec[field])
                db_session.add(res_obj)
            db_session.commit()


def set_rel_swapi_data(db_session):
    # Handling relationships for ModelFilms
    for resource in ['planets', 'people', 'species', 'starships', 'vehicles']:
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures', f'{resource}.json')) as f:
            data = json.load(f)
            for rec in data:
                if 'films' in rec:
                    parent = eval(f'db_session.query({resource_map[resource]})\
                                  .filter_by(url_id={rec["url_id"]}).first()')
                    for film_id in rec['films']:
                        child = db_session.query(ModelFilm)\
                                          .filter_by(url_id=film_id).first()
                        parent.film_list.append(child)
            db_session.commit()

    # Handling relationships for ModelPeople
    for resource in ['species', 'starships', 'vehicles']:
        if resource == 'species':
            field = 'people'
        else:
            field = 'pilots'

        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures', f'{resource}.json')) as f:
            data = json.load(f)
            for rec in data:
                if field in rec:
                    parent = eval(f'db_session.query({resource_map[resource]})\
                                  .filter_by(url_id={rec["url_id"]}).first()')
                    for people_id in rec[field]:
                        child = db_session.query(ModelPeople)\
                                          .filter_by(url_id=people_id).first()
                        if field == 'people':
                            parent.people_list.append(child)
                        else:
                            parent.pilot_list.append(child)
            db_session.commit()