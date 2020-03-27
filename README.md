# GraphQL SWAPI using Graphene, Pyramid, and SQLAlchemy

This is a integration example of [Graphene](http://graphene-python.org) in [Pyramid](https://trypyramid.com/).


## Structure

All the [models](./starwars/models/models.py) and [fixtures](./starwars/fixtures/) are based in the original [swapi project](https://github.com/phalt/swapi).

The schema can be found in [starwars/schema.py](./starwars/schema.py).
> For filters, SQLAlchemy doesnt support graphene filters so [graphene sql alchemy filter]([./starwars/schema.py](https://github.com/art1415926535/graphene-sqlalchemy-filter))


## Deploying locally

You can also have your own GraphQL Starwars example running on locally.
Just run the following commands and you'll be all set!

```bash
git clone git@github.com:coleschneider/swapi-pyramid.git
cd swapi-pyramid

# Create a virtual environment
python3 -m venv env && export ENV=./env

# Install the requirements
$ENV/bin/pip install -r requirements_base.txt

# Install in development mode
$ENV/bin/pip install -e .

# Initialize the database with fixtures
$ENV/bin/initialize_db development.ini

# Start server
$ENV/bin/pserve development.ini --reload
```

Visit [localhost:6543/graphql](http://localhost:6543/graphql)


## Testing


```bash

# Run tests with logging enabled
$ENV/bin/py.test ./starwars/tests/tests.py -s

# Run tests and update snapshots
$ENV/bin/py.test ./starwars/tests/tests.py -s --snapshot-update

```