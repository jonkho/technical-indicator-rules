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
	
def tour(request):
	return render_to_response("tour.html", context_instance=RequestContext(request))

def demo(request):
	try:
		symbol = request.GET['symbol']
	except KeyError as e:
		symbol = 'dow'
	service = Service()
	result = service.execute_query(symbol, "20090101", "20100301", "rsi(14) is_crossing 50")
	return render_to_response("demo.html", {'params': {'symbol':symbol, 'start_date': '20090101' ,'end_date': '20100301', 'query':'rsi(14) is_crossing 50'},"result":jsonpickle.encode(Return_Code(value="3000", contents=result))}, context_instance=RequestContext(request))




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
			indicator_string = request.GET["indicator_string"]
		except Exception as e:
			return HttpResponse(jsonpickle.encode(Return_Code(value="2001", contents=e)))	
			
		service = Service()
		final_data = service.get_indicator_historical_data(symbol, indicator_string, start_date, end_date)	
  		
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
			query = request.GET.getlist("query")
		except Exception as e:
			return HttpResponse(jsonpickle.encode(Return_Code(value="3001", contents=e)))
		

		service = Service()
		query_result = service.execute_query(symbol, start_date, end_date, query) 
 		return HttpResponse(jsonpickle.encode(Return_Code(value="3000", contents=query_result)))	
  			
