
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from state_seeder import StateSeeder
from pymongo import MongoClient, TEXT
import urllib
import os

class YelpImporter(object):
    def __init__(self, db):
        self.__db = db
        self.__auth = Oauth1Authenticator(
            consumer_key="REiAz8Bdo4ZDdqoSeZ_CHw",
            consumer_secret="TTbM3viyQyvT4ED4uEpPZEIgbXY",
            token="gdFMM-VX3R6nFblRMTFJj2cXELQxVFAI",
            token_secret="qaTy_1Y1PRVMfjLS4HaDy2HWuwk"
        )

    def __insertRestaurantsForCity(self, restaurants):
        insertedIds = self.__db.restaurants.insert_many(restaurants)
        self.__db.restaurants.create_index([
            ('Name', TEXT),
            ('City', TEXT),
            ('URL', TEXT),
            ('Rating', TEXT),
            ('State.name', TEXT),], default_language='english')

    def __buildRestaurant(self, city, state, business):
        result = {
            "Name" : business.name,
            "City" : city,
            "URL" : business.url,
            "Rating" : business.rating
        }

        if state != None:
            result["State"] = state
        return result

    def __reset(self):
        self.__db.restaurants.drop()

    def __import(self):
        client = Client(self.__auth)
        params = {
            'term': 'food',
            'limit' : 20,
        }

        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "city_names.txt")
        
        with open(file) as f:
            lines = f.readlines()

        states = StateSeeder()
        submissionList = []

        for city in lines:
            print "Searching for " + city
            locationParam = city.strip() + ", USA"
            results = client.search(locationParam, **params)
            state = states.lookupState(results.businesses[0].location.state_code)
            mapped = map(lambda (item): self.__buildRestaurant(city.strip(), state, item), results.businesses)
            submissionList.append(mapped)

        for item in submissionList:
            self.__insertRestaurantsForCity(item)
        print "DONE"

    def import_data(self):
        self.__reset()
        self.__import()
