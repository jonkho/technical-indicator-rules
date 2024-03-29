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
from sparrow.django_lean.experiments.models import Experiment, GoalRecord
from sparrow.django_lean.experiments.utils import WebUser
from django.core.cache import cache

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
    
def tour(request):
    GoalRecord.record("tour", WebUser(request))
    return render_to_response("tour.html", context_instance=RequestContext(request))
    
def cheatsheet(request):
    GoalRecord.record("cheatsheet", WebUser(request))
    return render_to_response("cheatsheet.html", context_instance=RequestContext(request))
    
def about(request):
    return render_to_response("about.html")

def demo(request):
    try:
        symbol = request.GET['symbol']
    except KeyError as e:
        symbol = 'dow'

    service = Service()
    utils = Utils()
    buy_points = service.execute_query(symbol, "20090101", "20100301",['rsi(14) is_crossing 50'])
    sell_points = service.execute_query(symbol, "20090101", "20100301", ['rsi(14) >= 70'], memo=buy_points.memo)
    backtester = Backtester()
    account = TradingAccount(cash_balance=10000)
    timeline, account_summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account)
    
    # FIX: need to merge with sell points as well
    indicators_data = utils.convert_indicators_data_to_nicks_specifications([buy_points.indicators_data, sell_points.indicators_data])
    result = {"data":timeline, "indicators_data":indicators_data, "summary":account_summary}
    cache.set('20090101;20100301;rsi(14)__is_crossing__50;rsi(14)__>=__70;', result, 30)

    #TODO: could not get the cache working for some reason????
    ''' 
    if cache.get('20090101;20100301;rsi(14)__is_crossing__50;rsi(14)__>=__70;') == None:
        service = Service()
        utils = Utils()
        buy_points = service.execute_query(symbol, "20090101", "20100301",['rsi(14) is_crossing 50'])
        sell_points = service.execute_query(symbol, "20090101", "20100301", ['rsi(14) >= 70'], memo=buy_points.memo)
        backtester = Backtester()
        account = Account(cash_balance=10000)
        timeline, account_summary = backtester.execute_long_strategy(buy_points.data, sell_points.data, account)
        
        # FIX: need to merge with sell points as well
        indicators_data = utils.convert_indicators_data_to_nicks_specifications(buy_points.indicators_data, sell_points.indicators_data)
        result = {"data":timeline, "indicators_data":indicators_data, "summary":account_summary}
        cache.set('20090101;20100301;rsi(14)__is_crossing__50;rsi(14)__>=__70;', result, 30)
    
    else:
        result = cache.get('20090101;20100301;rsi(14)__is_crossing__50;rsi(14)__>=__70;')        
    '''
    return render_to_response("demo.html", {'params': {'symbol':symbol, 'start_date': '20090101' ,'end_date': '20100301', 'buy_query':'rsi(14) is_crossing 50', 'sell_query':'rsi(14) >= 70'},"result":jsonpickle.encode(Return_Code(value="3000", contents=result))}, context_instance=RequestContext(request))

def alert(request):
    if request.method == 'GET':
        raise Http404
    else:
        GoalRecord.record("emailsubmitted", WebUser(request))
        email = request.POST['email']
        new_email = Email_Collector(email=email)
        new_email.save()
        return HttpResponse('ok')

@csrf_exempt
def query_data(request):        
    if request.method == "POST":
        raise Http404
    else:
        GoalRecord.record("query", WebUser(request))
        try:
            symbol = request.GET["symbol"]
            start_date = request.GET["start_date"].replace('/','')
            end_date = request.GET["end_date"].replace('/','')
            buy_query_1 = request.GET.getlist("buy_query_1")
            sell_query_1 = request.GET.getlist("sell_query_1")
            buy_query_2 = request.GET.getlist("buy_query_2")
            sell_query_2 = request.GET.getlist("sell_query_2")
            buy_query_3 = request.GET.getlist("buy_query_3")
            sell_query_3 = request.GET.getlist("sell_query_3")
            stop_loss_percent = request.GET.get("stop_loss_percent", None)
            
        except Exception as e:
            return HttpResponse(jsonpickle.encode(Return_Code(value="3001", contents=e)))
        
        utils = Utils()
        service = Service()
        buy_queries = []
        sell_queries = []

        if buy_query_1:
            buy_queries.append(buy_query_1)
        if buy_query_2:
            buy_queries.append(buy_query_2)
        if buy_query_3:
            buy_queries.append(buy_query_3)

        if sell_query_1:
            sell_queries.append(sell_query_1)
        if sell_query_2:
            sell_queries.append(sell_query_2)
        if sell_query_3:
            sell_queries.append(sell_query_3)
        
        if buy_queries and sell_queries:
            all_buy_points, buy_indicators_data_list = service.execute_logical_or_queries(symbol, start_date, end_date, buy_queries)
            all_sell_points, sell_indicators_data_list = service.execute_logical_or_queries(symbol, start_date, end_date, sell_queries)

            for indicators_data in sell_indicators_data_list:
			    buy_indicators_data_list.append(indicators_data)

            backtester = Backtester()
            account = TradingAccount(cash_balance=10000)
            timeline, account_summary = backtester.execute_long_strategy(all_buy_points, all_sell_points, account, stop_loss_percent)
	 
            indicators_data = utils.convert_indicators_data_to_nicks_specifications(buy_indicators_data_list)
            result = {"data":timeline, "indicators_data":indicators_data, "summary":account_summary}

        elif buy_queries and not sell_queries:
            all_buy_points, buy_indicators_data_list = service.execute_logical_or_queries(symbol, start_date, end_date, buy_queries)
            indicators_data = utils.convert_indicators_data_to_nicks_specifications(buy_indicators_data_list)
            result = {"data":all_buy_points, "indicators_data":indicators_data, "summary":None}

        elif not buy_queries and sell_queries:
            all_sell_points, sell_indicators_data_list = service.execute_logical_or_queries(symbol, start_date, end_date, sell_queries)
            indicators_data = utils.convert_indicators_data_to_nicks_specifications(sell_indicators_data_list)
            result = {"data":all_sell_points, "indicators_data":indicators_data, "summary":None}

        return HttpResponse(jsonpickle.encode(Return_Code(value="3000", contents=result)))    

class EngagementScoreCalculator(object):
    def calculate_user_engagement_score(self, user, start_date, end_date):
        """
        TODO: come up with a real measurement
        """

        days_in_period = (end_date - start_date).days + 1
        return 0
