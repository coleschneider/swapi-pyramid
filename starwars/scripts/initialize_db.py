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



def main(argv=sys.argv):
    # Usage and configuration
    # I.e. argv =  ['./env/bin/initialize_db', 'development.ini']
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    
    setup_logging(config_uri)
    # settings is a key, value pair of things set in development.ini
    settings = get_appsettings(config_uri)
    db_uri = settings.get('sqlalchemy.url')
    engine = create_engine(db_uri, convert_unicode=True)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')
    db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    Base.query = db_session.query_property()  # Used by graphql to execute queries

    # Make the database with schema and default data
    with transaction.manager:
        print('           *** Start Setup ***            ')
        print('           *** Creating Fixture metadata ***            ')
        Base.metadata.create_all()
        print('     ******** Loading Data *********      ')
        load_swapi_data(db_session)
        db_session.commit()
        transaction.commit()
        
        print('   ******* Set data relation *********    ')
        set_rel_swapi_data(db_session)
        db_session.commit()
        transaction.commit()
        print('************ Setup Finished **************')