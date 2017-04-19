
MAIN=main.py

install-tools:
	pip install Jinja2 Flask Whoosh pymongo python-dotenv lxml requests python-dateutil
	cp ./server/config/.env.template ./server/config/.env

install: install-tools

run-db-import:
	python $(MAIN) --import

db: run-db-import

build-index:
	python $(MAIN) --build

index: build-index

run-server:
	python $(MAIN) --server

server: run-server

test-code: 
	python server/searchers/tests.py

test: test-code

get-stats:
	python statistics/automation.py

stats: get-stats

all: db index server