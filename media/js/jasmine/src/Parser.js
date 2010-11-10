function Tokenizer(query_text) {
    var pattern = /-?[0-9]\.[0-9]+|[0-9]+|[0-9]|->|>=|<=|-|\|-\||\w+/gi
    this.tokens = query_text.match(pattern);
}

Tokenizer.prototype.peek = function() {
    return this.tokens[0];    
};

Tokenizer.prototype.consume = function() {   
    this.tokens.shift();
};

Tokenizer.prototype.has_tokens = function() {
    return this.tokens.length > 0;
};




function Parser() {
}


Parser.prototype.is_indicator = function(token) {
    
    if (token == "macd" || token == "macd_signal" || token == "sma" || token == "ema" || token == "stochastic" || token == "stochastic_signal" || token == "slow_stochastic" || token == "slow_stochastic_signal" || token == "rsi" || token == "price") {
        return true;
    }
    return false;
}

Parser.prototype.is_arithoperator = function(token) {
    
    if (token == "-" || token == "|-|") {
        return true;
    }
    return false;
}


Parser.prototype.is_transform = function(token) {
    
    if (token == "ema" || token == "sma" || token == "macd" || token == "macd_signal") {
        return true;
    } 
    return false;
}


Parser.prototype.is_unsigned_integer = function(token) {
    return (token.toString().search(/^[0-9]+$/) == 0);
}


Parser.prototype.parse_query = function(tokenizer) {
    
    if (tokenizer.has_tokens == false) {
        return new NoDocumentation(); 
    }
    
    else {
        var documentation = this.parse_expression(tokenizer);
        return documentation;    
    }

};

Parser.prototype.parse_expression = function(tokenizer) {
    
    var thiss_doc = this.parse_operand(tokenizer);
    var bool_doc = this.parse_booloperator(tokenizer);
    
    if (tokenizer.has_tokens == true) {
        var that_doc = this.parse_operand(tokenizer);
        return new bool_doc(thiss_doc, that_doc);
    }
    
    else {
        return new bool_doc(thiss_doc);
    }
    
}


Parser.prototype.parse_operand = function(tokenizer) {
    
    var token = tokenizer.peek();
    
    if (this.is_indicator(token)) {
        return this.parse_indicator(tokenizer);
    }
}


Parser.prototype.parse_indicator = function(tokenizer) {
    
    var token = tokenizer.peek();
    tokenizer.consume();
    
    if (token == "macd") {
    
        var long_term_ma = this.parse_number(tokenizer);
        var short_term_ma = this.parse_number(tokenizer);
        return new MacdDoc(long_term_ma, short_term_ma);
    }
}


Parser.prototype.parse_booloperator = function(tokenizer) {
    var booloperator = tokenizer.peek()
    tokenizer.consume()
    
    if (booloperator == "is_increasing") {
        return IsIncreasingDoc;
    }
}


Parser.prototype.parse_number = function(tokenizer) {
    
    var number = tokenizer.peek();
    tokenizer.consume();
    
    if (this.is_unsigned_integer(number)) {
        return number; 
    }
    
    return;
       
}

