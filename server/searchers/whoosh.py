
from base import IndexSearcher, SearchResult
import urllib
from ..index_builder.indexes import IndexManager

class WhooshSearch(IndexSearcher):

	def __init__(self, index):
		self.__indexName = index

	def search(self, text, table, limit=10):
		manager = IndexManager(self.__indexName, None)
		return manager.search(text, table, limit)