from django.test import TestCase
from webapp.models import *
from datetime import datetime, timedelta
from decimal import *
from webapp.quotes import *
from webapp.library import *
from parser import *
from functools import partial



# class Sma_Test(TestCase):	
# 	def test_given_a_prices_and_period_When_sma_is_computed_Then_result_returns(self):
# 		dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
# 					("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
# 					("GLD;01-09-2010;price", 8.28)]
# 
# 		sma = Sma(period=10)
# 		result = sma(past_data=dataset, latest_record=("GLD;01-10-2010;price", 9.56))
# 		self.failUnlessEqual("%.3f" % result, "8.244")
# 		
# class Ema_Test(TestCase):
# 	def test_given_a_previous_ema_and_period_and_latest_record_When_ema_is_computed_Then_result_returns(self):
# 		ema_compute = Ema_Value(period=10)
# 		result = ema_compute(previous_ema=9.86, latest_record=("GLD;01-10-2010;price", 10))
# 		self.failUnlessEqual("%.3f" % result, '9.885')
# 		
# 		result = ema_compute(previous_ema=9.86, latest_record=("GLD;01-10-2010;price", 10))
# 		self.failUnlessEqual("%.3f" % result, '9.885')
# 		
# 	def test_given_prices_for_one_period_When_ema_is_computed_then_the_previous_ema_is_derived_by_using_sma_for_the_first_period(self):
# 
# 		dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
# 					("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
# 	 				("GLD;01-09-2010;price", 8.28), ("GLD;01-10-2010;price", 9.56)]
# 		ema_compute_from_data = Ema(period=10)
# 		result = ema_compute_from_data(past_data=dataset, latest_record=("GLD;01-11-2010;price", 10))
# 		self.failUnlessEqual("%.3f" % result, '8.563')
# 
# 		
# 	def test_given_prices_for_more_than_one_period_When_ema_is_computed_Then_the_first_ema_is_sma_and_the_calculation_resumes_proper(self):
# 		dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
# 					("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
# 	 				("GLD;01-09-2010;price", 8.28), ("GLD;01-10-2010;price", 9.56), ("GLD;01-11-2010;price", 10)]
# 
# 		f = Ema(period=10)
# 		result = f(past_data=dataset, latest_record=("GLD;01-12-2010;price", 11))
# 		self.failUnlessEqual("%.3f" % result, '9.006')
# 
# 
# 
# 
# # Test Data Format: 
# #  0    1    2    3   4      5    6    7
# #Date,Open,High,Low,Close,Volume,Adj Close
# 		
# class Macd_Test(TestCase):
# 	def test_given_a_long_term_ma_and_a_short_term_ma_When_macd_is_computed_Then_result_is_returned(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		
# 		f = Macd(long_term_ma=17, short_term_ma=8)
# 		result = f(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual("%.6f" % result, '0.609794')
# 
# 		
# 	def test_given_macd_period_When_macd_signal_is_computed_Then_result_is_returned(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		
# 		f = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
# 		result = f(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual("%.6f" % result, '0.276538')	
# 
# 	
# 	def test_given_a_price_and_price_history_Then_macd_speed_can_be_calculated_for_that_price(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		f = Speed(macd)
# 		result = f(past_data=prices[:-1], latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(0.609794-0.393803))
# 		
# 	def test_given_a_price_and_price_history_Then_is_macd_crossing_with_signal_can_be_queried_False(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
# 		rule = Is_Crossing(operand1=macd, operand2=macd_signal)
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, False)
# 		
# class Stochastic_Test(TestCase):
# 	def test_given_a_price_and_price_history_Then_stochastic_can_be_calculated(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		stochastic = Stochastic(n=14)
# 		result = stochastic(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(94.141689))
# 		
# 	def test_given_a_price_and_price_history_Then_stochastic_signal_can_be_calculated(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		stochastic_signal = Stochastic_Signal(smoothing=3, n=14)
# 		result = stochastic_signal(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(87.943864))	
# 		
# 	def test_given_a_price_and_price_history_Then_slow_stochastic_can_be_calculated(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		slow_stochastic = Slow_Stochastic(n=14, ma=3)
# 		result = slow_stochastic(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(87.943864))
# 		
# 	def test_given_a_price_and_price_history_Then_slow_stochastic_signal_can_be_calculated(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		slow_stochastic_signal = Slow_Stochastic_Signal(n=14, ma=3, smoothing=3)
# 		result = slow_stochastic_signal(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
# 		self.failUnlessEqual("%.6f" % result, "81.093560")
# 
# class Rsi_Test(TestCase):					
# 	def test_given_a_price_and_price_history_Then_RSI_can_be_calculated(self):
# 		#data = get_historical_prices(symbol="GLD", start_date="20050101", end_date="20100301")
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		rsi = Rsi(period=14)
# 		result = rsi(past_data=prices, latest_record=("2010-03-02", 109.86, 111.45, 109.86, 111.02))
# 		self.failUnlessEqual("%.5f" % result, "60.22804")
# 	
# class Operator_Test(TestCase):		
# 	def test_given_a_price_and_price_history_Then_macd_comparisons_can_be_made_between_two_days_and_prices_and_latest_record_can_be_supplied_separately(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 	
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		
# 		result_1 = macd(prices=prices, latest_record=("2010-03-02", 111.02))
# 		result_2 = macd(prices=prices[:-1], latest_record=("2010-03-01", 109.43))
# 		self.failUnlessEqual("%.6f" % result_1, str(0.609794))
# 		self.failUnlessEqual("%.6f" % result_2, str(0.393803))
# 				
# 	def test_a_comparison_rule_should_take_the_rule_settings_the_prices_and_the_comparison_days_ago_displacement_and_return_true_or_false(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		prices = prices[:-1]
# 		
# 		# test Unit
# 		unit = Unit(5)
# 		self.failUnlessEqual(unit(past_data=prices, latest_record=("2010-03-02", 111.02)), 5)
# 		
# 		# here is the macd compute value rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		rule = Is_Less_Than_Or_Equal_To(operand1=macd, operand2=Past(macd, days_ago=1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, False)
# 		
# 		# here is the macd compute speed rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		rule = Is_Greater_Than_Or_Equal_To(operand1=Speed(macd), operand2=Past(Speed(macd), days_ago=1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, True)
# 		
# 		# here is a macd difference rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		rule = Difference_Of(operand1=macd, operand2=Past(macd, days_ago=1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(0.215991))
# 		
# 		rule = Is_Less_Than_Or_Equal_To(operand1=Difference_Of(operand1=macd, operand2=Past(macd, days_ago=1)), operand2=Unit(1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, True)
# 		
# 		# here is a macd abs difference rule
# 		rule = Abs_Difference_Of(operand1=Past(macd, days_ago=1), operand2=macd)
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual("%.6f" % result, str(0.215991))
# 		
# 		# here is a macd crossing signal rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
# 		rule = Is_Crossing(operand1=macd, operand2=macd_signal)
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))	
# 		self.failUnlessEqual(result, False)
# 		
# 		# here is a macd crossing threshold rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		rule_5 = Is_Crossing(operand1=macd, operand2=Unit(0.4))
# 		result = rule_5(past_data=prices, latest_record=("2010-03-02", 111.02))	
# 		self.failUnlessEqual(result, True)
# 		
# 		# here is a macd to macd signal difference rule
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
# 		rule = Is_Less_Than_Or_Equal_To(Difference_Of(operand1=macd, operand2=macd_signal), operand2=Unit(1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, True)
# 		
# 		rule = Is_Greater_Than_Or_Equal_To(Difference_Of(operand1=macd, operand2=Past(macd_signal, days_ago=2)), operand2=Unit(1))
# 		result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# 		self.failUnlessEqual(result, False)
# 		
# 
# 			
# class Rule_Test(TestCase):	
# 	def test_given_a_rule_and_a_data_set_When_the_rule_back_tests_the_data_set_Then_it_returns_the_points_where_the_rule_was_True(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		prices = prices[:-1]
# 		dates = [record[0] for record in data]
# 		
# 		macd = Macd(long_term_ma=17, short_term_ma=8)
# 		rule = Is_Crossing(operand1=macd, operand2=Unit(0))
# 		
# 		back_test = Scanner()
# 		result = back_test.run(expression=rule, past_data=prices)
# 		# for point in result:
# 		# 	print(dates[point])
# 		self.failUnlessEqual(len(result), 14) #should be 16 but long_term_ma buffer makes missing first 17 trading days
# 		
# 	def test_slow_stochastic_crossing_over_rule(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		dates = [record[0] for record in data]
# 		
# 		ss = Slow_Stochastic(n=10, ma=3) # Note: first 13 entries are useless (have None's).  Start at the 14th record
# # 		formatter = ss.data_formatter()
# # 		prices = formatter(data)
# 		back_test = Scanner()
# 
# 		rule = Is_Crossing(operand1=ss, operand2=Unit(20))
# 		result = back_test.run(expression=rule, past_data=prices)
# 		self.failUnlessEqual(len(result), 20)
# 		# print(result)
# 		# for point in result:
# 		# 	print(dates[point])	
# 		
# 		
# 	def test_rsi_speed_rule(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		dates = [record[0] for record in data]
# 		
# 		rule = And(Is_Greater_Than_Or_Equal_To(Speed(Rsi(14)), Unit(1)), Is_Crossing(Rsi(14), Unit(50)))
# 		back_test = Scanner()
# 		result = back_test.run(expression=rule, past_data=prices)
# 		self.failUnlessEqual(len(result), 38) # RSI needs to back date 300 data points from current date in order to be accurate
# 		# for point in result:
# 		# 	print(dates[point])
# 			
# 
# class Yahoo_Api_Test(TestCase):
# 	def test_given_a_raw_dataset_Extract_prices_and_calculate_ema(self):
# 		data = get_historical_prices(symbol="GLD", start_date="20090101", end_date="20100301")
# 
# # 		#days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# # 		data = [day[:-2].split(',') for day in days]
#  		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		
# 		rule = Ema(period=17)
# 		result = rule(past_data=prices[:-1], latest_record=("2010-03-02", 111.02), )
# 
# 		self.failUnlessEqual("%.3f" % result, '108.592') 
# 		
# 		
# class Parser_Test(TestCase):
# 	def test_tokenizer_can_tokenizer_empty_string(self):
# 		tokenizer = Tokenizer(query_text="")	
# 		self.failUnlessEqual(len(tokenizer.tokens), 0)
# 
# 
# 	def test_tokenizer_can_tokenize_raw_string(self):
# 		tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
# 		#print(tokenizer.tokens)	
# 		self.failUnlessEqual(len(tokenizer.tokens), 4)
# 	
# 	def test_parser_can_parse_an_empty_query_string(self):	
# 		tokenizer = Tokenizer(query_text="")
# 		parser = Parser()
# 		rule = parser.parse_query(tokenizer)	
# 		self.assert_(type(rule) is Null_Expression)
# 		
# 		
# 	def test_parser_can_parse_a_query(self):
# 		tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
# 		parser = Parser()
# 		rule = parser.parse_query(tokenizer)	
# 		self.assert_(rule != None)
# 		
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
# 		prices = prices[:-1]
# 		dates = [record[0] for record in data]
# 		
# 		back_test = Scanner()
# 		result = back_test.run(expression=rule, past_data=prices)
# 		self.failUnlessEqual(len(result), 41)
# 		#result = rule(past_data=prices, latest_record=("2010-03-02", 109.86, 111.45, 109.86, 111.02))
# 		# print(result)
# 		# for point in result:
# # 			print(dates[point])
# 		
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		prices = [(record[0], record[4]) for record in data]
# 		prices = prices[:-1]
# 		dates = [record[0] for record in data]
# 		
# 		tokenizer = Tokenizer(query_text="macd(17,8) speed >= macd(17,8) speed 1 days_ago")
# 		rule = parser.parse_query(tokenizer)
# 		self.assert_(rule != None)
# 		#print("test start")
# 		result = back_test.run(expression=rule, past_data=prices)
# 		#print("test end")
# 		self.failUnlessEqual(len(result), 128)
# 		#result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
# # 		for point in result:
# # 			print(dates[point])
# 		
# 		
# 		tokenizer = Tokenizer(query_text="macd(17,8) speed - macd(17,8) speed 1 days_ago >= 0")
# 		rule = parser.parse_query(tokenizer)
# 		self.assert_(rule != None)
# 		result = back_test.run(expression=rule, past_data=prices)
# 		self.failUnlessEqual(len(result), 128)
# 		# for point in result:
# 		# 	print(dates[point])
# 		
# 		tokenizer = Tokenizer(query_text="macd(17,8) is_crossing macd_signal(17,8,9)")
# 		self.failUnlessEqual(len(tokenizer.tokens), 8)
# 		rule = parser.parse_query(tokenizer)
# 		self.assert_(rule != None)
		
		
		
class Execution_Env_Test(TestCase):
# 	def test_Given_an_expression_and_uncut_data_When_it_is_executed_against_the_query_analyzer_Then_it_returns_the_result(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		
# 
# 		ss = Slow_Stochastic(n=10, ma=3) # Note: first 13 entries are useless (have None's).  Start at the 14th record
# 		rule = Is_Crossing(operand1=ss, operand2=Unit(20))
#   		exe_box = Query_Execution_Box(data)
#  		result = exe_box.exe(rule)
#  		self.failUnlessEqual(len(result.data), 20) 		
#  		
#  		parser = Parser()
# 		tokenizer = Tokenizer(query_text="macd(17,8) speed >= macd(17,8) speed 1 days_ago")
# 		rule = parser.parse_query(tokenizer)
# 		result = exe_box.exe(rule)
# 		self.failUnlessEqual(len(result.data), 128)
# 		
# 		
# 		tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
# 		rule = parser.parse_query(tokenizer)	
# 		result = exe_box.exe(rule)
# 		self.failUnlessEqual(len(result.data), 41)
# 		
# 		#very long test
# 		tokenizer = Tokenizer(query_text="macd(17,8) is_crossing macd_signal(17,8,9)")
# 		rule = parser.parse_query(tokenizer)	
# 		result = exe_box.exe(rule)
# 		self.failUnlessEqual(len(result.data), 25)
# 
# 		tokenizer = Tokenizer(query_text="slow_stochastic(10,3) is_crossing 20")
# 		rule = parser.parse_query(tokenizer)	
#  		result = exe_box.exe(rule)
#  		self.failUnlessEqual(len(result.data), 20)
#   		
#  		#very long test
#  		tokenizer = Tokenizer(query_text="slow_stochastic(10,3) is_crossing slow_stochastic_signal(10,3,10)")
# 		rule = parser.parse_query(tokenizer)	
#   		result = exe_box.exe(rule)
#   		self.failUnlessEqual(len(result.data), 46)
#  		#print(result.data)
# 			
# 		
# 	def test_execution_boxes_can_be_chained(self):
# 		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
# 		data = [day[:-2].split(',') for day in days]
# 		data.reverse()
# 		
# 		
#  		parser = Parser()
#  		tokenizer = Tokenizer(query_text="macd(17,8) speed >= macd(17,8) speed 1 days_ago")
#  		rule = parser.parse_query(tokenizer)
#  		exe_box = Query_Execution_Box(data)
#  		result_box = exe_box.exe(rule)	
# 		
# 		tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
# 		rule = parser.parse_query(tokenizer)	
# 		result = result_box.exe(rule)
# 		self.failUnlessEqual(len(result.data), 23)
# 		#print(result.data)
# 		
# 		
# 		#fluent interface
# 		parser = Parser()
#  		tokenizer = Tokenizer(query_text="macd(17,8) speed >= macd(17,8) speed 1 days_ago")
#  		expression1 = parser.parse_query(tokenizer)
# 		tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
# 		expression2 = parser.parse_query(tokenizer)
# 		
# 		box = Query_Execution_Box(data)
# 		results = box.exe(expression1).exe(expression2)
# 		self.failUnlessEqual(len(results.data), 23)
		
	def test_execution_box_can_accept_query_string(self):
		days = open("/home/developer/sparrow.com/sparrow/webapp/test_data/data.txt").readlines()
		data = [day[:-2].split(',') for day in days]
		data.reverse()
		
# 		box = Query_Execution_Box(data)
#  		result = box("macd(17,8) speed is_increasing")("rsi(14) is_crossing 50")(None)
# #		result = box("macd(17,8) speed is_increasing")()
# 		self.failUnlessEqual(len(result.data), 23)
		
		data = get_historical_prices(symbol="aapl", start_date="20090101", end_date="20100601")
 		data.reverse()
 		print("test start------------------------------------------------------------")
 		box = Query_Execution_Box(data)
 		
		result = box("price >= 220")
# 		parser = Parser()
#  		tokenizer = Tokenizer(query_text="price >= 220")
#  		print tokenizer.tokens
# 		expression = parser.parse_query(tokenizer)
		print("test end--------------------------------------------------------------")

		#print(result.data)

