
# Whoosh imports
from whoosh.fields import Schema, TEXT, NUMERIC, DATETIME, ID
from whoosh.index import create_in, open_dir
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring

# MongoDB imports
from bson.objectid import ObjectId

# System imports
import os.path
import datetime

class QueryResults(object):
	""" Contains the query time and the documents that were returned. """

	def __init__(self, queryResult, table):

		self.documents = []
		""" The list of documents returned by the search. """
		for i in range(0, queryResult.scored_length()):
			doc = queryResult[i].fields()
			score = queryResult.score(i)

			if doc['prop6'] == table:
				self.documents.append({ 'score': score, 'document': doc })

		self.time = queryResult.runtime
		""" The total query time. This excludes mapping done by this code. """

class SchemaBuilder(object):
	""" Provides a way to build a normalized schema for any document type. """

	def build_index_schema(self):
		""" Builds a schema based on the proeprties of a given document. """

		params = {
			"prop1": TEXT(analyzer=StemmingAnalyzer(), stored=True),
			"prop2": TEXT(analyzer=StemmingAnalyzer(), stored=True),
			"prop3": TEXT(analyzer=StemmingAnalyzer(), stored=True),
			"prop4": TEXT(analyzer=StemmingAnalyzer(), stored=True),
			"prop5": TEXT(analyzer=StemmingAnalyzer(), stored=True),
			"prop6": TEXT(stored=True)
		}

		return Schema(**params)

	def build_data_schema(self):
		return {
			"prop1": u'',
			"prop2": u'',
			"prop3": u'',
			"prop4": u'',
			"prop5": u''
		}


class IndexManager(object):
	def __init__(self, indexPath, db):
		self.__index_path = indexPath
		self.__db = db

	def build(self):
		""" Builds the index over all database items. """
		index = self.__get_index(self.__get_schema(), True)
		writer = index.writer()

		print "Indexing players..."
		self.__index_players(writer)
		print "Saving index..."

		print "Indexing restaruants..."
		self.__index_restaurants(writer)
		print "Saving index..."
		writer.commit()

		return index

	def search(self, text, table):
		""" Searches the index for anything containing the text. """

		schema = self.__get_schema()
		index = self.__get_index(schema, False)

		# Here we use TF-IDF because that is what our mongo search will use.

		with index.searcher(weighting=scoring.TF_IDF()) as searcher:
			query = MultifieldParser(schema.names(), schema=index.schema).parse(text)
			results = searcher.search(query)
			return QueryResults(results, table)

	def __get_index(self, full_schema, shouldClean):
		""" Creates an index if necessary and returns it. """

		if not os.path.exists(self.__index_path):
			os.mkdir(self.__index_path)
			return create_in(self.__index_path, full_schema)

		if shouldClean:
			create_in(self.__index_path, full_schema)

		return open_dir(self.__index_path)

	def __get_schema(self):
		# We use the player document because it contains the most fields.
		return SchemaBuilder().build_index_schema()

	def __index_players(self, writer):
		""" Indexes the players collection. """

		total = self.__db.players.count()
		current = 0
		for player in self.__db.players.find({}):

			document = SchemaBuilder().build_data_schema()

			document['prop1'] = unicode(player['name'])
			document['prop2'] = unicode(player['position']['name'])
			document['prop3'] = unicode(player['number'])
			document['prop4'] = unicode(player['team']['name'])
			document['prop5'] = unicode(player['url'])
			document['prop6'] = u'players'

			writer.add_document(**document)
			current += 1
			print "Players Indexed {0}/{1}".format(current, total)

	def __index_restaurants(self, writer):
		""" Indexes the restaurants collection. """

		total = self.__db.restaurants.count()
		current = 0
		for rest in self.__db.restaurants.find({}):
			document = SchemaBuilder().build_data_schema()

			document['prop1'] = unicode(rest['Name'])
			document['prop2'] = unicode(rest['Rating'])
			document['prop3'] = unicode(rest['City'])
			document['prop4'] = unicode(rest['State']['name'])
			document['prop5'] = unicode(rest['URL'])
			document['prop6'] = u'restaurants'

			writer.add_document(**document)
			current += 1
			print "Restaurants Indexed {0}/{1}".format(current, total)
