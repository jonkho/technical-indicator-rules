from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from webapp.models import *
from django.utils import simplejson as json



class Api_01_Test(TestCase):
	def setUp(self):
		self.client = Client()
	
	def test_api_ticker_data_success(self):
		response = self.client.get("/ticker/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100101"})
		return_code = json.loads(response.content)
		self.failUnlessEqual(int(return_code["value"]), 1000)
		self.failUnlessEqual(len(return_code["contents"]), 252)
		
		
		
	def test_api_technical_indicator_data_success(self):
		response = self.client.get("/indicator/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100101", "indicator_string":"macd(17,8)"})
		return_code = json.loads(response.content)
		self.failUnlessEqual(int(return_code["value"]), 2000)
		self.failUnlessEqual(len(return_code["contents"]), 252)
		#print return_code["contents"]
		
	
	def test_api_query_results_success(self):
		response = self.client.get("/query/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100301", "query":"macd(17,8) is_crossing macd_signal(17,8,9)"})
		return_code = json.loads(response.content)
		self.failUnlessEqual(int(return_code["value"]), 3000)
		self.failUnlessEqual(len(return_code["contents"]["data"]), 291)
		
		# tests to describe the indicators data returned
		# indicators_data is a dictionary with the indicator string as the key.
		# using the test above, indicators_data looks: 
		# { 
		#	"macd(17,8)": ("macd", "macd(17,8)", [(2009-01-01, 0.50), (date, value), (...)]),
		#	"macd_signal(17,8,9)": ("macd_signal", "macd_signal(17,8,9)", "[(2009-01-01, 0.70), (date, value), (...)]")	
		# }
		
		
		# confirm there is macd and macd_signal historical data
		self.failUnlessEqual(len(return_code["contents"]["indicators_data"]), 2)
		self.failUnlessEqual(return_code["contents"]["indicators_data"].has_key("macd(17,8)"), True)
		self.failUnlessEqual(return_code["contents"]["indicators_data"].has_key("macd_signal(17,8,9)"), True)
		
		# confirm the 3-tuple of ("macd", "macd(17,8)", data) exists
		self.failUnlessEqual(len(return_code["contents"]["indicators_data"]["macd(17,8)"]), 3)
		self.failUnlessEqual(len(return_code["contents"]["indicators_data"]["macd_signal(17,8,9)"]), 3)
		
		# confirm the 3-tuple values are correct
		self.failUnlessEqual(return_code["contents"]["indicators_data"]["macd(17,8)"][0], "macd")
		self.failUnlessEqual(return_code["contents"]["indicators_data"]["macd(17,8)"][1], "macd(17,8)")
		self.failUnlessEqual(len(return_code["contents"]["indicators_data"]["macd(17,8)"][2]), 291)
		
		self.failUnlessEqual(return_code["contents"]["indicators_data"]["macd_signal(17,8,9)"][0], "macd_signal")
		self.failUnlessEqual(return_code["contents"]["indicators_data"]["macd_signal(17,8,9)"][1], "macd_signal(17,8,9)")
		self.failUnlessEqual(len(return_code["contents"]["indicators_data"]["macd_signal(17,8,9)"][2]), 291)
		
		
		
