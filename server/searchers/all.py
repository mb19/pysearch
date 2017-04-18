
from whoosh import WhooshSearch
from mongo import MongoSearch
from ..config.settings import Settings

class Searcher(object):
	def __init__(self, db, indexName):
		self.whoosh = WhooshSearch(indexName)
		self.mongo = MongoSearch(db)

def build_searcher():
	settings = Settings()
	return Searcher(settings.db, "index")
	