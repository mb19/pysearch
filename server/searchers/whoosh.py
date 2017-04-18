
from base import IndexSearcher
from ..index_builder.indexes import IndexManager

class WhooshSearch(IndexSearcher):

	def __init__(self, index):
		self.__indexName = index

	def search(self, text):
		manager = IndexManager(self.__indexName, None)
		results = manager.search(text)
		return results