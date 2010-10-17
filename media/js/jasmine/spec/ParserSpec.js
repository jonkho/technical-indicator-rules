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
        expect(tokenizer.peek()).toEqual("14")
        
    });
    
});  
  