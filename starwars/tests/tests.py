


import sys
import unittest

import unittest
import os
import transaction
from pyramid import testing
from pyramid.paster import get_appsettings
from .db import db_session
from graphene.test import Client
from starwars.schema import schema

def test_api_me(snapshot):
    """Testing the API for /me"""
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