
from base import IndexSearcher
from ..index_builder.indexes import IndexManager

class WhooshSearch(IndexSearcher):

	def __init__(self, index):
		self.__indexName = index

	def search(self, text):
		manager = IndexManager(self.__indexName, None)
		results = manager.search(text)
		return results

		# 	# Do search
		# 	print "Searching index..."
		# 	results = manager.search(arg['search'])
		# 	print "Done searching index."

		# 	print "==== Documents Returned in {0} s: {1} ====".format(results.time, len(results.documents))
		# 	for doc in results.documents:
		# 		if arg['expand']:
		# 			# Print everything, score and document.
		# 			print doc
		# 		else:
		# 			# Condensed vesion, only print top 5 properties.
		# 			val = doc['document']
		# 			print "{0}, {1}, {2}, {3}, {4}".format(val['prop1'], val['prop2'], val['prop3'], val['prop4'], val['prop5'])

		pass