
MAIN=main.py

install-tools:
	pip install Jinja2 Flask Whoosh pymongo python-dotenv
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

all: db index server