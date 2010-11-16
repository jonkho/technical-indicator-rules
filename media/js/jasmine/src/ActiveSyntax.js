/*

indicators:
    macd(<number>,<number>) #commentary: parameters are long-term moving average, short-term moving averag
    macd_signal(<number>,<number>,<number>) #commentary: parameters are long-term moving average, short-term moving average, period
    sma(<number>)
    ema(<number>)
    stochastic(<number>)
    stochastic_signal(<number>, <number>) #commentary: parameters are n, smoothing
    slow_stochastic(<number>)
    slow_stochastic_signal(<number>,<number>)
    rsi(<number>)
    price

arithmetic:
    -
    \-\
    
comparison:
    >=
    <=
    is_crossing
    is_crossing_above
    is_crossing_below
    is_increasing
    is_decreasing
    
days ago:
    <number> days_ago

gradient:    
    gradient
    speed    

transform:
    ->
    
transform indicators:
    ema(<number>)
    sma(<number>)
    macd(<number>,<number>) 
    macd_signal(<number>,<number>,<number>)
    
value:
    <any real number>            

*/




function ActiveSyntax() {
    var active_set = ""
}


ActiveSyntax.prototype.is_indicator = function(token) {
    
    if (token == "macd" || token == "macd_signal" || token == "sma" || token == "ema" || token == "stochastic" || token == "stochastic_signal" || token == "slow_stochastic" || token == "slow_stochastic_signal" || token == "rsi" || token == "price") {
        return true;
    }
    return false;
}

ActiveSyntax.prototype.is_arithoperator = function(token) {
    
    if (token == "-" || token == "|-|") {
        return true;
    }
    return false;
}


ActiveSyntax.prototype.is_transform = function(token) {
    
    if (token == "ema" || token == "sma" || token == "macd" || token == "macd_signal") {
        return true;
    } 
    return false;
}

ActiveSyntax.prototype.is_modifier = function(token) {

    if (token == "speed" || token == "gradient" || this.is_unsigned_integer(token)) {
        return true;
    }
    return false;
}


ActiveSyntax.prototype.is_unsigned_integer = function(token) {
    return (token.toString().search(/^[0-9]+$/) == 0);
}


ActiveSyntax.prototype.parse_phrase = function(tokenizer) {
    this.active_set = "indicators,value"
    
    if (!tokenizer.has_tokens()) {
        return;
    }
    this.parse_expression(tokenizer);  

};

ActiveSyntax.prototype.parse_expression = function(tokenizer) {
    
    this.parse_operand(tokenizer);
    
    if (!tokenizer.has_tokens()) {
        return;
    }    
            
    this.parse_booloperator(tokenizer);
    
    if (!tokenizer.has_tokens()) {
        return;
    }
    
    this.parse_operand(tokenizer);
}


ActiveSyntax.prototype.parse_operand = function(tokenizer) {
    
    var token = tokenizer.peek();
    
    if (this.is_indicator(token)) {
        this.parse_indicator(tokenizer);
        
        if (!tokenizer.has_tokens()) {  
            return;
        }
        
        token = tokenizer.peek();
        
        if (!this.is_modifier(token) && !this.is_arithoperator(token)) {
            return;
        }
        
        if (this.is_modifier(token)) {
            this.parse_modifier(tokenizer);
            
            if (tokenizer.has_tokens()) {
                token = tokenizer.peek();
            }       
        }
        
        if (this.is_arithoperator(token)) {
            this.parse_arithoperator(tokenizer);
            
            if (!tokenizer.has_tokens()) {
                return
            }
            
            this.parse_operand(tokenizer);
            return;
        }
    }
    
    else {
        this.parse_unit(tokenizer)    
    }
        
}


ActiveSyntax.prototype.parse_indicator = function(tokenizer) {
    
    var token = tokenizer.peek();
    tokenizer.consume();
    
    if (token == "macd") {
        var short_term_ma = this.parse_number(tokenizer);
        var long_term_ma = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "macd_signal") { 
        var short_term_ma = this.parse_number(tokenizer);
        var long_term_ma = this.parse_number(tokenizer);
        var n = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "ema") {
        var period = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "sma") {
        var period = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "rsi") {
        var period = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "stochastic") {
        var period = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "stochastic_signal") {
        var period = this.parse_number(tokenizer);
        var n = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "slow_stochastic") {
        
        var period = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "slow_stochastic_signal") {
        var period = this.parse_number(tokenizer);
        var n = this.parse_number(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else if (token == "price") {
        this.active_set = "arithmetic,comparison,days ago,gradient,transform";
    }
    
    else {
        this.active_set = ""
        return;
    }
    
    if (!tokenizer.has_tokens()) {
        return;
    }
    
    token = tokenizer.peek();
    
    if (token == "->") {
        tokenizer.consume();
        
        this.active_set = "transform";
        
        if (!tokenizer.has_tokens()) {
            return;
        }
        
        this.parse_transform(tokenizer) 
    }          
}


ActiveSyntax.prototype.parse_booloperator = function(tokenizer) {
    var booloperator = tokenizer.peek()
    tokenizer.consume()
    
    if (booloperator == "is_increasing") {
        this.active_set = "";
    }
    
    else if (booloperator == "is_decreasing") {
        this.active_set = "";
    }
    
    else if (booloperator == "is_crossing_above") {
        this.active_set = "indicators,value";
    }
    
    else if (booloperator == "is_crossing_below") {
        this.active_set = "indicators,value";
    }
    
    else if (booloperator == "is_crossing") {
        this.active_set = "indicators,value";
    }
    
    else if (booloperator == ">=") {
        this.active_set = "indicators,value";
    }
    
    else if (booloperator == "<=") {
        this.active_set = "indicators,value";
    }
    else {
        this.active_set = "";
    }
}


ActiveSyntax.prototype.parse_transform = function(tokenizer, indicator) {
    var token = tokenizer.peek();
    
    if (this.is_transform(token)) {
        var transform_indicator = this.parse_indicator(tokenizer);
        this.active_set = "arithmetic,comparison,days ago,gradient";
    }
    
    else {
        this.active_set = "";
        return;
    }
}



ActiveSyntax.prototype.parse_modifier = function(tokenizer) {
    
    var token = tokenizer.peek();
        
    if (token == "speed") {
        this.active_set = "arithmetic,comparison,days ago";
        tokenizer.consume();
        
        if (!tokenizer.has_tokens()) {
            return;
        }
        
        token = tokenizer.peek();
    }


    else if (token == "gradient") {
        this.active_set = "arithmetic,comparison,days ago";
        tokenizer.consume();
        
        if (!tokenizer.has_tokens()) {
            return;
        }
        
        token = tokenizer.peek();
           
    }
       
    if (this.is_unsigned_integer(token)) {
        this.active_set = "days ago";
        this.parse_day_displacement(tokenizer);
    }
    
    else {
        this.active_set = ""
    }
}


ActiveSyntax.prototype.parse_day_displacement = function(tokenizer) {

    var number = this.parse_number(tokenizer);
    this.active_set = "days ago";
    
    if (!tokenizer.has_tokens()) {
        return;
    }
    
    var token = tokenizer.peek();
    tokenizer.consume();
    
    if (token == "days_ago") {
        this.active_set = "arithmetic,comparison";
        return;
    }

    else if (token == "days_later") {
        this.active_set = "arithemtic,comparison";
        return;
    }
    
    else {
        this.active_set = "";
        return;
    }
        
}


ActiveSyntax.prototype.parse_arithoperator = function(tokenizer) {
    var token = tokenizer.peek();
    tokenizer.consume();
    
    if (token == "-") {
        this.active_set = "indicators,value";
    }
    
    else if (token == "|-|") {
        this.active_set = "indicators,value";
    }
    
    else {
        this.active_set = "";
    }
}



ActiveSyntax.prototype.parse_unit = function(tokenizer) {
    var float_value = this.parse_float(tokenizer)
    return new FloatDoc(float_value);
}


ActiveSyntax.prototype.parse_float = function(tokenizer) {
    var float_value = tokenizer.peek();
    tokenizer.consume();
    return float_value;
}


ActiveSyntax.prototype.parse_number = function(tokenizer) {
    
    var number = tokenizer.peek();
    tokenizer.consume();
    
    if (this.is_unsigned_integer(number)) {
        return number; 
    }
    
    return;
       
}