from django.test import TestCase
from webapp.models import *

class Account_Test(TestCase):
    
    def test_account_should_be_able_to_add_sms_number(self):
        account = Account(username="jonkho", password="pass", sms="6143230129")
        
        self.failUnlessEqual(account.sms, "6143230129")  
        
    def test_account_should_be_able_to_add_symbols(self):
        account = Account(username="jonkho", password="pass", sms="6143230129")
        account.save()
        
        ibm = Symbol(account=account, string="ibm")
        ibm.save()
        
        goog = Symbol(account=account, string="goog")
        goog.save()
        
        self.failUnlessEqual(account.symbol_set.count(), 2)    
       