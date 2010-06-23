from django.db import models
from django.contrib.auth.models import User, UserManager
import sys, traceback
from parser import *
# Create your models here.


	



class Scanner(object):		
	# this class evaluates the expression on all the past data points
	# and return the indexes into the past_data set when the expression evaluates true
	
	def run(self, expression, past_data, memo=None):
		result_list = []
		for (counter, point) in enumerate(past_data):
			try:
				result = expression(past_data=past_data[:counter], latest_record=past_data[counter], memo=memo)
			except Exception as e:
				traceback.print_exc()
				result = None
	
			if result: 
				result_list.append(counter)				
		return result_list


class Query_Execution_Box(object):	
	# this class creates the execution environment by cutting the data
	# then running the scan
	def __init__(self, data, full_data=None):
		# data holds the parent (or previous) query result
		# full_data holds the raw data for reference when fluent chaining
		# if full_data is None, this implies this class instance is the root and thus data holds the full raw data
		# memo is the dictionary for memoization that must be passed to the scanner 
		self.memo = {}
		self.data = data
		self._full_data = full_data
		if full_data is None:
			self._full_data = data
		
	def __call__(self, query_string):
		parser = Parser()
 		tokenizer = Tokenizer(query_text=query_string)
 		expression = parser.parse_query(tokenizer)
		return self.exe(expression)
		
	def exe(self, expression):
		# always cut and scan from the full raw data
		formatted_data = expression.cut_data(self._full_data)
		scanner = Scanner()
		indexes = scanner.run(expression, formatted_data, self.memo)
		
		# retrieve the resulting records
		query_data = [self._full_data[index] for index in indexes]
		
		# find the intersection between the current query results and the parent query results to get the FINAL result
		query_result = self.intersection(self.data, query_data)
		return Query_Execution_Box(data=query_result, full_data=self._full_data)	
		
	def intersection(self, data1, data2):
		
		# make lists of dates for easier set operations
		data1_set = set([record[0] for record in data1])
		data2_set = set([record[0] for record in data2])		
		records_in_common = data1_set.intersection(data2_set)
		result_dates = list(records_in_common)
		result_dates.sort()
		
		# retrieve the records from data1 that corresponds to the result dates
		result = []
		data1_dict = {} # make a data1 dictionary keyed by date for O(n) performance
		for record in data1:
			data1_dict[record[0]] = record 
		
		for date in result_dates:
			result.append(data1_dict[date])
				
		return result
		

		
		


		
			