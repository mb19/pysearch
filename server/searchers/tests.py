from base import SearchResult

class Tester(object):
	def __init__(self, topReturned, totalReturned):
		self.top = topReturned
		self.total_returned = totalReturned

	def count(self, totalRelevant=False):
		if not totalRelevant:
			return self.total_returned
		return self.top

def precision_test():
	testValues = Tester(10, 0)
	result = SearchResult(testValues)
	calc = result.calculate_precision(5)
	assert(calc == 0.5)

def recall_test():
	testValues = Tester(0, 20)
	result = SearchResult(testValues)
	calc = result.calculate_recall(5)
	assert(calc == 0.25)

def f_measure_test():
	testValues = Tester(20, 60)
	result = SearchResult(testValues)
	calc = result.calculate_f_measure(15)
	assert(calc == 0.375)

precision_test()
recall_test()
f_measure_test()