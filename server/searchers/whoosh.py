
from base import IndexSearcher
import urllib
from ..index_builder.indexes import IndexManager

class WhooshSearch(IndexSearcher):

	def __init__(self, index):
		self.__indexName = index

	def search(self, text, table):
		manager = IndexManager(self.__indexName, None)
		results = manager.search(text, table)

		# loop over results to url encode url for navigation.
		for doc in results.documents:
			doc['document']['prop5'] = urllib.quote_plus(doc['document']['prop5'])

		return results