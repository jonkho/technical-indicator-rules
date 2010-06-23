# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from models import *
from forms import *

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = auth.authenticate(username=request.POST["username"], password=request.POST["password"])
			if user is not None and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect("/demo/")		
	else:	
		form = LoginForm()
	return render_to_response("login.html", {"form":form}, context_instance=RequestContext(request))

@login_required
def demo(request):
	if request.method == "POST":
		form = DemoForm(request.POST)
		if form.is_valid():
			result = form.save()
	else:
		form = DemoForm()
		result = []
	return render_to_response("demo.html", {"form":form, "result":result}, context_instance=RequestContext(request))		
	
	
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login/")	
