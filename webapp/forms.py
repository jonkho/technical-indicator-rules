from django import forms
from models import *
from quotes import *
	
class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

class ChartForm(forms.Form):
	start_date = forms.CharField(max_length=255, required=True, initial="20100101")
	end_date = forms.CharField(max_length=255, required=True, initial="20100601")
	symbol = forms.CharField(max_length=255, required=True)
	query = forms.CharField(max_length=255, required=False)

class DemoForm(forms.Form):
	start_date = forms.CharField(max_length=255, required=True)
	end_date = forms.CharField(max_length=255, required=True)
	symbol = forms.CharField(max_length=255, required=True)
	expression1 = forms.CharField(max_length=255, required=False)
	expression2 = forms.CharField(max_length=255, required=False)
	expression3 = forms.CharField(max_length=255, required=False)
	expression4 = forms.CharField(max_length=255, required=False)
	expression5 = forms.CharField(max_length=255, required=False)
	expression6 = forms.CharField(max_length=255, required=False)
	expression7 = forms.CharField(max_length=255, required=False)
	expression8 = forms.CharField(max_length=255, required=False)
	
	def save(self):
		data = get_historical_prices(symbol=self.cleaned_data["symbol"], start_date=self.cleaned_data["from_date"], end_date=self.cleaned_data["to_date"])
 		data.reverse()
 		data = data[:-1]
 		
 		box = Query_Execution_Box(data)
		result = box(self.cleaned_data["expression1"])(self.cleaned_data["expression2"])(self.cleaned_data["expression3"])(self.cleaned_data["expression4"])(self.cleaned_data["expression5"])(self.cleaned_data["expression6"])(self.cleaned_data["expression7"])(self.cleaned_data["expression8"])

		return result.data

		
	