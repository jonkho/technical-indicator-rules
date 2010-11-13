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
        
        expect(doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) has increased over the previous day.");
        
    });
    
    it("should be able to parse a simple is_crossing_above phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14) is_crossing_above macd_signal(5,14,9)");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) has crossed above MACD Signal(5,14,9).");
        
    });
    
    it("should be able to parse a gradient phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14) gradient is_crossing_above macd_signal(5,14,9) gradient");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the the value of the slope (steepness) of the MACD(5,14) has crossed above the value of the slope (steepness) of MACD Signal(5,14,9).");
        
    });
       
       
    it("should be able to parse a days_ago phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14) gradient 1 days_ago is_crossing_above macd_signal(5,14,9) gradient 1 days_ago");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where 1 day ago, the the value of the slope (steepness) of the MACD(5,14) has crossed above 1 day ago the value of the slope (steepness) of MACD Signal(5,14,9).");
        
    });
    
    
    it("should be able to parse a float phrase", function() {
        
        var tokenizer = new Tokenizer("1.2 <= macd_signal(5,14,9)");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("1.2 is less than or equal to MACD Signal(5,14,9).");
        
    });
    
    it("should be able to parse an arithoperator phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14) - macd_signal(5,14,9) >= 0.05");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) 's difference between MACD Signal(5,14,9) is greater than or equal to 0.05.");
        
    });
    
    
    it("should be able to parse an transform phrase", function() {
        
        var tokenizer = new Tokenizer("macd(5,14)->sma(5) >= macd_signal(5,14,9)");
        var doc = parser.parse_query(tokenizer);
        
        expect(doc.compose_lead_in()).toEqual("MACD(5,14)'s 5 day Simple Moving Average is the 5 day Simple Moving Average of the MACD(5,14). Indicators moving above its averages are bullish signs. This rule selects the days where its MACD(5,14)'s 5 day Simple Moving Average is greater than or equal to MACD Signal(5,14,9).");
        
    });
    
            

});
  