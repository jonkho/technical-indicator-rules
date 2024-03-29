from django.test import TestCase
from webapp.models import *
from datetime import datetime, timedelta
from decimal import *
from webapp.quotes import *
from webapp.library import *
from parser import *
from functools import partial
from webapp.quotes import *
from django.test import Client
from django.utils import simplejson as json
import os

APP_ROOT = os.path.realpath(os.path.dirname(__file__))
DATAFILE_PATH = APP_ROOT+"/test_data/data.txt"

class test_bed(TestCase):
    def test1(self):    
    
#         response = self.client.get("/query/", {"symbol":"gld", "start_date":"20100228", "end_date":"20100301", "buy_query":["macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0"], "sell_query":["macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient <= 0"]})
#         return_code = json.loads(response.content)
#         self.failUnlessEqual(int(return_code["value"]), 3000)
#         #self.failUnlessEqual(len(return_code["contents"]["data"]), 291)
#         print(return_code["contents"]["indicators_data"])
#         self.failUnlessEqual(return_code["contents"]["indicators_data"][0][0][0], "macd(17,8)")
#         self.failUnlessEqual(return_code["contents"]["indicators_data"][0][1][0], "macd_signal(17,8,9)")
        
#         days = open(DATAFILE_PATH).readlines()
#         data = [day[:-2].split(',') for day in days]
#         data.reverse()
#         data = data[:-1]
#         data_with_flag = []
#         for record in data:
#             record.append(None)
#             data_with_flag.append(record)
#         parser = Parser(data_with_flag)

        service = Service()
        utils = Utils()
  
 

        
#         result2 = service.execute_query("GLD", "20090101", "20100301", ["macd_signal(17,8,9) >= 0"])
#         self.failUnlessEqual(result2.number_of_points, 197)  
        
#         tokenizer = Tokenizer(query_text="macd(17,8)->ema(9) >= 0")
#         rule = parser.parse_query(tokenizer)
#         exe_box = Query_Execution_Box(data_with_flag)
#         result = exe_box.exe(rule) 
#         
#         result = service.execute_query("GLD", "20090101", "20100301", ["macd(17,8)->ema(9) >= 0"])
#         self.failUnlessEqual(result.number_of_points, 197)
        

#               buy_points = service.execute_query("GLD", "20100101", "20100601", "macd(17,8) is_crossing macd_signal(17,8,9)")
                
                
#               print buy_points.data
                #buy_points = service.execute_query("DIG", "20100101", "20100820", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0", "macd(17,8) <= 0")
                #buy_points = service.execute_query("DIG", "20100101", "20100820", "macd(17,8) speed is_increasing", "macd(17,8) gradient >= 0.5", "macd(17,8) is_crossing macd_signal(17,8,5)", "macd(17,8) <= 0", "full_stochastic(5,3) gradient >= 0")


#         buy_points = service.execute_query("ADBE", "20100101", "20100915", ["macd(17,8) is_crossing macd_signal(17,8,5)", "macd(17,8) gradient >= 0"])
#         sell_points = service.execute_query("ADBE", "20100101", "20100915", ["macd(17,8) speed is_decreasing", "full_stochastic(5,3) speed is_decreasing", "macd(17,8) >= 0"])
                

                #sell_points = service.execute_query("GLD", "20100101", "20100820", "full_stochastic(5,5) is_crossing 80", "full_stochastic(5,5) gradient <= 0")
                #sell_points = service.execute_query("DIG", "20100101", "20100820", "full_stochastic(5,5) gradient 1 days_ago >= 0", "full_stochastic(5,5) gradient <= 0")
                
                
        # buy_points = service.execute_query("BP", "20100101", "20100912", ["macd(17,8) is_crossing macd_signal(17,8,5)", "macd(17,8) gradient >= 0", "macd(17,8) <= 0", "full_stochastic(5,5) speed is_increasing"])
#         sell_points = service.execute_query("BP", "20100101", "20100912", ["macd(17,8) speed is_decreasing", "full_stochastic(5,3) speed is_decreasing", "macd(17,8) >= 0"])

#         buy_points = service.execute_query("gld", "20090101", "20101112", ["macd(17,8) 2 days_ago >= macd_signal(17,8,9) 2 days_ago", "macd(17,8) 3 days_ago >= macd_signal(17,8,9) 3 days_ago", "macd(17,8) 1 days_ago >= macd_signal(17,8,9) 1 days_ago", "macd(17,8) >= macd_signal(17,8,9)"])
#         sell_points = service.execute_query("gld", "20090101", "20101112", ["macd(17,8) is_crossing macd_signal(17,8,9)"])
#        
#                 
#         backtester = Backtester()
#         account = Account(cash_balance=10000)
#         timeline, account_summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account)
#         print account_summary
#               
#               self.failUnlessEqual(summary, "100")
                
#               short_points = service.execute_query("GLD", "20100101", "20100820", "macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient <= 0", "macd(17,8) >= 0")
#               print short_points.data
#               cover_points = service.execute_query("GLD", "20100101", "20100820", "full_stochastic(5,5) speed is_decreasing")
#               backtester = Backtester()
#               account = Account(cash_balance=10000)
#               summary = backtester.execute_short_strategy(short_points.data, cover_points.data, account)
#               print summary
                
#         rsi_points = service.execute_query("GLD", "20091101", "20100820", ["rsi(14) is_crossing 50", "rsi(14) gradient >= 0"])
#         print rsi_points.data
#         response = self.client.get("/query/", {"symbol":"orcl", "start_date":"20100101", "end_date":"20110101", "buy_query":["macd_histogram(17,8,9) is_increasing", "macd_histogram(17,8,9) <= 0", "macd_histogram(17,8,9) gradient is_increasing", "rsi(14) <= 40", "macd_histogram(17,8,9) gradient >= 0.01"]})
#                 
#         return_code = json.loads(response.content)
#         self.failUnlessEqual(int(return_code["value"]), 3000)
#         self.failUnlessEqual(len(return_code["contents"]["data"]), 291)

                

#         tokenizer = Tokenizer(query_text="macd_signal(17,8,9)->histogram >= 0")
#         parser = Parser()
#         rule = parser.parse_query(tokenizer)    
#         self.assert_(rule != None)
#         self.failUnlessEqual(parser.indicator_operands[0][0], "macd_signal(17,8,9)")
#         self.failUnlessEqual(parser.indicator_operands[1][0], "macd_signal(17,8,9)->histogram")
#         print parser.indicator_operands

                
    

from tests_web_api_01 import *
from tests_lib import *
from tests_model import *
