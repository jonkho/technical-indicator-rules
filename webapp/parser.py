import re
from library import *



class Tokenizer(object):
    def __init__(self, query_text):
        if not query_text:
            query_text = ""
        self.tokens = re.findall(r'-?[0-9]\.[0-9]+|[0-9]+|[0-9]|->|>=|<=|-|\|-\||\w+', query_text)
        super(Tokenizer, self).__init__()
        
    def peek(self, ahead=0):
        try:
            return self.tokens[ahead]
        except:
            return None
        
    def consume(self):
        the_token = self.tokens[0]
        self.tokens.pop(0)
        return the_token
        
    def has_tokens(self):
        return len(self.tokens) > 0
        
class Parser(object):
    INDICATORS = ["macd", "macd_signal", "macd_histogram", "sma", "ema", "stochastic", "stochastic_signal", "full_stochastic", "full_stochastic_signal", "slow_stochastic", "slow_stochastic_signal","rsi", "price", "volume"]
    ARITHOPERATOR = ["-", "|-|"]
    TRANSFORMS = ["ema", "sma", "macd", "macd_signal"]
    
    
    def __init__(self, full_data=None):
        self.full_data = full_data
        self.indicator_operands = []
        super(Parser, self).__init__()
        
    def parse_query(self, tokenizer):
        self.indicator_operands = []
        
        if not tokenizer.has_tokens():
            return Null_Expression()                
    
        function = self.parse_expression(tokenizer)
        return function
        
    def parse_expression(self, tokenizer):
        thiss = self.parse_operand(tokenizer)
        booloperator = self.parse_booloperator(tokenizer)
        
        if tokenizer.has_tokens():
            that = self.parse_operand(tokenizer)
            return booloperator(operand1=thiss, operand2=that)
    
        else:
            return booloperator(operand1=thiss)     
    
    def parse_operand(self, tokenizer):
        token = tokenizer.peek()
        
        if token in self.INDICATORS:
            operand, s = indicator, s = self.parse_indicator(tokenizer)
            
            if not tokenizer.tokens:
                return operand
        
            token = tokenizer.peek()
            
            if not self.is_modifier(token) and not self.is_arithoperator(token):
                return operand
        
            if self.is_modifier(token):     
                operand = self.parse_modifier(tokenizer, operand)
                
                if tokenizer.has_tokens(): 
                    token = tokenizer.peek()        
    
            if self.is_arithoperator(token):
                arithoperator = self.parse_arithoperator(tokenizer)
                arithoperand = self.parse_operand(tokenizer)
                operand = arithoperator(operand, arithoperand)
                return operand          
        else:
            operand = self.parse_unit(tokenizer)
    
        return operand          

    def parse_indicator(self, tokenizer):
        token = tokenizer.peek()
        tokenizer.consume()
        #indicator_type = token
        
        if token == "macd":
            short_term_ma = self.parse_number(tokenizer)
            long_term_ma = self.parse_number(tokenizer)
            indicator = Macd(short_term_ma, long_term_ma)
            indicator_string = "macd(%s,%s)" % (short_term_ma, long_term_ma)
    
        elif token == "macd_signal":
            short_term_ma = self.parse_number(tokenizer)
            long_term_ma = self.parse_number(tokenizer)
            period = self.parse_number(tokenizer)
            indicator = Macd_Signal(short_term_ma, long_term_ma, period)
            indicator_string = "macd_signal(%s,%s,%s)" % (short_term_ma, long_term_ma, period)
            
        elif token == "macd_histogram":
            short_term_ma = self.parse_number(tokenizer)
            long_term_ma = self.parse_number(tokenizer)
            period = self.parse_number(tokenizer)
            indicator = Macd_Histogram(short_term_ma, long_term_ma, period)
            indicator_string = "macd_histogram(%s,%s,%s)" % (short_term_ma, long_term_ma, period)    
    
        elif token == "stochastic":
            n = self.parse_number(tokenizer)
            indicator = Stochastic(n)
            indicator_string = "stochastic(%s)" % n
    
        elif token == "stochastic_signal":
            n = self.parse_number(tokenizer)
            smoothing = self.parse_number(tokenizer)
            indicator = Stochastic_Signal(smoothing, n)
            indicator_string = "stochastic_signal(%s,%s)" % (n, smoothing)
    
        elif token == "full_stochastic":
            n = self.parse_number(tokenizer)
            ma = self.parse_number(tokenizer)
            indicator = Full_Stochastic(n, ma)
            indicator_string = "full_stochastic(%s,%s)" % (n, ma)
    
        elif token == "full_stochastic_signal":
            n = self.parse_number(tokenizer)
            ma = self.parse_number(tokenizer)
            smoothing = self.parse_number(tokenizer)
            indicator = Full_Stochastic_Signal(n, ma, smoothing)
            indicator_string = "full_stochastic_signal(%s,%s,%s)" % (n, ma, smoothing)
            
        elif token == "slow_stochastic":
            n = self.parse_number(tokenizer)
            indicator = Full_Stochastic(n, 3)
            indicator_string = "slow_stochastic(%s)" % n   
            
        elif token == "slow_stochastic_signal":
            n = self.parse_number(tokenizer)
            smoothing = self.parse_number(tokenizer)
            indicator = Full_Stochastic_Signal(n, 3, smoothing)
            indicator_string = "slow_stochastic_signal(%s,%s)" % (n, smoothing) 
                 
        elif token == "sma":
            period = self.parse_number(tokenizer)
            indicator = Sma(period)
            indicator_string = "sma(%s)" % period
    
        elif token == "ema":
            period = self.parse_number(tokenizer)
            indicator = Ema(period)
            indicator_string = "ema(%s)" % period   
    
        elif token == "price":
            indicator = Price()
            indicator_string = "price"              
    
        elif token == "volume":
            indicator = Volume()
            indicator_string = "volume"     
    
        elif token == "rsi":
            period = self.parse_number(tokenizer)
            indicator = Rsi(period)
            indicator_string = "rsi(%s)" % period    
            
        token = tokenizer.peek()
        
        if token == "->":
            tokenizer.consume()
            self.indicator_operands.append([indicator_string, indicator]) 
            indicator_string, indicator = self.parse_transform(tokenizer, indicator_string, indicator)      
            
        self.indicator_operands.append([indicator_string, indicator])   
        
        return indicator, indicator_string        
         
    def parse_transform(self, tokenizer, indicator_string, indicator):
        token = tokenizer.peek()
              
        if token == "histogram":
            tokenizer.consume()
            p = Parser()
            slow_signal, slow_signal_indicator_string = p.parse_indicator(Tokenizer(indicator_string))
            fast_signal, fast_signal_indicator_string = p.parse_indicator(Tokenizer(indicator_string.replace("_signal", "")))            
            indicator = Histogram(fast_signal, slow_signal)
            indicator_string = "%s->%s" % (indicator_string, token)
            
        elif token in self.TRANSFORMS:
            p = Parser()
            transform_indicator, transform_indicator_string = p.parse_indicator(tokenizer)
            transform_1 = Transform(indicator)
            transform_2 = transform_1.add(transform_indicator)
            indicator = transform_2
            indicator_string = "%s->%s" % (indicator_string, transform_indicator_string)
            
        return indicator_string, indicator     
                
    def parse_modifier(self, tokenizer, operand):
        modified_operand = operand
        token = tokenizer.peek()
        
        if token == "speed":
            modified_operand = Speed(modified_operand)
            tokenizer.consume()
            token = tokenizer.peek()
    
        elif token == "gradient":
            modified_operand = Gradient(modified_operand)
            tokenizer.consume()
            token = tokenizer.peek()        
    
        if self.is_number(token):
            #number = self.parse_number(tokenizer)
            modified_operand = self.parse_day_displacement(tokenizer, modified_operand)
    
        return modified_operand
        
    def parse_day_displacement(self, tokenizer, operand):
        number = self.parse_number(tokenizer)
        token = tokenizer.peek()
        tokenizer.consume()
        
        if token == "days_ago":
            return Past(operand, days_ago=number)
    
        elif token == "days_later":
            return Future(operand, days_later=number, future_data=self.full_data)           

    def parse_unit(self, tokenizer):
        float_value = self.parse_float(tokenizer)
        return Unit(float_value)                
                
    def parse_booloperator(self, tokenizer):
        booloperator = tokenizer.peek()
        tokenizer.consume()
        
        if booloperator == "is_crossing":
            return Is_Crossing
            
        elif booloperator == "is_crossing_above":
            return Is_Crossing_Above
        
        elif booloperator == "is_crossing_below":
            return Is_Crossing_Below        
    
        elif booloperator == "<=":
            return Is_Less_Than_Or_Equal_To
    
        elif booloperator == ">=":      
            return Is_Greater_Than_Or_Equal_To
    
        elif booloperator == "is_increasing":
            return Is_Increasing
    
        elif booloperator == "is_decreasing":
            return Is_Decreasing            

    def parse_arithoperator(self, tokenizer):
        token = tokenizer.peek()
        tokenizer.consume()
        
        if token == "-":
            return Difference_Of
    
        elif token == "|-|":
            return Abs_Difference_Of
            
    def parse_number(self, tokenizer):
        number = tokenizer.peek()
        tokenizer.consume()
        return int(number)      
        
    def parse_float(self, tokenizer):
        float_value = tokenizer.peek()
        tokenizer.consume()
        return float(float_value)               

    def is_number(self, token):
        try:
            days = int(token)
            return True
        except:
            return False            
                    
    def is_modifier(self, token):
        return token == "speed" or token == "gradient" or self.is_number(token)
                        
    def is_arithoperator(self, token):
        return token in self.ARITHOPERATOR
        
        
        
