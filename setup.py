from setuptools import setup

requires = [
    'pyramid',
    'waitress',
    'pyramid_tm',
    'pyramid_sqlalchemy',
    'transaction',
    'psycopg2',
    'zope.sqlalchemy',
    'pyramid_retry',
    'graphene',
    'graphene_sqlalchemy',
    'requests',
    'webob_graphql',
    'graphene_sqlalchemy_filter'
]

setup(
    name='starwars',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = starwars:main'
        ],   
        'console_scripts': [
            'initialize_api_db=starwars.scripts.initialize_db:main',
        ],
    }
)