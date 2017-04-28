
MAIN=main.py

install-tools:
	pip install -r requirements.txt

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

build-stats:
	python statistics/automation.py --build

process-stats:
	python statistics/automation.py --process

all: db index server
