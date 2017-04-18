
INDEXER=indexer
DB_IMPORTERS=db_importers

players:
	python $(DB_IMPORTERS)/MongoNFL/main.py

food:
	python $(DB_IMPORTERS)/yelp_scraper/main.py

database: players food

index:
	python $(INDEXER)/main.py --build index

server: 
	python server.py

all: database index


