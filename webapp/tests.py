from django.test import TestCase
from webapp.models import *
from datetime import datetime, timedelta
from decimal import *
from webapp.quotes import *
from webapp.library import *
from parser import *
from functools import partial
from webapp.quotes import *


class test_bed(TestCase):
	def test1(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		data = data[:-1]
# 		parser = Parser(data)
# 		#print data	
# 	
# 		exe_box = Query_Execution_Box(data)
# 		tokenizer = Tokenizer(query_text="price 3 days_later >= price")
# 		rule = parser.parse_query(tokenizer)
# 		result = exe_box.exe(rule)
# 		#print(result.data)
# 		self.failUnlessEqual(len(result.data), 168)

# 		expression_evaluator = Expression_Evaluator()
# 		expression = Is_Greater_Than_Or_Equal_To(operand1=Price(), operand2=Unit(120))
# 		result = expression_evaluator.is_true(symbol="gld", expression=expression, today="20100703")
		#print result
# 		result = get_quote("gld")
# 		print result
		
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		data = data[:-1]
# 		data_with_flag = []
# 		for record in data:
#   			record.append(None)
#   			data_with_flag.append(record)
# 		parser = Parser(data_with_flag)
# 		
# 		
# 		exe_box = Query_Execution_Box(data_with_flag)
# 		tokenizer = Tokenizer(query_text="macd(17,8) is_crossing macd_signal(17,8,9)")
# 		rule = parser.parse_query(tokenizer)	
# 		result = exe_box.exe(rule)
# 		self.failUnlessEqual(result.number_of_points, 25)


		service = Service()
		result = service.execute_query("GLD", "20090101", "20100301", "macd(17,8) is_crossing macd_signal(17,8,9)")
		self.failUnlessEqual(result.number_of_points, 28)
		
				
		buy_points = service.execute_query("GLD", "20090101", "20100801", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0")
		sell_points = service.execute_query("GLD", "20090101", "20100801", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient <= 0")
		backtester = Backtester()
		summary = backtester.execute(buy_points.data, sell_points.data)
		print summary


#from tests_web_api_01 import *
#from tests_lib import *