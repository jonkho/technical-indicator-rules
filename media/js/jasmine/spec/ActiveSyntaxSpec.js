describe("ActiveSyntax", function() {
    
    beforeEach(function() {

    });
   

    it("should be able to correctly give syntax from blank state", function() {
        var tokenizer = new Tokenizer("");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual("indicators,value"); 
    });

    
    it("should be able to correctly give syntax from indicator state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5)");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison,:days ago,:gradient,:transform"); 
    });

    
    it("should be able to correctly give syntax from arithmetic state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) - ");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual("stochastic,stochastic_signal,slow_stochastic,slow_stochastic_signal,:value"); 
    });
    
    it("should be able to correctly give syntax from after arithmetic state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) - slow_stochastic(4)");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison,:days ago,:gradient,:transform"); 
    });
    
    it("should be able to correctly give syntax from after arithmetic state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) - slow_stochastic(4) >=");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual("stochastic,stochastic_signal,slow_stochastic,slow_stochastic_signal,:value"); 
    });
    
    
    it("should be able to correctly give syntax from number of days ago state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) 2 ");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":days ago"); 
    });
    
    it("should be able to correctly give syntax from days ago state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) 2 days_ago");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison"); 
    });
    
    it("should be able to correctly give syntax from gradient state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) gradient");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison,:days ago"); 
    });
    
    it("should be able to correctly give syntax from transform state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) ->");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":transform_indicators"); 
    });
    
    it("should be able to correctly give syntax after transform state", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) -> macd(5,9) ");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":days ago,:gradient,:comparison,:arithmetic");
    });
    
    it("should be able to correctly give syntax after transform state modifier", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) -> macd(5,9) gradient ");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison,:days ago");
    });  
    
    it("should be able to correctly give syntax after transform state comparison", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) -> macd(5,9) gradient >= ");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual("stochastic,stochastic_signal,slow_stochastic,slow_stochastic_signal,:value");
    });
    
    it("should be able to correctly give syntax after transform state comparison second indicator", function() {
        var tokenizer = new Tokenizer("slow_stochastic(5) -> macd(5,9) gradient >= slow_stochastic_signal(5,5)");
        var active_syntax = new ActiveSyntax();
        active_syntax.parse_phrase(tokenizer);
        
        expect(active_syntax.active_set).toEqual(":arithmetic,:comparison,:days ago,:gradient,:transform");
    });  
              
        
});