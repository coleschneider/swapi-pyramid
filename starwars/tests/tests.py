from .db import db_session
from graphene.test import Client
from starwars.schema import schema

def test_all_people(snapshot):
    """Testing the schema for fetching all people"""
    client = Client(schema)
    snapshot.assert_match(client.execute('''
    {
        allPeople {
            edges {
                node {
                        id
                        name
                    }
                }
            }
        }
    '''))

def test_all_people_filter(snapshot):
    """Testing the schema for fetching all people with a filter"""
    client = Client(schema)
    snapshot.assert_match(client.execute('''
    {
        allPeople(filters: {name: "Darth Vader"}) {
            edges {
            node {
                id
                name
            }
            }
        }
        }
    '''))