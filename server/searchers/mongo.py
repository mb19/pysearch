
from base import IndexSearcher
import urllib
import pymongo

class MongoSearch(object):

	def __init__(self, db):
		self.restaurants = RestaurantSearch(db.restaurants)
		self.players = PlayerSearch(db.players)

class TableSearch(IndexSearcher):
	def __init__(self, table):
		self.table = table

	def query(self, text):
		return {
			'$text': {
				'$search': text
			}
		}

	def meta(self):
		return {
			"$meta": 'textScore'
		}

	def projection(self):
		raise NotImplementedError("Must implement to use.")

	def normalize(self, document):
		raise NotImplementedError("Must implement to use.")

	def search(self, text):
		query = self.query(text)

		projection = self.projection()

		meta = self.meta()

		results = self.table.find(query, projection).sort([('score', self.meta())]).limit(10)
		count = results.count()
		items = results.count(True)
		
		return [self.normalize(rest) for rest in results]

class PlayerSearch(TableSearch):

	def normalize(self, document):
		return {
			'document': {
				'prop1': document['name'],
				'prop2': document['position']['name'],
				'prop3': document['number'],
				'prop4': document['team']['name'],
				'prop5': urllib.quote_plus(document['url'])
			},
			'score': document['score']
		}

	def projection(self):
		return {
			'name': 1,
			'position.name': 1,
			'number': 1,
			'team.name': 1,
			'url': 1,
			'score': self.meta()
		}

class RestaurantSearch(TableSearch):

	def normalize(self, document):
		return {
			'document': {
				'prop1': document['Name'],
				'prop2': document['Rating'],
				'prop3': document['City'],
				'prop4': document['State']['abbr'],
				'prop5': urllib.quote_plus(document['URL'])
			},
			'score': document['score']
		}

	def projection(self):
		return {
			'Name': 1,
			'Rating': 1,
			'City': 1,
			'State.abbr': 1,
			'URL': 1,
			'score': self.meta()
		}
