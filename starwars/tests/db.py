import os
import sys
import transaction
from sqlalchemy import create_engine
from pyramid.config import Configurator
from sqlalchemy.orm import scoped_session, sessionmaker
from pyramid_sqlalchemy import Session
from pyramid.paster import get_appsettings, setup_logging
from ..utils import (load_swapi_data, set_rel_swapi_data)


from starwars.models import (
    ModelFilm, ModelPeople, ModelPlanet,
    ModelSpecies, ModelVehicle, ModelStarship,
)
from starwars.models.metadata import (
    Base
)
# Takes in the ini file to determine running
def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

db_uri = 'postgresql:///starwars'
engine = create_engine(db_uri, convert_unicode=True)
Base.metadata.bind = engine


db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = db_session.query_property()  # Used by graphql to execute queries

# def setup_db():
    
    
#     # settings is a key, value pair of things set in development.ini
    
    

#     # Make the database with schema and default data
#     with transaction.manager:
#         print('           *** Start Setup ***            ')
#         print('           *** Creating Fixture metadata ***            ')
#         Base.metadata.create_all()
#         print('     ******** Loading Data *********      ')
#         load_swapi_data(db_session)
#         db_session.commit()
#         transaction.commit()
        
#         print('   ******* Set data relation *********    ')
#         set_rel_swapi_data(db_session)
#         db_session.commit()
#         transaction.commit()
#         print('************ Setup Finished **************')