from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from webapp.models import *
from django.utils import simplejson as json



class Api_01_Test(TestCase):
    def setUp(self):
        self.client = Client()
        
                
# 
#       def test_api_ticker_data_success(self):
#               response = self.client.get("/ticker/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100101"})
#               return_code = json.loads(response.content)
#               self.failUnlessEqual(int(return_code["value"]), 1000)
#               self.failUnlessEqual(len(return_code["contents"]), 252)
#               
#               
#               
#       def test_api_technical_indicator_data_success(self):
#               response = self.client.get("/indicator/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100101", "indicator_string":"macd(17,8)"})
#               return_code = json.loads(response.content)
#               self.failUnlessEqual(int(return_code["value"]), 2000)
#               self.failUnlessEqual(len(return_code["contents"]), 252)
#               #print return_code["contents"]


    def test_api_buy_query_results_success(self):
        response = self.client.get("/query/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100301", "buy_query_1":["macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0"]})
                
        return_code = json.loads(response.content)
        self.failUnlessEqual(int(return_code["value"]), 3000)
        self.failUnlessEqual(len(return_code["contents"]["data"]), 291)
                
                # tests to describe the indicators data returned
                # indicators_data is a dictionary with the indicator string as the key.
                # using the test above, indicators_data looks: 
                # [ 
                #       [
                #         ["macd(17,8)", [[2009-01-01, 0.50], [date, value], [...]]],
                #         ["macd_signal(17,8,9)", [[2009-01-01, 0.70], [date, value], [...]]]
                #       ]
                #       [
                #               other indicators on a separate chart if present         
                #       ]
                # ]             
                
                # confirm there is macd and macd_signal historical data
        #print(return_code["contents"]["indicators_data"])
        
        self.failUnlessEqual(len(return_code["contents"]["indicators_data"][0]), 2)
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][0][0], "macd(17,8)")
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][1][0], "macd_signal(17,8,9)")
        #print(return_code["contents"]["indicators_data"])
        self.failUnlessEqual(len(return_code["contents"]["indicators_data"][0][0][1]), 291)



                
    def test_api_sell_query_results_success(self):
        response = self.client.get("/query/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100301", "sell_query_1":["macd(17,8) is_crossing macd_signal(17,8,9)"]})
        return_code = json.loads(response.content)
        self.failUnlessEqual(int(return_code["value"]), 3000)
        self.failUnlessEqual(len(return_code["contents"]["data"]), 291)
                
                # tests to describe the indicators data returned
                # indicators_data is a dictionary with the indicator string as the key.
                # using the test above, indicators_data looks: 
                # [ 
                #       [
                #         ["macd(17,8)", [[2009-01-01, 0.50], [date, value], [...]]],
                #         ["macd_signal(17,8,9)", [[2009-01-01, 0.70], [date, value], [...]]]
                #       ]
                #       [
                #               other indicators on a separate chart if present         
                #       ]
                # ]
                
                
                # confirm there is macd and macd_signal historical data
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][0][0], "macd(17,8)")
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][1][0], "macd_signal(17,8,9)")
                
                # confirm all of the data is there and spot check a few values
        self.failUnlessEqual(len(return_code["contents"]["indicators_data"][0][0][1]), 291)             
                
    def test_api_buy_sell_query_results_success(self):
        response = self.client.get("/query/", {"symbol":"gld", "start_date":"20100228", "end_date":"20100301", "buy_query_1":["macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient >= 0"], "sell_query_1":["macd(17,8) is_crossing macd_signal(17,8,9)", "macd(17,8) gradient <= 0"]})
        return_code = json.loads(response.content)
        self.failUnlessEqual(int(return_code["value"]), 3000)
        self.failUnlessEqual(len(return_code["contents"]["data"]), 1)
        #print(return_code["contents"]["indicators_data"])
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][0][0], "macd(17,8)")
        self.failUnlessEqual(return_code["contents"]["indicators_data"][0][1][0], "macd_signal(17,8,9)")
                #print(return_code["contents"]["data"][290])
                
                
                
                
