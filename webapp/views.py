# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
from forms import *
import jsonpickle

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
			if user is not None and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect("/index/")		
	else:	
		form = LoginForm()
	return render_to_response("login.html", {"form":form}, context_instance=RequestContext(request))


'''
def demo(request):
	if request.method == "POST":
		form = DemoForm(request.POST)
		if form.is_valid():
			result = form.save()
	else:
		form = DemoForm()
		result = []
	return render_to_response("demo.html", {"form":form, "result":result}, context_instance=RequestContext(request))		
'''
	
	
@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login/")	


def chart(request):
	if request.method == "POST":
		pass
	else:
	    form = ChartForm()
	return render_to_response("chart.html", {"form":form}, context_instance=RequestContext(request))


def index(request):
	if request.method == "POST":
		pass
	return render_to_response("index.html", context_instance=RequestContext(request))

def demo(request):
	symbol = request.GET['symbol']
	service = Service()
	result = service.execute_query(symbol, start_date="20090101", end_date="20100301", query="rsi(14) is_crossing 50")
	return render_to_response("demo.html", {"result":jsonpickle.encode(Return_Code(value="3000", contents=result))}, context_instance=RequestContext(request))




@csrf_exempt
def ticker_data(request):
	if request.method == "POST":
		raise Http404
	else:
		
		try:
			symbol = request.GET["symbol"]
			start_date = request.GET["start_date"]
			end_date = request.GET["end_date"]
		except Exception as e:
			return HttpResponse(jsonpickle.encode(Return_Code(value="1001", contents=e)))	
		
		data = get_historical_prices(symbol=symbol, start_date=start_date, end_date=end_date)
 		data.reverse()
 		
 		try:
 			data = data[:-1]
 		except:
 			data = None
 		
 		return HttpResponse(jsonpickle.encode(Return_Code(value="1000", contents=data)))
 		
 		
@csrf_exempt
def indicator_data(request):
	if request.method == "POST":
		raise Http404
	else:
		try:
			symbol = request.GET["symbol"]
			start_date = request.GET["start_date"]
			end_date = request.GET["end_date"]
			indicator = request.GET["indicator"]
		except Exception as e:
			return HttpResponse(jsonpickle.encode(Return_Code(value="2001", contents=e)))	
		
		utils = Utils()
		# back date one year to converge to true values by the time we reach the start date
		runway_start_date = utils.one_year_earlier(start_date)
		data = get_historical_prices(symbol=symbol, start_date=runway_start_date, end_date=end_date)
 		data.reverse()
 		data = data[:-1]
 		
		indicator_history = Indicator_History()
  		indicator_data = indicator_history(indicator, data)
  		#print indicator_data
  		final_data = utils.remove_runway(indicator_data, start_date)
  		
 		return HttpResponse(jsonpickle.encode(Return_Code(value="2000", contents=final_data)))
		
@csrf_exempt
def query_data(request):		
	if request.method == "POST":
		raise Http404
	else:
		try:
			symbol = request.GET["symbol"]
			start_date = request.GET["start_date"]
			end_date = request.GET["end_date"]
			query = request.GET["query"]
		except Exception as e:
			return HttpResponse(jsonpickle.encode(Return_Code(value="3001", contents=e)))
		
		data = get_historical_prices(symbol=symbol, start_date=start_date, end_date=end_date)
 		data.reverse()
 		data = data[:-1]
 		
 		# add the extra flag for each record
 		data_with_flag = []
		for record in data:
  			record.append(None)
  			data_with_flag.append(record)
  			
  		box = Query_Execution_Box(data_with_flag)
 		query_result = box(query)
 		    
 		return HttpResponse(jsonpickle.encode(Return_Code(value="3000", contents=query_result)))	
  			
