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

		expression_evaluator = Expression_Evaluator()
		expression = Is_Greater_Than_Or_Equal_To(operand1=Price(), operand2=Unit(120))
		result = expression_evaluator.is_true(symbol="gld", expression=expression, today="20100703")
		#print result
# 		result = get_quote("gld")
# 		print result
		
		


from tests_web_api_01 import *
from tests_lib import *