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
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
]
tests_require = [
    "pytest>=5.3,<6",
    "pytest-benchmark>=3.2,<4",
    "pytest-cov>=2.8,<3",
    "pytest-mock>=2,<3",
    "pytest-asyncio>=0.10,<2",
    "snapshottest>=0.5,<1",
    "coveralls>=1.11,<2",
    "promise>=2.3,<3",
    "mock>=4.0,<5",
    "pytz==2019.3",
    "iso8601>=0.1,<2",
]
setup(
    name='starwars',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
        'test': tests_require
    },
    entry_points={
        'paste.app_factory': [
            'main = starwars:main'
        ],   
        'console_scripts': [
            'initialize_api_db=starwars.scripts.initialize_db:main',
        ],
    }
)