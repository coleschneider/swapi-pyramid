from pyramid.config import Configurator
from pyramid.response import Response
from pyramid_sqlalchemy import metadata

def main(global_config, **settings):
    # Settings
    
    
    config = Configurator(settings=settings)

    config.include('.routes')
    config.include('.models')
    config.scan()
    config.include('pyramid_sqlalchemy')
    metadata.create_all()
    
    return config.make_wsgi_app()
