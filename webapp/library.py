

# cache = {}
# 
# def get(key):
#       return cache[key]
#       
# def set_key(key, value):
#       pass
# #     if value != None:
# #             cache[key] = value

#-----------------------PRICE---------------------------
class Price(object):
    def __call__(self, past_data, latest_record, memo={}):
        return float(latest_record[1])
        
    def cut_data(self, unformatted_data):
        formatted_records = [(record[0], record[4]) for record in unformatted_data]
        #return formatted_records[:-1]
        return formatted_records
        
#-----------------------VOLUME--------------------------

class Volume(object):
    def __call__(self, past_data, latest_record, memo={}):
        return float(latest_record[1])
        
    def cut_data(self, unformatted_data):
        formatted_records = [(record[0], record[5]) for record in unformatted_data]
        return formatted_records                

#---------------------SMA FORMULAS-----------------------

class SmaDataFormatter(object):
    def cut(self, unformatted_records):
        formatted_records = [(record[0], record[4]) for record in unformatted_records]
        #formatted_records = formatted_records[:-1]
        return formatted_records


def sma_derive_key(pre_key, period):
    return "%s;sma;period=%s" % (pre_key, period)           
                            
class Sma(object):
    def __init__(self, period):
        self.period = period

    def __call__(self, past_data, latest_record, memo={}):
        if self.period - 1 > len(past_data):
            return None
        pre_key, value = latest_record
        key = sma_derive_key(pre_key, self.period)
        
        try:    
            return self.memo[key]
        except:
            pass

        # get the last period-1 number of records
        number_of_recent_entries = self.period - 1
        data = past_data[-number_of_recent_entries:]
        result = 0
        for record in data:
            record_key, value = record
            result += (float(value) / self.period)
        record_key, value = latest_record
        result += (float(value) / self.period)

        try:
            memo[key] = result
        except:
            pass
                    
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = SmaDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data   
        
        
#---------------------EMA FORUMLAS---------------------         

class EmaDataFormatter(object):
    def cut(self, unformatted_records):
        formatted_records = [(record[0], record[4]) for record in unformatted_records]
        #formatted_records = formatted_records[:-1]
        return formatted_records

def ema_derive_key(pre_key, period):
    return "%s;ema;period=%s" % (pre_key, period)           

class Ema_Value(object):
    def __init__(self, period):
        self.period = period
        

    def __call__(self, previous_ema, latest_record, memo={}):
        pre_key, value = latest_record
        key = ema_derive_key(pre_key, self.period)
        
        try:
            return memo[key]
        except:
            pass
    
        weight_current = float(2) / float(self.period + 1)
        weight_ma = float(1 - weight_current)
        result = (weight_current * float(value)) + (weight_ma * float(previous_ema))

        try:
            memo[key] = result
        except:
            pass
            
        return result
                        

class Ema(object):
    def __init__(self, period):
        self.period = period
        

    def __call__(self, past_data, latest_record, memo={}):
        pre_key, value = latest_record
        key = ema_derive_key(pre_key, self.period)
        
        try:
            return memo[key]
        except:
            pass
            
        ema_compute = Ema_Value(period=self.period)
        sma_compute = Sma(period=self.period)
        latest_ema = sma_compute(past_data=past_data[0:self.period-1], latest_record=past_data[self.period-1], memo=memo)
        
        for point in past_data[self.period:]:
            latest_ema = ema_compute(latest_ema, point, memo)       
        return ema_compute(latest_ema, latest_record, memo)


    def cut_data(self, unformatted_data):
        data_formatter = EmaDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
        
        
        
#-----------------------MACD FORMULAS-------------------------- 
class MacdDataFormatter(object):
    def cut(self, unformatted_records):
        formatted_records = [(record[0], record[4]) for record in unformatted_records]
        #formatted_records = formatted_records[:-1]
        return formatted_records


def macd_derive_key(pre_key, long_term_ma, short_term_ma, period=None):
    return "%s;macd;long_ma=%s;short_ma=%s;signal_period=%s" % (pre_key, long_term_ma, short_term_ma, period)

class Macd(object):
    def __init__(self, long_term_ma, short_term_ma):                
        self.long_term_ma = long_term_ma
        self.short_term_ma = short_term_ma
        
    def __call__(self, prices, latest_record, memo={}):
        pre_key, value = latest_record
        key = macd_derive_key(pre_key, self.long_term_ma, self.short_term_ma)
        
        try:
            return memo[key]
        except:
            pass
            
        ema = Ema(period=self.long_term_ma)
        long_term_ema_result = ema(past_data=prices, latest_record=latest_record, memo=memo)
        ema = Ema(period=self.short_term_ma)
        short_term_ema_result = ema(past_data=prices, latest_record=latest_record, memo=memo)
        result = short_term_ema_result - long_term_ema_result
        
        try:
            memo[key] = result
        except:
            pass
                    
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = MacdDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
                        

class Macd_Compute_All(object):
    def __init__(self, long_term_ma, short_term_ma):
        self.long_term_ma = long_term_ma
        self.short_term_ma = short_term_ma

        
    def __call__(self, prices, memo={}):    
        macd_list = []
        number_of_price_entries = len(prices)

        long_term_ema = Ema(period=self.long_term_ma)
        short_term_ema = Ema(period=self.short_term_ma)

        for i in range(self.long_term_ma, number_of_price_entries):
            long_term_ema_result = long_term_ema(past_data=prices[:i], latest_record=prices[i], memo=memo)
            short_term_ema_result = short_term_ema(past_data=prices[:i], latest_record=prices[i], memo=memo)                        
            macd = short_term_ema_result - long_term_ema_result

            pre_key, value = prices[i]
            key = macd_derive_key(pre_key, self.long_term_ma, self.short_term_ma)
            result = (key, macd)
            macd_list.append(result)                        

            try:
                memo[key] = macd
            except:
                pass
                        
        return macd_list
                

class Macd_Signal(object):
    def __init__(self, long_term_ma, short_term_ma, period):
        self.long_term_ma = long_term_ma
        self.short_term_ma = short_term_ma
        self.period = period

    def __call__(self, prices, latest_record, memo={}):
        pre_key, value = latest_record
        key = macd_derive_key(pre_key, self.long_term_ma, self.short_term_ma, self.period)
        try:
            return memo[key]
        except:
            pass
    
        macd_compute = Macd(long_term_ma=self.long_term_ma, short_term_ma=self.short_term_ma)
        macd_compute_all = Macd_Compute_All(long_term_ma=self.long_term_ma, short_term_ma=self.short_term_ma)

        latest_macd = (key, macd_compute(prices, latest_record, memo))
        list_of_macds = macd_compute_all(prices, memo)

        ema_compute_from_data = Ema(period=self.period)
        result = ema_compute_from_data(list_of_macds, latest_macd, memo)

        try:
            memo[key] = result
        except:
            pass    
            
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = MacdDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
                        

#----------------------------STOCHASTIC FORMULAS---------------------------------------

def hilo(past_data):
    high = low = None
    for record in past_data:
        if float(record[1]) > high or high == None:
            high = float(record[1])
        if float(record[2]) < low or low == None:
            low = float(record[2])
    return high, low

def stochastic_derive_key(pre_key, n, ma=None, ss_smoothing=None):
    return "%s;stochastic;n=%s;signal_ma=%s;ss_smoothing=%s" % (pre_key, n, ma, ss_smoothing)

    
class StochasticDataFormatter(object):
    def cut(self, unformatted_records):
        formatted_records = [(record[0], record[2], record[3], record[4]) for record in unformatted_records]
        #formatted_records = formatted_records[:-1]
        return formatted_records

class Stochastic(object):
    def __init__(self, n):
        self.n = n
                
    def cut_data(self, unformatted_data):
        data_formatter = StochasticDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
                
    def __call__(self, past_data, latest_record, memo={}):
        if self.n > len(past_data):
            raise RuntimeError
        date, hi, low, close = latest_record
        key = stochastic_derive_key(pre_key=date, n=self.n)
        
        try:
            return memo[key]
        except:
            pass
    
        past_data.append(latest_record)
        highest_high, lowest_low = hilo(past_data[-self.n:])
        latest_close = float(latest_record[3])
        past_data.pop()
        result = ((latest_close - lowest_low) / (highest_high - lowest_low)) * 100
        
        try:
            memo[key] = result
        except:
            pass

        return result
        

class Stochastic_Compute_All(object):
    def __init__(self, n):
        self.n = n

    def __call__(self, past_data, memo={}):
        stochastic_list = []
        stochastic = Stochastic(self.n)
        for i in range(self.n, len(past_data)):
            stoch = stochastic(past_data[:i], latest_record=past_data[i], memo=memo)
            date, hi, low, close = past_data[i]
            key = stochastic_derive_key(pre_key=date, n=self.n)
            result = (key, stoch)
            stochastic_list.append(result)
        return stochastic_list
        
        
class Stochastic_Signal(object):
    def __init__(self, smoothing, n):
        self.smoothing = smoothing
        self.n = n              

    def __call__(self, past_data, latest_record, memo={}):
        date, hi, low, close = latest_record
        key = stochastic_derive_key(pre_key=date, n=self.n, ma=self.smoothing)
        
        try:
            return memo[key]
        except:
            pass
    
        stochastic_compute_all = Stochastic_Compute_All(n=self.n)
        list_of_stochastics = stochastic_compute_all(past_data, memo)
        stochastic = Stochastic(n=self.n)
        current_stochastic = stochastic(past_data, latest_record=latest_record, memo=memo)
        sma = Sma(period=self.smoothing)
        result = sma(list_of_stochastics, latest_record=(key, current_stochastic), memo=memo)

        try:
            memo[key] = result
        except:
            pass
            
        return result

    def cut_data(self, unformatted_data):
        data_formatter = StochasticDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
        
        
class Full_Stochastic(object):
    def __init__(self, n, ma):
        self.n = n
        self.ma = ma

    def __call__(self, past_data, latest_record, memo={}):
        full_stochastic = Stochastic_Signal(smoothing=self.ma, n=self.n)
        result = full_stochastic(past_data, latest_record, memo)
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = StochasticDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
                
        
class Full_Stochastic_Compute_All(object):
    def __init__(self, n, ma):
        self.n = n
        self.ma = ma
        
    def __call__(self, past_data, memo={}):
        full_stochastic_list = []
        full_stochastic = Full_Stochastic(n=self.n, ma=self.ma)
        for i in range(self.n, len(past_data)):
            slow_stoch = full_stochastic(past_data[:i], past_data[i], memo)
            date, hi, low, close = past_data[i]
            key = stochastic_derive_key(pre_key=date, n=self.n, ma=self.ma)
            result = (key, slow_stoch)
            full_stochastic_list.append(result)
        return full_stochastic_list

        
class Full_Stochastic_Signal(object):
    def __init__(self, n, ma, smoothing):
        self.ma = ma
        self.n = n
        self.smoothing = smoothing
        
    def __call__(self, past_data, latest_record, memo={}):
        date, hi, low, close = latest_record
        key = stochastic_derive_key(pre_key=date, n=self.n, ma=self.ma, ss_smoothing=self.smoothing)
        
        try:
            return memo[key]
        except:
            pass
    
        full_stochastic_compute_all = Full_Stochastic_Compute_All(n=self.n, ma=self.ma)
        list_of_full_stochastics = full_stochastic_compute_all(past_data, memo)
        full_stochastic = Full_Stochastic(n=self.n, ma=self.ma)
        current_full_stochastic = full_stochastic(past_data, latest_record=latest_record, memo=memo)
        sma = Sma(period=self.smoothing)
        result = sma(list_of_full_stochastics, latest_record=(key, current_full_stochastic), memo=memo)
        
        try:
            memo[key] = result
        except:
            pass
    
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = StochasticDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data
        


                
#----------------------------RSI FORMULAS-------------------------              
                
class RsiDataFormatter(object):
    def cut(self, unformatted_records):
        formatted_records = [(record[0], record[1], record[2], record[3], record[4]) for record in unformatted_records]
        #formatted_records = formatted_records[:-1]
        return formatted_records                

        
class Rs(object):
    def __init__(self, period):
        self.period = period

    def __call__(self, past_data, latest_record):
        previous_average_gain, previous_average_loss = self.first_average_gain_loss(past_data[:self.period+1])
        result = previous_average_gain / previous_average_loss

        for i in range(self.period+1, len(past_data)):
            if self.is_gain(past_data[i], past_data[i-1]):
                average_gain = ((previous_average_gain) * (self.period-1) + self.gain(past_data[i], past_data[i-1])) / self.period
                average_loss = ((previous_average_loss) * (self.period-1) + 0) / self.period
            else:
                average_loss = ((previous_average_loss) * (self.period-1) + self.loss(past_data[i], past_data[i-1])) / self.period
                average_gain = ((previous_average_gain) * (self.period-1) + 0) / self.period
            previous_average_gain, previous_average_loss = average_gain, average_loss

        if self.is_gain(latest_record, past_data[-1]):
            average_gain = ((previous_average_gain) * (self.period-1) + self.gain(latest_record, past_data[-1])) / self.period
            average_loss = ((previous_average_loss) * (self.period-1) + 0) / self.period
        else:
            average_loss = ((previous_average_loss) * (self.period-1) + self.loss(latest_record, past_data[-1])) / self.period
            average_gain = ((previous_average_gain) * (self.period-1) + 0) / self.period
    
        result = average_gain / average_loss
        return result           
        
    def first_average_gain_loss(self, past_data):
        average_gain = 0
        average_loss = 0
        
        for i in range(1, len(past_data)):                      
            if self.is_gain(past_data[i], past_data[i-1]):
                average_gain += self.gain(past_data[i], past_data[i-1])
            elif self.is_loss(past_data[i], past_data[i-1]):
                average_loss += self.loss(past_data[i], past_data[i-1])

        return average_gain / self.period, average_loss / self.period
        
    def is_gain(self, current_record, yesterday_record):
        return float(current_record[4]) > float(yesterday_record[4])
        
    def is_loss(self, current_record, yesterday_record):
        return not self.is_gain(current_record, yesterday_record)
        
    def gain(self, current_record, yesterday_record):
        return float(current_record[4]) - float(yesterday_record[4])
        
    def loss(self, current_record, yesterday_record):
        return float(yesterday_record[4]) - float(current_record[4])            
        
        
def rsi_derive_key(pre_key, period):
    return "%s;rsi;period=%s" % (pre_key, period)           
            
            
class Rsi(object):
    def __init__(self, period):
        self.period = period
        
    def __call__(self, past_data, latest_record, memo={}):
        date, open, hi, low, close = latest_record
        key = rsi_derive_key(pre_key=date, period=self.period)
        
        try:
            return memo[key]
        except:
            pass
    
        rs = Rs(self.period)
        result = 100 - (100 / (1 + rs(past_data=past_data, latest_record=latest_record)))
        
        try:
            memo[key] = result
        except:
            pass
    
        return result
        
    def cut_data(self, unformatted_data):
        data_formatter = RsiDataFormatter()
        formatted_data = data_formatter.cut(unformatted_data)
        return formatted_data   



#--------------------MODIFIERS---------------------

class Unit(object):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value
        
    def cut_data(self, raw_data):                   
        pass    
        
class Past(object):
    def __init__(self, operand, days_ago):
        self.operand = operand
        self.days_ago = days_ago
        
    def __call__(self, past_data, latest_record, memo={}):
        return self.operand(past_data[:-self.days_ago], latest_record=past_data[-self.days_ago], memo=memo)
        
    def cut_data(self, raw_data):                   
        try:
            return self.operand.cut_data(raw_data)
        except Exception as e:  
            raise e 
            
class Future(object):
    def __init__(self, operand, days_later, future_data):
        self.operand = operand
        self.days_later = days_later
        self.future_data = future_data
        
    def __call__(self, past_data, latest_record, memo={}):
        look_ahead_length = len(past_data) + self.days_later
#               print "past data length %s" % len(past_data)
#               print "look ahead length %s" % look_ahead_length
        if look_ahead_length > len(self.future_data) - 1:
            raise RuntimeError
        else:   
            data = self.future_data[:look_ahead_length + 1]
    #               print "data with future length %s" % len(data)
            data = self.cut_data(data)
            return self.operand(data[:-1], latest_record=data[-1], memo=memo)
    
    def cut_data(self, raw_data):                   
        try:
            return self.operand.cut_data(raw_data)
        except Exception as e:  
            raise e                                 
    
class Speed(object):
    def __init__(self, operand):    
        self.operand = operand
        
    def __call__(self, past_data, latest_record, memo={}):
        current_day = self.operand(past_data, latest_record, memo)
        back_day = self.operand(past_data[:-1], past_data[-1], memo)
        #print("%s %s %s" % (latest_record[0], current_day, back_day))
        speed = abs(self.operand(past_data, latest_record, memo) - self.operand(past_data[:-1], past_data[-1], memo))
        #print("%s speed is: %s" % (latest_record[0], speed))
        #speed = self.operand(past_data, latest_record, memo) - self.operand(past_data[:-1], past_data[-1], memo)
        return speed
                
    def cut_data(self, raw_data):                   
        try:
            return self.operand.cut_data(raw_data)
        except Exception as e:  
            raise e

class Gradient(object):
    def __init__(self, operand):    
        self.operand = operand
        
    def __call__(self, past_data, latest_record, memo={}):
#               print("%s %s - %s = %s" % (latest_record[0], self.operand(past_data, latest_record, memo), self.operand(past_data[:-1], past_data[-1], memo), self.operand(past_data, latest_record, memo) - self.operand(past_data[:-1], past_data[-1], memo)))
        return self.operand(past_data, latest_record, memo) - self.operand(past_data[:-1], past_data[-1], memo)
                
    def cut_data(self, raw_data):                   
        try:
            return self.operand.cut_data(raw_data)
        except Exception as e:  
            raise e
            
            
#----------------BASE OPERATOR----------------------

class Base_Operator(object):
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2
        
    def cut_data(self, raw_data):
        try:
            return self.operand1.cut_data(raw_data)
        except:
            pass
            
        try:
            return self.operand2.cut_data(raw_data)
        except Exception as e:  
            raise e 
            
#------------------ARITHOPERATORS--------------------------                                             
                
class Difference_Of(Base_Operator):
    def __init__(self, operand1, operand2):
        super(Difference_Of, self).__init__(operand1, operand2)

    def __call__(self, past_data, latest_record, memo={}):  
        return self.operand1(past_data, latest_record, memo) - self.operand2(past_data, latest_record, memo)

        
class Abs_Difference_Of(Base_Operator):
    def __init__(self, operand1, operand2):
        super(Abs_Difference_Of, self).__init__(operand1, operand2)

    def __call__(self, past_data, latest_record, memo={}):
        return abs(self.operand1(past_data, latest_record, memo) - self.operand2(past_data, latest_record, memo))
                


#-------------------BOOLOPERATORS---------------------------    
        
class Is_Less_Than_Or_Equal_To(Base_Operator):
    def __init__(self, operand1, operand2):
        super(Is_Less_Than_Or_Equal_To, self).__init__(operand1, operand2)
        
    def __call__(self, past_data, latest_record, memo={}):
        return self.operand1(past_data, latest_record, memo) <= self.operand2(past_data, latest_record, memo)
        
        
class Is_Greater_Than_Or_Equal_To(Base_Operator):
    def __init__(self, operand1, operand2):
        super(Is_Greater_Than_Or_Equal_To, self).__init__(operand1, operand2)

    def __call__(self, past_data, latest_record, memo={}):
        #print("%s %s %s %s" % (latest_record[0], self.operand1(past_data, latest_record, memo), self.operand2(past_data, latest_record, memo),
        #self.operand1(past_data, latest_record, memo) >= self.operand2(past_data, latest_record, memo)))
        return self.operand1(past_data, latest_record, memo) >= self.operand2(past_data, latest_record, memo)
        

class Is_Crossing(Base_Operator):
    def __init__(self, operand1, operand2):
        super(Is_Crossing, self).__init__(operand1, operand2)
        
    def __call__(self, past_data, latest_record, memo={}):
        current_operand1 = self.operand1(past_data, latest_record=latest_record, memo=memo)
        yesterday_operand1 = self.operand1(past_data[:-1], latest_record=past_data[-1], memo=memo)
        current_operand2 = self.operand2(past_data, latest_record=latest_record, memo=memo)
        yesterday_operand2 = self.operand2(past_data[:-1], latest_record=past_data[-1], memo=memo)
        
        #print "%s current operand1: %s, yesterday operand1: %s, current operand2: %s, yesterday operand2: %s" % (latest_record[0], current_operand1, yesterday_operand1, current_operand2, yesterday_operand2)
                
        if current_operand1 != None and yesterday_operand1 != None and current_operand2 != None and yesterday_operand2 != None:
            if current_operand1 >= current_operand2 and yesterday_operand1 <= yesterday_operand2:
                return True
            if current_operand1 <= current_operand2 and yesterday_operand1 >= yesterday_operand2:
                return True
        return False
        
class Is_Increasing(Base_Operator):
    def __init__(self, operand1):
        super(Is_Increasing, self).__init__(operand1, None)

    def __call__(self, past_data, latest_record, memo={}):
        current_operand1 = self.operand1(past_data, latest_record=latest_record, memo=memo)
        yesterday_operand1 = self.operand1(past_data[:-1], latest_record=past_data[-1], memo=memo)
        
        if current_operand1 > 0 and yesterday_operand1 > 0:
        #print("%s %s %s" % (latest_record[0], current_operand1, yesterday_operand1))
            return current_operand1 > yesterday_operand1
    
        if current_operand1 < 0 and yesterday_operand1 < 0:
            return current_operand1 > yesterday_operand1
    
        if current_operand1 > 0 and yesterday_operand1 < 0:
            return True
            
        if current_operand1 < 0 and yesterday_operand1 > 0:
            return False            
                    
                                            
class Is_Decreasing(Base_Operator):
    def __init__(self, operand1):
        super(Is_Decreasing, self).__init__(operand1, None)
        
    def __call__(self, past_data, latest_record, memo={}):
        is_increasing = Is_Increasing(self.operand1)
        return not is_increasing(past_data, latest_record, memo=memo)

        
class And(Base_Operator):
    def __init__(self, operand1, operand2):
        super(And, self).__init__(operand1, operand2)
        
    def __call__(self, past_data, latest_record, memo={}):
        return self.operand1(past_data, latest_record, memo) and self.operand2(past_data, latest_record, memo)
                

#------------------NULL EXPRESSION--------------------
class Null_Expression(object):
    def __call__(self, past_data, latest_record, memo={}):
        return True

    def cut_data(self, raw_data):   
        return raw_data
        
        

                        
