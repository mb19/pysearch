
MAIN=main.py

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