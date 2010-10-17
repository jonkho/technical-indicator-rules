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
    
    var thiss_documentation = this.parse_operand(tokenizer);
    
}