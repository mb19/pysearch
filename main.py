
from db_importers.MongoNFL.importer import NFLImporter
from db_importers.yelp_scraper.importer import YelpImporter

from server.index_builder.main import Builder

from server.main import Server
from server.config.settings import Settings

import argparse

class App(object):

	indexName = "index"

	def __settings(self):
		return Settings()

	def build_index(self):
		return Builder().build(self.__settings().db, self.indexName)

	def import_database(self):
		settings = self.__settings()

		# Import NFL first
		nfl = NFLImporter(settings.db)
		nfl.import_data()

		# Then do yelp
		yelpData = YelpImporter(settings.db)
		yelpData.import_data()

	def run_server(self):
		server = Server()
		server.run(True)

def get_args():
	parser = argparse.ArgumentParser(description='Performs various tasks')
	parser.add_argument('--build', action='store_true', help='rebuilds the index')
	parser.add_argument('--import', action='store_true', help='scrapes, crawls, and updates the database.')
	parser.add_argument('--server', action='store_true', help='runs the server')
	return vars(parser.parse_args())
	
if __name__ == "__main__":
	args = get_args()
	app = App()
	if args['build']:
		app.build_index()
	elif args['import']:
		app.import_database()
	elif args['server']:
		app.run_server()
