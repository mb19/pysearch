
from base import IndexSearcher

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

class PlayerSearch(TableSearch):

	def __normalize(self, document):
		return {
			'document': {
				'prop1': document['name'],
				'prop2': document['position']['name'],
				'prop3': document['number'],
				'prop4': document['team']['name'],
				'prop5': document['url']
			},
			'score': document['score']
		}

	def search(self, text):
		query = self.query(text)

		projection = {
			'name': 1,
			'position.name': 1,
			'number': 1,
			'team.name': 1,
			'url': 1,
			'score': {
				'$meta': 'textScore'
			}
		}

		results = self.table.find(query, projection)
		return [self.__normalize(rest) for rest in results]

class RestaurantSearch(TableSearch):

	def __normalize(self, document):
		return {
			'document': {
				'prop1': document['Name'],
				'prop2': document['Rating'],
				'prop3': document['City'],
				'prop4': document['State'],
				'prop5': document['URL']
			},
			'score': document['score']
		}

	def search(self, text):
		query = self.query(text)

		projection = {
			'Name': 1,
			'Rating': 1,
			'City': 1,
			'State': 1,
			'URL': 1,
			'score': {
				'$meta': 'textScore'
			}
		}

		results = self.table.find(query, projection)
		return [self.__normalize(rest) for rest in results]