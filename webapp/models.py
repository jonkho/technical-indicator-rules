from django.db import models
from django.contrib.auth.models import User, UserManager
import sys, traceback
from datetime import datetime, timedelta
from parser import *
from webapp.quotes import *
import copy
# Create your models here.

class Utils(object):
    def convert_indicators_data_to_nicks_specifications(self, indicators_data):
        indicator_data_list = []    
        for phrase_indicator_key, indicator_record in indicators_data.items():
            indicator_data_list.append(indicator_record) 
        return indicator_data_list            

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
            
    def convert_query_flags_to_integer(self, data):
        for record in data:
            if record[-1] == True:
                record[-1] = 1
            else:
                record[-1] = 0
        return data  
        
               


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
        
    def process_indicator_string(self, indicator_string, data):
        parser = Parser()
        tokenizer = Tokenizer(indicator_string)
        indicator = parser.parse_indicator(tokenizer)   
        final_list = self.process_indicator(indicator, data)
        
        return final_list

        
    def process_indicator(self, indicator, data):
        final_list = []
        formatted_data = indicator.cut_data(data)
        
        for (counter, point) in enumerate(formatted_data):
            date = data[counter][0]
            
            try:
                indicator_value = indicator(formatted_data[:counter], formatted_data[counter], self.memo)
                date_value_pair = [date, indicator_value]
            except:
                date_value_pair = [date, None]
                
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
    
    def __init__(self, data, indicators_data=None):
        # data holds the running query result
        # number_of_points is the running count of the resulting number of points that is evaluated True
        # memo is the dictionary for memoization that must be passed to the scanner 
        # indicators_data holds the operands which are indicators and their data    
        self.memo = {}
        self.data = data
        
        if indicators_data:
            self.indicators_data = indicators_data
        else:
            self.indicators_data = {}   
            
        super(Query_Execution_Box, self).__init__() 
        
    def __call__(self, query_string):
        parser = Parser(self.data)
        tokenizer = Tokenizer(query_text=query_string)
        expression = parser.parse_query(tokenizer)
        
        # collect the indicator's data
        indicator_history = Indicator_History()
        indicator_history.memo = self.memo
        
        phrase_indicator_key = ""
        indicator_list = []
        
        # example for macd(17,8) is_crossing macd(17,8,9):
        # phrase_indicator_key = ";macd(17,8);macd_signal(17,8,9)"
        # indicator_list = [
        #                      ["macd(17,8)", [data]], 
        #                      ["macd_signal(17,8,9)", [data]]
        #                  ]
        for indicator_record in parser.indicator_operands:
            phrase_indicator_key = "%s;%s" % (phrase_indicator_key, indicator_record[0])
            indicator_data = indicator_history.process_indicator(indicator_record[-1], self.data)
            indicator_list.append([indicator_record[0], indicator_data])
        
        
        # search indicators_data to see if that phrase's indicators already exist, 
        # or whether the phrase indicators is already a substring of another existing phrase's indicators (in which case it's also redundant)
        is_redundant_indicator = False
        for indicator_chart_key, data in self.indicators_data.items():
            #print("%s, %s" % (phrase_indicator_key, indicator_chart_key))
            if phrase_indicator_key in indicator_chart_key:
                is_redundant_indicator = True
        
        # if in is not in the indicators_data, then add it
        if not is_redundant_indicator:    
            self.indicators_data[phrase_indicator_key] = indicator_list
        
        result = self.exe(expression)
        return result
        
    def exe(self, expression):
        formatted_data = expression.cut_data(self.data)
        scanner = Scanner()
        indexes = scanner.run(expression, formatted_data, self.memo)
        
        # initialize the records for this query's results
        this_querys_results = copy.deepcopy(self.data)
        for record in this_querys_results:
            record[-1] = False
                        
        for index in indexes:
            this_querys_results[index][-1] = True   
            
        # apply logical AND to this query's results to the running result 
        result = self.logical_and(this_querys_results, self.data)   

        # return    
        return Query_Execution_Box(data=result, indicators_data=self.indicators_data)   
            
        
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
            
class Service(object):
    def execute_query(self, symbol, start_date, end_date, query):

        # get the extra runway data
        utils = Utils()
        runway_start_date = utils.one_year_earlier(start_date)
        runway_data = get_historical_prices(symbol=symbol, start_date=runway_start_date, end_date=end_date)
        runway_data.reverse()
        runway_data = runway_data[:-1]

        
        # add the extra flag for each record
        data_with_flag = []
        for record in runway_data:
            record.append(None)
            data_with_flag.append(record)
            
        # execute the query 
        box = Query_Execution_Box(data_with_flag)
        
        for phrase in query:
            box = box(phrase)   
        
        # remove the runway from the result query data
        box.data = utils.remove_runway(box.data, start_date)
        
        # remove the runway from the result indicators data
        for phrase_indicator_key, indicator_record in box.indicators_data.items():
            for indicator_string_data_pair in indicator_record:
                indicator_string_data_pair[-1] = utils.remove_runway(indicator_string_data_pair[-1], start_date)
            #box.indicators_data[indicator][-1] = utils.remove_runway(indicator_record[-1], start_date)   
                
        
        # convert the box data boolean flags to integer flags
        box.data = utils.convert_query_flags_to_integer(box.data)
        
#         i = 0
#         temp = ["i"]
#         for x in box.indicators_data.keys():
#             temp.append(x)
#         
#         size = len(box.indicators_data[x][2])
#         temp = [temp]
#         for y in range(size):
#             t2 = [i]
#             for x in box.indicators_data.keys():
#                 t2.append(box.indicators_data[x][2][y][1])
#             i += 1
#             temp.append(t2)
#         
#         box.indicators_data = temp;
        
        return box
        
        
    def get_indicator_historical_data(self, symbol, indicator_string, start_date, end_date):
        utils = Utils()
        # back date one year to converge to true values by the time we reach the start date
        runway_start_date = utils.one_year_earlier(start_date)
        data = get_historical_prices(symbol=symbol, start_date=runway_start_date, end_date=end_date)
        data.reverse()
        data = data[:-1]
        
        indicator_history = Indicator_History()
        indicator_data = indicator_history.process_indicator_string(indicator_string, data)
        #print indicator_data
        final_data = utils.remove_runway(indicator_data, start_date)
        return final_data           
        
            
class Backtester(object):   
    def execute_long_strategy(self, buy_points, sell_points, account):
        timeline = copy.deepcopy(buy_points)
        
        # buy points are marked as "buy".
        # normalize other points by marking as None
        for day in timeline:
            if day[-1]:
                day[-1] = "buy"
            
            else:
                day[-1] = None  
        
        # sell points are marked as "sell"
        for (counter, day) in enumerate(timeline):
            if sell_points[counter][-1]:
                day[-1] = "sell"
        
        #print timeline
        looking_to = "buy"
        
        for day in timeline:
            if looking_to == "buy" and day[-1] == "buy":
                account.buy_at_price(day[4])
                looking_to = "sell"
                print "%s bought at %s" % (day[0], day[4])
            
            elif looking_to == "sell" and day[-1] == "sell":
                account.sell_at_price(day[-4])
                looking_to = "buy"
                print "%s sold at %s" % (day[0], day[4])
                
        
        # convert timeline buy/sell/none to 1/2/0        
        for day in timeline:
            if day[-1] == "buy":
                day[-1] = 1
        
            elif day[-1] == "sell":
                day[-1] = 2
        
            else:
                day[-1] = 0
                                        
                
        return timeline, account.value(current_share_price=timeline[-1][4])
        
    def execute_short_strategy(self, short_points, cover_points, account):
        timeline = copy.deepcopy(short_points)
        
        for day in timeline:
            if day[-1]:
                day[-1] = "short"
            else:
                day[-1] = None
                
        for (counter, day) in enumerate(timeline):
            if cover_points[counter][-1]:
                day[-1] = "cover"   
                
        looking_to = "short"
        for day in timeline:
            if looking_to == "short" and day[-1] == "short":
                account.short_at_price(day[4])
                looking_to = "cover"
                print "%s shorted at %s" % (day[0], day[4])
            
            elif looking_to == "cover" and day[-1] == "cover":
                account.cover_at_price(day[-4])
                looking_to = "short"
                print "%s covered at %s" % (day[0], day[4])
                        
        return account.value(current_share_price=timeline[-1][4])
                            
    
        
class Account(object):
    def __init__(self, cash_balance=0, number_of_shares=0):
        self.cash_balance = float(cash_balance)
        self.number_of_shares = float(number_of_shares)
        
    def buy_at_price(self, price):
        price = float(price)
        self.number_of_shares = self.cash_balance / price
        self.cash_balance = 0
        return self.cash_balance, self.number_of_shares
    
    def sell_at_price(self, price):
        price = float(price)
        self.cash_balance = self.number_of_shares * price
        self.number_of_shares = 0
        return self.cash_balance,  self.number_of_shares
        
    def short_at_price(self, price):
        price = float(price)
        self.cash_balance += 10000
        self.number_of_shares = -10000 / price
        return self.cash_balance, self.number_of_shares
        
    def cover_at_price(self, price):
        price = float(price)
        self.cash_balance = self.cash_balance + (self.number_of_shares * price)
        self.number_of_shares = 0
        return self.cash_balance, self.number_of_shares     
        
    def value(self, current_share_price):
        current_share_price = float(current_share_price)
        return self.cash_balance + (self.number_of_shares * current_share_price)        
                    
                    
#   def intersection(self, data1, data2):
#       
#       # make lists of dates for easier set operations
#       data1_set = set([record[0] for record in data1])
#       data2_set = set([record[0] for record in data2])        
#       records_in_common = data1_set.intersection(data2_set)
#       result_dates = list(records_in_common)
#       result_dates.sort()
#       
#       # retrieve the records from data1 that corresponds to the result dates
#       result = []
#       data1_dict = {} # make a data1 dictionary keyed by date for O(n) performance
#       for record in data1:
#           data1_dict[record[0]] = record 
#       
#       for date in result_dates:
#           result.append(data1_dict[date])
#               
#       return result
#       

        


        
