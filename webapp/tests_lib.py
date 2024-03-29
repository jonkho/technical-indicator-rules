from django.test import TestCase
from webapp.models import *
from datetime import datetime, timedelta
from decimal import *
from webapp.quotes import *
from webapp.library import *
from parser import *
from functools import partial
import os

#use relative paths for portability
APP_ROOT = os.path.realpath(os.path.dirname(__file__))
DATAFILE_PATH = APP_ROOT+"/test_data/data.txt"

class Sma_Test(TestCase):       
    def test_given_a_prices_and_period_When_sma_is_computed_Then_result_returns(self):
        dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
                                ("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
                                ("GLD;01-09-2010;price", 8.28)]

        sma = Sma(period=10)
        result = sma(past_data=dataset, latest_record=("GLD;01-10-2010;price", 9.56))
        self.failUnlessEqual("%.3f" % result, "8.244")
        
class Ema_Test(TestCase):
    def test_given_a_previous_ema_and_period_and_latest_record_When_ema_is_computed_Then_result_returns(self):
        ema_compute = Ema_Value(period=10)
        result = ema_compute(previous_ema=9.86, latest_record=("GLD;01-10-2010;price", 10))
        self.failUnlessEqual("%.3f" % result, '9.885')
        
        result = ema_compute(previous_ema=9.86, latest_record=("GLD;01-10-2010;price", 10))
        self.failUnlessEqual("%.3f" % result, '9.885')
        
    def test_given_prices_for_one_period_When_ema_is_computed_then_the_previous_ema_is_derived_by_using_sma_for_the_first_period(self):

        dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
                                ("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
                                ("GLD;01-09-2010;price", 8.28), ("GLD;01-10-2010;price", 9.56)]
        ema_compute_from_data = Ema(period=10)
        result = ema_compute_from_data(past_data=dataset, latest_record=("GLD;01-11-2010;price", 10))
        self.failUnlessEqual("%.3f" % result, '8.563')

        
    def test_given_prices_for_more_than_one_period_When_ema_is_computed_Then_the_first_ema_is_sma_and_the_calculation_resumes_proper(self):
        dataset = [("GLD;01-01-2010;price", 10.55), ("GLD;01-02-2010;price", 9.69), ("GLD;01-03-2010;price", 7.67), ("GLD;01-04-2010;price", 7.89), 
                                ("GLD;01-05-2010;price", 6.90), ("GLD;01-06-2010;price", 6.89), ("GLD;01-07-2010;price", 7.67), ("GLD;01-08-2010;price", 7.34), 
                                ("GLD;01-09-2010;price", 8.28), ("GLD;01-10-2010;price", 9.56), ("GLD;01-11-2010;price", 10)]

        f = Ema(period=10)
        result = f(past_data=dataset, latest_record=("GLD;01-12-2010;price", 11))
        self.failUnlessEqual("%.3f" % result, '9.006')




# Test Data Format: 
#  0    1    2    3   4      5    6    
#Date,Open,High,Low,Close,Volume,Adj Close
                
class Macd_Test(TestCase):
    def test_given_a_long_term_ma_and_a_short_term_ma_When_macd_is_computed_Then_result_is_returned(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        
        f = Macd(long_term_ma=17, short_term_ma=8)
        result = f(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, '0.609794')

        
    def test_given_macd_period_When_macd_signal_is_computed_Then_result_is_returned(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        
        f = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
        result = f(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, '0.276538')   
        
#         f2 = Ema(9, Macd(8,17))
#         result = f2(past_data=prices[:-1], latest_record=("2010-03-02", 111.02))
#         self.failUnlessEqual("%.6f" % result, '0.276538')
        
        
    def test_given_a_price_and_price_history_Then_macd_speed_can_be_calculated_for_that_price(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        
        macd = Macd(long_term_ma=17, short_term_ma=8)
        f = Speed(macd)
        result = f(past_data=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, str(0.609794-0.393803))
        
    def test_given_a_price_and_price_history_Then_is_macd_crossing_with_signal_can_be_queried_False(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        
        macd = Macd(long_term_ma=17, short_term_ma=8)
        macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
        rule = Is_Crossing(operand1=macd, operand2=macd_signal)
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, False)
        
    def test_given_a_price_and_price_history_Then_a_macd_histogram_bar_can_be_calculated(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        
        f = Macd(long_term_ma=17, short_term_ma=8)
        result = f(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, '0.609794')
        
        f2 = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
        result2 = f2(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result2, '0.276538')
        
        histogram_value = result - result2
         
        f3 = Macd_Histogram(8,17,9)
        result3 = f3(prices=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % histogram_value, "%.6f" % result3)
        
        f4 = Histogram(Macd(8,17), Macd_Signal(8,17,9))
        result4 = f4(past_data=prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % histogram_value, "%.6f" % result4)
                     
        
class Stochastic_Test(TestCase):
    def test_given_a_price_and_price_history_Then_stochastic_can_be_calculated(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        
        stochastic = Stochastic(n=14)
        result = stochastic(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
        self.failUnlessEqual("%.6f" % result, str(94.141689))
        
    def test_given_a_price_and_price_history_Then_stochastic_signal_can_be_calculated(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        
        stochastic_signal = Stochastic_Signal(smoothing=3, n=14)
        result = stochastic_signal(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
        self.failUnlessEqual("%.6f" % result, str(87.943864))   
        
    def test_given_a_price_and_price_history_Then_full_stochastic_can_be_calculated(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        
        full_stochastic = Full_Stochastic(n=14, ma=3)
        result = full_stochastic(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
        self.failUnlessEqual("%.6f" % result, str(87.943864))
        
    def test_given_a_price_and_price_history_Then_full_stochastic_signal_can_be_calculated(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        
        full_stochastic_signal = Full_Stochastic_Signal(n=14, ma=3, smoothing=3)
        result = full_stochastic_signal(past_data=prices, latest_record=("2010-03-02", 111.45, 109.86, 111.02))
        self.failUnlessEqual("%.6f" % result, "81.093560")
        
    

class Rsi_Test(TestCase):                                       
    def test_given_a_price_and_price_history_Then_RSI_can_be_calculated(self):
        #data = get_historical_prices(symbol="GLD", start_date="20050101", end_date="20100301")
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        
        rsi = Rsi(period=14)
        result = rsi(past_data=prices, latest_record=("2010-03-02", 109.86, 111.45, 109.86, 111.02))
        self.failUnlessEqual("%.5f" % result, "60.22804")

class Operator_Test(TestCase):          
    def test_given_a_price_and_price_history_Then_macd_comparisons_can_be_made_between_two_days_and_prices_and_latest_record_can_be_supplied_separately(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        

        macd = Macd(long_term_ma=17, short_term_ma=8)
        
        result_1 = macd(prices=prices, latest_record=("2010-03-02", 111.02))
        result_2 = macd(prices=prices[:-1], latest_record=("2010-03-01", 109.43))
        self.failUnlessEqual("%.6f" % result_1, str(0.609794))
        self.failUnlessEqual("%.6f" % result_2, str(0.393803))
                        
    def test_a_comparison_rule_should_take_the_rule_settings_the_prices_and_the_comparison_days_ago_displacement_and_return_true_or_false(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        
        # test Unit
        unit = Unit(5)
        self.failUnlessEqual(unit(past_data=prices, latest_record=("2010-03-02", 111.02)), 5)
        
        # here is the macd compute value rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule = Is_Less_Than_Or_Equal_To(operand1=macd, operand2=Past(macd, days_ago=1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, False)
        
        # here is the macd compute speed rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule = Is_Greater_Than_Or_Equal_To(operand1=Speed(macd), operand2=Past(Speed(macd), days_ago=1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, True)
        
        # here is a macd difference rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule = Difference_Of(operand1=macd, operand2=Past(macd, days_ago=1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, str(0.215991))
        
        rule = Is_Less_Than_Or_Equal_To(operand1=Difference_Of(operand1=macd, operand2=Past(macd, days_ago=1)), operand2=Unit(1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, True)
        
        # here is a macd abs difference rule
        rule = Abs_Difference_Of(operand1=Past(macd, days_ago=1), operand2=macd)
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, str(0.215991))
        
        # here is a macd crossing signal rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
        rule = Is_Crossing(operand1=macd, operand2=macd_signal)
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))   
        self.failUnlessEqual(result, False)
        
        # here is a macd crossing threshold rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule_5 = Is_Crossing(operand1=macd, operand2=Unit(0.4))
        result = rule_5(past_data=prices, latest_record=("2010-03-02", 111.02)) 
        self.failUnlessEqual(result, True)
        
        # here is a macd crossing above threshold rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule_5 = Is_Crossing_Above(operand1=macd, operand2=Unit(0.4))
        result = rule_5(past_data=prices, latest_record=("2010-03-02", 111.02)) 
        self.failUnlessEqual(result, True)
        
        # here is a macd crossing below threshold rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule_5 = Is_Crossing_Below(operand1=macd, operand2=Unit(0.4))
        result = rule_5(past_data=prices, latest_record=("2010-03-02", 111.02)) 
        self.failUnlessEqual(result, False)
        
        # here is a macd to macd signal difference rule
        macd = Macd(long_term_ma=17, short_term_ma=8)
        macd_signal = Macd_Signal(long_term_ma=17, short_term_ma=8, period=9)
        rule = Is_Less_Than_Or_Equal_To(Difference_Of(operand1=macd, operand2=macd_signal), operand2=Unit(1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, True)
        
        rule = Is_Greater_Than_Or_Equal_To(Difference_Of(operand1=macd, operand2=Past(macd_signal, days_ago=2)), operand2=Unit(1))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, False)
        
class Price_Test(TestCase):
    def test_price(self):
        # here is price rule
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        price = Price()
        
        rule = Is_Greater_Than_Or_Equal_To(operand1=price, operand2=Unit(107))
        result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual(result, True)
        
    def test_price_against_sma(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        prices = [(record[0], record[4]) for record in data]

        price = Price()
        rule = Is_Greater_Than_Or_Equal_To(operand1=price, operand2=Sma(20))
        
        scanner = Scanner()
        result = scanner.run(expression=rule, past_data=prices)
        self.failUnlessEqual(len(result), 179)
        

class Volume_Test(TestCase):
    def test_volume(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        volumes = [(record[0], record[5]) for record in data]
        volumes = volumes[:-1]
        volume = Volume()
        
        rule = Is_Greater_Than_Or_Equal_To(operand1=volume, operand2=Unit(30000000))
        result = rule(past_data=volumes, latest_record=("2010-03-02", 40000000))
        self.failUnlessEqual(result, True)

        back_test = Scanner()
        result = back_test.run(expression=rule, past_data=volumes)
#               for point in result:
#                       print(volumes[point][0])
        self.failUnlessEqual(len(result), 18)
        
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
        parser = Parser(data_with_flag)
        tokenizer = Tokenizer(query_text="volume >= 30000000")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data)
        result_box = exe_box.exe(rule)
        self.failUnlessEqual(result_box.number_of_points, 18)   

                        
        
class Modifier_Test(TestCase):
    def test_Future_modifier(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        prices = [(record[0], record[4]) for record in data]
        dates = [record[0] for record in data]
        
        price = Price()
        rule = Is_Greater_Than_Or_Equal_To(operand1=Future(operand=price, days_later=3, future_data=data), operand2=price)
        result = rule(past_data=prices[:-11], latest_record=("2010-02-12", 107.04))
        self.failUnlessEqual(result, True)
        
        rule = Is_Greater_Than_Or_Equal_To(operand1=price, operand2=Future(operand=price, days_later=3, future_data=data))
        result = rule(past_data=prices[:-11], latest_record=("2010-02-12", 107.04))
        self.failUnlessEqual(result, False)

                
class Rule_Test(TestCase):      
    def test_given_a_rule_and_a_data_set_When_the_rule_back_tests_the_data_set_Then_it_returns_the_points_where_the_rule_was_True(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        dates = [record[0] for record in data]
        
        macd = Macd(long_term_ma=17, short_term_ma=8)
        rule = Is_Crossing(operand1=macd, operand2=Unit(0))
        
        back_test = Scanner()
        result = back_test.run(expression=rule, past_data=prices)
        # for point in result:
        #       print(dates[point])
        self.failUnlessEqual(len(result), 14) #should be 16 but long_term_ma buffer makes missing first 17 trading days
        
    def test_full_stochastic_crossing_over_rule(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        dates = [record[0] for record in data]
        
        ss = Full_Stochastic(n=10, ma=3) # Note: first 13 entries are useless (have None's).  Start at the 14th record
#               formatter = ss.data_formatter()
#               prices = formatter(data)
        back_test = Scanner()

        rule = Is_Crossing(operand1=ss, operand2=Unit(20))
        result = back_test.run(expression=rule, past_data=prices)
        self.failUnlessEqual(len(result), 20)
        # print(result)
        # for point in result:
        #       print(dates[point])     
        
        
    def test_rsi_speed_rule(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        dates = [record[0] for record in data]
        
        rule = And(Is_Greater_Than_Or_Equal_To(Speed(Rsi(14)), Unit(1)), Is_Crossing(Rsi(14), Unit(50)))
        back_test = Scanner()
        result = back_test.run(expression=rule, past_data=prices)
        self.failUnlessEqual(len(result), 38) # RSI needs to back date 300 data points from current date in order to be accurate
        # for point in result:
        #       print(dates[point])
                

class Yahoo_Api_Test(TestCase):
    def test_given_a_raw_dataset_Extract_prices_and_calculate_ema(self):
        data = get_historical_prices(symbol="GLD", start_date="20090101", end_date="20100301")

#               #days = open(DATAFILE_PATH).readlines()
#               data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        
        rule = Ema(period=17)
        result = rule(past_data=prices[:-1], latest_record=("2010-03-02", 111.02), )

        self.failUnlessEqual("%.3f" % result, '108.592') 
        
        
class Parser_Test(TestCase):
    def test_tokenizer_can_tokenizer_empty_string(self):
        tokenizer = Tokenizer(query_text="")    
        self.failUnlessEqual(len(tokenizer.tokens), 0)


    def test_tokenizer_can_tokenize_raw_string(self):
        tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")      
        self.failUnlessEqual(len(tokenizer.tokens), 4)

    def test_parser_can_parse_an_empty_query_string(self):  
        tokenizer = Tokenizer(query_text="")
        parser = Parser()
        rule = parser.parse_query(tokenizer)    
        self.assert_(type(rule) is Null_Expression)
        
        
    def test_parser_can_parse_a_query(self):
        tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
        parser = Parser()
        rule = parser.parse_query(tokenizer)    
        self.assert_(rule != None)
        self.failUnlessEqual(parser.indicator_operands[0][0], "rsi(14)")
        
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[1], record[2], record[3], record[4]) for record in data]
        prices = prices[:-1]
        dates = [record[0] for record in data]
        
        back_test = Scanner()
        result = back_test.run(expression=rule, past_data=prices)
        self.failUnlessEqual(len(result), 41)
        #result = rule(past_data=prices, latest_record=("2010-03-02", 109.86, 111.45, 109.86, 111.02))
        # print(result)
        # for point in result:
#                       print(dates[point])
                
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]
        prices = prices[:-1]
        dates = [record[0] for record in data]
        
        tokenizer = Tokenizer(query_text="macd(8,17) speed >= macd(8,17) speed 1 days_ago")
        rule = parser.parse_query(tokenizer)
        self.assert_(rule != None)
        self.failUnlessEqual(parser.indicator_operands[0][0], "macd(8,17)")
        self.failUnlessEqual(parser.indicator_operands[1][0], "macd(8,17)")
        #print("test start")
        result = back_test.run(expression=rule, past_data=prices)
        #print("test end")
        self.failUnlessEqual(len(result), 128)
        #result = rule(past_data=prices, latest_record=("2010-03-02", 111.02))
#               for point in result:
#                       print(dates[point])
                
                
        tokenizer = Tokenizer(query_text="macd(8,17) speed - macd(8,17) speed 1 days_ago >= 0")
        rule = parser.parse_query(tokenizer)
        self.assert_(rule != None)
        result = back_test.run(expression=rule, past_data=prices)
        self.failUnlessEqual(len(result), 128)
        # for point in result:
        #       print(dates[point])
        
        tokenizer = Tokenizer(query_text="macd(8,17) is_crossing macd_signal(8,17,9)")
        self.failUnlessEqual(len(tokenizer.tokens), 8)
        rule = parser.parse_query(tokenizer)
        self.failUnlessEqual(parser.indicator_operands[0][0], "macd(8,17)")
        self.failUnlessEqual(parser.indicator_operands[1][0], "macd_signal(8,17,9)")
        self.assert_(rule != None)
        
        # test negative floats
        tokenizer = Tokenizer(query_text="macd(8,17) <= -0.523")
        self.failUnlessEqual(len(tokenizer.tokens), 5)
        
        # test parsing transforms
        tokenizer = Tokenizer(query_text="macd_signal(8,17,9)->histogram >= 0")
        parser = Parser()
        rule = parser.parse_query(tokenizer)    
        self.assert_(rule != None)
        self.failUnlessEqual(parser.indicator_operands[0][0], "macd_signal(8,17,9)")
        self.failUnlessEqual(parser.indicator_operands[1][0], "macd_signal(8,17,9)->histogram")
        

class Transform_Test(TestCase):
    def test_transform_should_be_able_to_process_data_properly(self):
    
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        prices = [(record[0], record[4]) for record in data]    
    
        one_transform = Transform(Macd(long_term_ma=17, short_term_ma=8))
        result = one_transform(prices[:-1], latest_record=("2010-03-02", 111.02)) 
        self.failUnlessEqual("%.6f" % result, '0.609794')
        
        two_transforms = one_transform.add(Ema(9))
        result = two_transforms(prices[:-1], latest_record=("2010-03-02", 111.02))
        self.failUnlessEqual("%.6f" % result, '0.276538')
    
    def test_parser_should_be_able_to_read_transform_queries(self):
    
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
        parser = Parser(data_with_flag)


        # These two macds queries should be mathematically identical
        tokenizer = Tokenizer(query_text="macd_signal(8,17,9) >= 0")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data_with_flag)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 171)
        
        tokenizer = Tokenizer(query_text="macd(8,17)->ema(9) >= 0")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data_with_flag)   
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 171)
        self.failUnlessEqual(parser.indicator_operands[0][0], "macd(8,17)")
        self.failUnlessEqual(parser.indicator_operands[1][0], "macd(8,17)->ema(9)")
        #self.failUnlessEqual("%.6f" % parser.indicator_operands[2][1][-1], '0.276538')
        
        # These two stochastic queries should be mathematically identical
        tokenizer = Tokenizer(query_text="slow_stochastic(5) >= 0")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data_with_flag)   
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 284)
        
        tokenizer = Tokenizer(query_text="stochastic(5)->sma(3) >= 0")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data_with_flag)   
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 284)
        self.failUnlessEqual(parser.indicator_operands[0][0], "stochastic(5)") 
        self.failUnlessEqual(parser.indicator_operands[1][0], "stochastic(5)->sma(3)")  
        
        
        # test service
        service = Service()
        ticker_data = service.get_ticker_data("GLD", "20090101", "20100301")
        result = service.execute_query_on_ticker_data(ticker_data, "20090101", ["macd(8,17)->ema(9) >= 0"])
        #result = service.execute_query("GLD", "20090101", "20100301", ["macd(8,17)->ema(9) >= 0"])
        self.failUnlessEqual(result.number_of_points, 197)
        
        result2 = service.execute_query_on_ticker_data(ticker_data, "20090101", ["macd_signal(8,17,9) >= 0"])
        #result2 = service.execute_query("GLD", "20090101", "20100301", ["macd_signal(8,17,9) >= 0"])
        self.failUnlessEqual(result2.number_of_points, 197)  
                    
        
class Execution_Env_Test(TestCase):
    def test_Given_an_expression_and_uncut_data_When_it_is_executed_against_the_query_analyzer_Then_it_returns_the_result(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
        parser = Parser(data_with_flag)
        

        ss = Full_Stochastic(n=10, ma=3) # Note: first 13 entries are useless (have None's).  Start at the 14th record
        rule = Is_Crossing(operand1=ss, operand2=Unit(20))
        exe_box = Query_Execution_Box(data_with_flag)
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 20)               
        
        
        tokenizer = Tokenizer(query_text="macd(8,17) speed >= macd(8,17) speed 1 days_ago")
        rule = parser.parse_query(tokenizer)
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 128)
        
        
        tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 41)
        
        #very long test
        tokenizer = Tokenizer(query_text="macd(8,17) is_crossing macd_signal(8,17,9)")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 25)
        
        tokenizer = Tokenizer(query_text="macd(8,17) is_crossing_above macd_signal(8,17,9)")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 13)
        
        tokenizer = Tokenizer(query_text="macd(8,17) is_crossing_below macd_signal(8,17,9)")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 12)
        

        tokenizer = Tokenizer(query_text="full_stochastic(10,3) is_crossing 20")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 20)
        
        #very long test
        tokenizer = Tokenizer(query_text="full_stochastic(10,3) is_crossing full_stochastic_signal(10,3,10)")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 46)
        #print(result.data)
#       
        tokenizer = Tokenizer(query_text="slow_stochastic(10) is_crossing slow_stochastic_signal(10,10)")
        rule = parser.parse_query(tokenizer)    
        result = exe_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 46)        

        exe_box = Query_Execution_Box(data)
        tokenizer = Tokenizer(query_text="price 3 days_later >= price")
        rule = parser.parse_query(tokenizer)
        result = exe_box.exe(rule)
        #print(result.data)
        self.failUnlessEqual(result.number_of_points, 168)
                
    def test_execution_box_logical_and(self):
        exe_box = Query_Execution_Box(None)
        result = exe_box.logical_and([["something", None], ["something", False], ["something", True]], [["something", None], ["something", True], ["something", True]]) 
        self.failUnlessEqual(len(result), 3)
        self.failUnlessEqual(result[0][-1], False)
        self.failUnlessEqual(result[1][-1], False)
        self.failUnlessEqual(result[2][-1], True)       
                
        
    def test_execution_boxes_can_be_chained(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
        parser = Parser(data_with_flag)
        
        tokenizer = Tokenizer(query_text="macd(8,17) speed >= macd(8,17) speed 1 days_ago")
        rule = parser.parse_query(tokenizer)
        exe_box = Query_Execution_Box(data)
        result_box = exe_box.exe(rule)


        tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
        rule = parser.parse_query(tokenizer)    
        result = result_box.exe(rule)
        self.failUnlessEqual(result.number_of_points, 23)
        #print(result.data)

        
        
        #fluent interface
        parser = Parser()
        tokenizer = Tokenizer(query_text="macd(8,17) speed >= macd(8,17) speed 1 days_ago")
        expression1 = parser.parse_query(tokenizer)
        tokenizer = Tokenizer(query_text="rsi(14) is_crossing 50")
        expression2 = parser.parse_query(tokenizer)
        
        box = Query_Execution_Box(data)
        results = box.exe(expression1).exe(expression2)
        self.failUnlessEqual(results.number_of_points, 23)
        
    def test_execution_box_can_accept_query_string(self):
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
    
        box = Query_Execution_Box(data_with_flag)
        result = box("macd(8,17) speed is_increasing")("rsi(14) is_crossing 50")(None)
        self.failUnlessEqual(result.number_of_points, 23)
        
        

        data = get_historical_prices(symbol="gld", start_date="20090101", end_date="20100601")
        data.reverse()
        data = data[:-1]
        data_with_flag = []
        for record in data:
            record.append(None)
            data_with_flag.append(record)
            
        box = Query_Execution_Box(data_with_flag)
        result = box("price 3 days_later >= price")
        self.failUnlessEqual(result.number_of_points, 209)
        
        
        box = Query_Execution_Box(data_with_flag)
        result = box("macd_histogram(8,17,9) >= 0")
        self.failUnlessEqual(result.number_of_points, 172)
        
        
        box = Query_Execution_Box(data_with_flag)
        result = box("macd_signal(8,17,9)->histogram >= 0")
        self.failUnlessEqual(result.number_of_points, 172)

        

    def test_execution_box_should_return_the_history_of_the_technical_indicators_being_queried(self):
        data = get_historical_prices(symbol="gld", start_date="20080101", end_date="20100601")
        data.reverse()
        data = data[:-1]
        indicator_history = Indicator_History()

        
        exe_box = Query_Execution_Box(data)
        #print exe_box.indicators_data.keys()
        result_box = exe_box("macd(8,17) speed >= macd(8,17) speed 1 days_ago")
        result = result_box("rsi(14) is_crossing 50")
        
        self.failUnlessEqual(result.number_of_points, 46)
        #self.failUnlessEqual(result.number_of_points, 23)
        #print(result.data)
        #print(result.indicators_data.keys())
        self.failUnlessEqual(len(result.indicators_data), 2)
        self.failUnlessEqual(result.indicators_data.has_key(";macd(8,17);macd(8,17)"), True)
        self.failUnlessEqual(result.indicators_data.has_key(";rsi(14)"), True)
        self.failUnlessEqual(len(result.indicators_data[";macd(8,17);macd(8,17)"][0][-1]), 608)
        self.failUnlessEqual(result.indicators_data[";macd(8,17);macd(8,17)"][0][-1][400][1], 0.51649808583636059)
        

class Technical_Data_Test(TestCase):
    def test_technical_indicator_macd_can_be_parsed(self):
        parser = Parser()
        tokenizer = Tokenizer("macd(8,17)")
        indicator = parser.parse_indicator(tokenizer)
        self.assert_(indicator != None)

    def test_Given_date_ranges_and_symbol_and_technical_indicator_Then_the_technical_data_history_can_be_retrieved(self):           
        data = get_historical_prices(symbol="gld", start_date="20080101", end_date="20100601")
        data.reverse()
        data = data[:-1]
        indicator_history = Indicator_History()
        result = indicator_history.process_indicator_string("macd(8,17)", data)
        self.failUnlessEqual(len(result), 608)
        self.failUnlessEqual(result[400][1], 0.51649808583636059)
        
        data = get_historical_prices(symbol="gld", start_date="20080101", end_date="20100601")
        data.reverse()
        data = data[:-1]
        indicator_history = Indicator_History()
        result = indicator_history.process_indicator_string("rsi(14)", data)
        self.failUnlessEqual(len(result), 608)
        self.failUnlessEqual(result[400][1], 62.348797863808123)


class Service_Test(TestCase):
    def test_execute_query_returns_expected_results(self):
        service = Service()
        result = service.execute_query("GLD", "20090101", "20100301", ["macd(8,17) is_crossing macd_signal(8,17,9)"])
        self.failUnlessEqual(result.number_of_points, 28)
        
    def test_queries_can_be_logical_or(self):
        service = Service()
        result, indicators_data_list = service.execute_logical_or_queries("GLD", "20100101", "20100601", [["macd(8,17) is_crossing macd_signal(8,17,9)"], ["macd(8,17) >= macd_signal(8,17,9)"], None])
        
        count = 0
        for record in result:
            if record[-1]:
                count += 1
        
        self.failUnlessEqual(count, 63)  
        
    def test_live_data_point_is_not_requested(self):
        service = Service()
        ticker_data = service.get_ticker_data("GLD", "20090101", "20100301")
        result = service.live_data_point_is_requested(ticker_data, "20100301", "20100301")
        self.failUnlessEqual(result, False)

    def test_live_data_point_is_requested(self):
        service = Service()
        ticker_data = service.get_ticker_data("GLD", "20100101", "20100926")
        result = service.live_data_point_is_requested(ticker_data, "20100927", "20100927")
        self.failUnlessEqual(result, True)                  


class Backtester_Test(TestCase):
    def test_Given_a_flagged_history_data_designated_as_buy_points_and_a_flagged_history_data_designated_as_sell_points_Then_the_performance_can_be_backtested(self):
        service = Service()
        buy_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient >= 0"])
        sell_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient <= 0"])
        backtester = Backtester()
        account = TradingAccount(cash_balance=10000)
        timeline, summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account)        
        self.failUnlessEqual(summary["strategy_value"], "11639.67")
    
    def test_Given_a_stop_loss_Then_the_strategy_should_respect_it(self):
        service = Service()
        buy_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient >= 0"])
        sell_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient <= 0"])
        backtester = Backtester()
        account = TradingAccount(cash_balance=10000)
        timeline, summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account, stop_loss_percent=1)        
        self.failUnlessEqual(summary["strategy_value"], "11778.17")    
        
class Utils_Test(TestCase):
    def test_one_year_earlier_should_return_a_date_one_year_earlier(self):
        utils = Utils()
        year = utils.one_year_earlier("20000101")
        self.failUnlessEqual(year, "19990101")
        
    def test_remove_runway_should_remove_runway_records_until_the_start_date_in_the_list(self):     
        days = open(DATAFILE_PATH).readlines()
        data = [day[:-2].split(',') for day in days]
        data.reverse()
        data = data[:-1]
        
        utils = Utils()
        result = utils.remove_runway(data, "20100301")
        self.failUnlessEqual(len(result), 1)
        
    def test_given_indicators_data_when_nicks_specifications_are_applied_then_redundant_indicators_are_removed(self):
        service = Service()
        utils = Utils()
        buy_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient >= 0"])
        buy_points.indicators_data = utils.convert_indicators_data_to_nicks_specifications([buy_points.indicators_data])
        
        # results of buy_points.indicators_data should be:
        # [
        #   [
        #       ["macd(8,17)", [data]],
        #       ["macd_signal(8,17,9)", [data]]
        #   ]
        # ]
        
        self.failUnlessEqual(len(buy_points.indicators_data), 1)
        self.failUnlessEqual(len(buy_points.indicators_data[0]), 2)
        self.failUnlessEqual(buy_points.indicators_data[0][0][0], "macd(8,17)")
        self.failUnlessEqual(buy_points.indicators_data[0][1][0], "macd_signal(8,17,9)")
        
        
        # now test merging two indicators_data
        buy_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient >= 0"])
        sell_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient <= 0"])
        
        combined_indicators_data = utils.convert_indicators_data_to_nicks_specifications([buy_points.indicators_data, sell_points.indicators_data])
        
        self.failUnlessEqual(len(combined_indicators_data), 1)
        self.failUnlessEqual(len(combined_indicators_data[0]), 2)
        self.failUnlessEqual(combined_indicators_data[0][0][0], "macd(8,17)")
        self.failUnlessEqual(combined_indicators_data[0][1][0], "macd_signal(8,17,9)")
        
        # another test
        buy_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing macd_signal(8,17,9)", "macd(8,17) gradient >= 0"])
        sell_points = service.execute_query("GLD", "20090101", "20100801", ["macd(8,17) is_crossing_below 0"])
        
        combined_indicators_data = utils.convert_indicators_data_to_nicks_specifications([buy_points.indicators_data, sell_points.indicators_data])
        
        self.failUnlessEqual(len(combined_indicators_data), 1)
        self.failUnlessEqual(len(combined_indicators_data[0]), 2)
        self.failUnlessEqual(combined_indicators_data[0][0][0], "macd(8,17)")
        self.failUnlessEqual(combined_indicators_data[0][1][0], "macd_signal(8,17,9)")
        
    def test_given_two_query_results_data_Then_the_results_can_be_logically_ORed(self):
        service = Service()
        buy_points_1 = service.execute_query("GLD", "20100101", "20100601", ["macd(8,17) is_crossing macd_signal(8,17,9)"])
        buy_points_2 = service.execute_query("GLD", "20100101", "20100601", ["macd(8,17) >= macd_signal(8,17,9)"])
        
        utils = Utils()
        all_buy_points = utils.logical_or([buy_points_1.data, buy_points_2.data])
        
        count = 0
        for record in all_buy_points:
            if record[-1]:
                count += 1
        
        self.failUnlessEqual(count, 63)
        

        
            
                        

#from tests_web_api_01 import *
