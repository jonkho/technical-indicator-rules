describe("Tokenizer", function() {
    
    beforeEach(function() {
        tokenizer = new Tokenizer("rsi(14) is_crossing 50");
    });
   
    it("should be able to count the number of tokens", function() {
       
        expect(tokenizer.tokens.length).toEqual(4);
    
    });
    
    it("should be able to know whether there are tokens", function() {
        
        expect(tokenizer.has_tokens()).toEqual(true);
       
    });
    
    it("should be able to peek at its leading token", function() {
    
         expect(tokenizer.peek()).toEqual("rsi");
    
    });
    
    it("should be able to consume a token", function() {
        
        tokenizer.consume();
        expect(tokenizer.peek()).toEqual("14");
        
    });
    
});  


describe("Parser", function() {

    beforeEach(function() {
        parser = new Parser();
    });
    
    it("should be able to discern an indicator token", function() {
        
        expect(parser.is_indicator("sma")).toEqual(true);
        
    });
    
    it("should be able to discern an arithoperator token", function() {
        
        expect(parser.is_arithoperator("|-|")).toEqual(true);
        
    });
    
    it("should be able to discern an transform token", function() {
        
        expect(parser.is_transform("macd")).toEqual(true);
        
    });
    
    it("should be able to discern an integer token", function() {
        
        expect(parser.is_unsigned_integer("5")).toEqual(true);
        
    });
    
    it("should be able to parse a simple phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14) is_increasing");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("");
        
    });   

});
  