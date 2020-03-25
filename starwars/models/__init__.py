from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
# from .models import People,  # flake8: noqa
from .models import (
    ModelFilm, ModelPeople, ModelPlanet,
    ModelSpecies, ModelVehicle, ModelStarship
)
from .metadata import Base
# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    Base.metadata.bind = engine
    factory.configure(bind=engine, expire_on_commit=False)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.
    This function will hook the session to the transaction manager which
    will take care of committing any changes.
    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.
    - When using scripts you should wrap the session in a manager yourself.
      For example::
          import transaction
          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              db_session = get_tm_session(session_factory, transaction.manager)
    """
    db_session = session_factory()
    # Base.query = db_session.query_property()  # Used by graphql to execute queries
    zope.sqlalchemy.register(
        db_session, transaction_manager=transaction_manager)
    return db_session


def includeme(config):
    """
    Initialize the model for a Pyramid app.
    Activate this setup using ``config.include('todo_list_pyramid.models')``.
    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['db_session_factory'] = session_factory

    # make request.db_session available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'db_session',
        reify=True
    )
