from django.test import TestCase
from webapp.models import *
from datetime import datetime, timedelta
from decimal import *
from webapp.quotes import *
from webapp.library import *
from parser import *
from functools import partial
from webapp.quotes import *
import os

APP_ROOT = os.path.realpath(os.path.dirname(__file__))
DATAFILE_PATH = APP_ROOT+"/test_data/data.txt"

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
# 		buy_points = service.execute_query("GLD", "20100101", "20100601", "macd(17,8) is_crossing macd_signal(17,8,9)")
		
		
#		print buy_points.data
		#buy_points = service.execute_query("DIG", "20100101", "20100820", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0", "macd(17,8) <= 0")
 		#buy_points = service.execute_query("DIG", "20100101", "20100820", "macd(17,8) speed is_increasing", "macd(17,8) gradient >= 0.5", "macd(17,8) is_crossing macd_signal(17,8,5)", "macd(17,8) <= 0", "slow_stochastic(5,3) gradient >= 0")
		# for point in buy_points.data:
# 			if point[-1]:
# 				print point

		buy_points = service.execute_query("MSFT", "20100101", "20100820", ["macd(17,8) is_crossing macd_signal(17,8,5)", "macd(17,8) gradient >= 0"])
		#print buy_points.data

 		#sell_points = service.execute_query("GLD", "20100101", "20100820", "slow_stochastic(5,5) is_crossing 80", "slow_stochastic(5,5) gradient <= 0")
 		#sell_points = service.execute_query("DIG", "20100101", "20100820", "slow_stochastic(5,5) gradient 1 days_ago >= 0", "slow_stochastic(5,5) gradient <= 0")
 		
 		
		sell_points = service.execute_query("MSFT", "20100101", "20100820", ["macd(17,8) speed is_decreasing", "slow_stochastic(5,3) speed is_decreasing", "macd(17,8) >= 0"])
  		backtester = Backtester()
 		account = Account(cash_balance=10000)
 		summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account)
		print summary
# 		
#		self.failUnlessEqual(summary, "100")
		
# 		short_points = service.execute_query("GLD", "20100101", "20100820", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient <= 0", "macd(17,8) >= 0")
# 		print short_points.data
# 		cover_points = service.execute_query("GLD", "20100101", "20100820", "slow_stochastic(5,5) speed is_decreasing")
# 		backtester = Backtester()
# 		account = Account(cash_balance=10000)
# 		summary = backtester.execute_short_strategy(short_points.data, cover_points.data, account)
# 		print summary
		


# 		


from tests_web_api_01 import *
from tests_lib import *