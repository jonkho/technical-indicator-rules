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
		response = self.client.get("/indicator/", {"symbol":"gld", "start_date":"20090101", "end_date":"20100101", "indicator":"macd(17,8)"})
		return_code = json.loads(response.content)
		self.failUnlessEqual(int(return_code["value"]), 2000)
		self.failUnlessEqual(len(return_code["contents"]), 252)
		#print return_code["contents"]