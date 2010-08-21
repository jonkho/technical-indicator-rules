from django.db import models
from django.contrib.auth.models import User, UserManager
import sys, traceback
from datetime import datetime, timedelta
from parser import *
from webapp.quotes import *
import copy
# Create your models here.

class Utils(object):
	def one_year_earlier(self, start_date):
		year = int(start_date[:4])
		year_earlier = year - 1
		return "%s%s" % (year_earlier, start_date[4:]) 
		
	def remove_runway(self, data, start_date):
		date_string_to_search = "%s-%s-%s" % (start_date[:4], start_date[4:6], start_date[6:8])
		for (counter, record) in enumerate(data):
			if record[0] >= date_string_to_search:
				return data[counter:]
				
		raise RuntimeError
		
	def yesterday(self, start_date):
		date_string = "%s-%s-%s" % (start_date[:4], start_date[4:6], start_date[6:8])
		start_datetime = datetime.strptime(date_string, "%Y-%m-%d")
		start_datetime = start_datetime - timedelta(days=1)
		return start_datetime.strftime("%Y%m%d")
			


class Return_Code(object):
	value = ""
	contents = None
	
	def __init__(self, value, contents=None):
		super(Return_Code, self).__init__()
		self.value = value
		self.contents = contents

class Indicator_History(object):
	def __init__(self):
		self.memo = {}
		super(Indicator_History, self).__init__()
		
	def __call__(self, indicator, data):
		final_list = []
		parser = Parser()
 		tokenizer = Tokenizer(indicator)
		indicator = parser.parse_indicator(tokenizer)
		formatted_data = indicator.cut_data(data)
		
		for (counter, point) in enumerate(formatted_data):
			date = data[counter][0]
			
			try:
				indicator_value = indicator(formatted_data[:counter], formatted_data[counter], self.memo)
				date_value_pair = (date, indicator_value)
			except:
				date_value_pair = (date, None)
				
			final_list.append(date_value_pair)	
		
		return final_list	

class Expression_Evaluator(object):
	def is_true(self, symbol, expression, today):
		utils = Utils()
		runway_start_date = utils.one_year_earlier(today)
		yesterday = utils.yesterday(today)
		runway_data = get_historical_prices(symbol=symbol, start_date=runway_start_date, end_date=yesterday)
 		runway_data.reverse()
 		runway_data = runway_data[:-1]
 		formatted_runway_data = expression.cut_data(runway_data)
 		#print formatted_runway_data
 		
 		latest_record = get_quote(symbol)
 		formatted_record = expression.cut_data([latest_record])
 		#print formatted_record
 		result = expression(past_data=formatted_runway_data, latest_record=formatted_record[0])
		return result
 		

class Scanner(object):		
	# this class evaluates the expression on all the past data points
	# and return the indexes into the past_data set when the expression evaluates true
	
	def run(self, expression, past_data, memo=None):
		result_list = []
		for (counter, point) in enumerate(past_data):
			try:
				result = expression(past_data=past_data[:counter], latest_record=past_data[counter], memo=memo)
			except Exception as e:
				#traceback.print_exc()
				result = None
	
			if result: 
				result_list.append(counter)				
		return result_list


class Query_Execution_Box(object):	
	# this class creates the execution environment by cutting the data
	# then running the scan
	
	def __init__(self, data):
		# data holds the parent (or previous) query result
		# full_data holds the raw data for reference when fluent chaining
		# if full_data is None, this implies this class instance is the root and thus data holds the full raw data
		# number_of_points is the running count of the resulting number of points that is evaluated True
		# memo is the dictionary for memoization that must be passed to the scanner 
		self.memo = {}
		self.data = data
		
# 		if full_data is None:
# 			self._full_data = data
# 		else:
# 			self._full_data = None
			
		super(Query_Execution_Box, self).__init__()	
		
	def __call__(self, query_string):
#		parser = Parser(self._full_data)
		parser = Parser(self.data)
 		tokenizer = Tokenizer(query_text=query_string)
 		expression = parser.parse_query(tokenizer)
		return self.exe(expression)
		
	def exe(self, expression):
		# always cut and scan from the full raw data
		formatted_data = expression.cut_data(self.data)
		scanner = Scanner()
		indexes = scanner.run(expression, formatted_data, self.memo)
		
		# mark the records for this query's results
		this_querys_results = copy.deepcopy(self.data)
		for record in this_querys_results:
			record[-1] = False
						
		for index in indexes:
			this_querys_results[index][-1] = True	
			
		# apply logical AND	
		result = self.logical_and(this_querys_results, self.data)	

		# return	
		return Query_Execution_Box(data=result)	
			
		
		# find the intersection between the current query results and the parent query results to get the FINAL result
		#query_result = self.intersection(self.data, query_data)
		#return Query_Execution_Box(data=query_result, full_data=self._full_data)	
	
	@property
	def number_of_points(self):
		count = 0
		for record in self.data:
			if record[-1]:
				count += 1
		return count
		
	@property	
	def marked_days(self):
		result = []
		for record in self.data:
			if record[-1]:
				result.append(record)
		return result	
		
	def logical_and(self, data1, data2):
		result = []
		for (counter, record) in enumerate(data1):
			new_record = copy.deepcopy(record)
			if record[-1] == None and data2[counter][-1] == None:
				new_record[-1] = False
				#print("%s) branch 1, new record is set to: %s and %s = %s" % (counter,record[-1], data2[counter][-1], new_record[-1]))
				
			elif record[-1] == None and data2[counter][-1] != None:
				new_record[-1] = data2[counter][-1]	
				#print("%s) branch 2, new record is set to: %s and %s = %s" % (counter,record[-1], data2[counter][-1], new_record[-1]))	
			
			elif record[-1] != None and data2[counter][-1] == None:
				new_record[-1] = record[-1]
				#print("%s) branch 3, new record is set to: %s and %s = %s" % (counter,record[-1], data2[counter][-1], new_record[-1]))
			
			else:
				new_record[-1] = record[-1] and data2[counter][-1]
				#print("%s) branch 4, new record is set to: %s and %s = %s" % (counter,record[-1], data2[counter][-1], new_record[-1]))
			
			result.append(new_record)
		
		return result	
			
		
# 	def intersection(self, data1, data2):
# 		
# 		# make lists of dates for easier set operations
# 		data1_set = set([record[0] for record in data1])
# 		data2_set = set([record[0] for record in data2])		
# 		records_in_common = data1_set.intersection(data2_set)
# 		result_dates = list(records_in_common)
# 		result_dates.sort()
# 		
# 		# retrieve the records from data1 that corresponds to the result dates
# 		result = []
# 		data1_dict = {} # make a data1 dictionary keyed by date for O(n) performance
# 		for record in data1:
# 			data1_dict[record[0]] = record 
# 		
# 		for date in result_dates:
# 			result.append(data1_dict[date])
# 				
# 		return result
# 		
			