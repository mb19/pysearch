
import sys, os

from indexes import SchemaBuilder, IndexManager
import json
import os
import argparse
import datetime

class Builder(object):
	def __main(self, db, indexName):
		manager = IndexManager(indexName, db)

		# Build index with the specified name
		print "Building index..."
		# Now build the index
		manager.build()
		print "Done building index."

	def build(self, db, indexName):
		return self.__main(db, indexName)

