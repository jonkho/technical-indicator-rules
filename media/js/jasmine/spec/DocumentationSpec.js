describe("Documentation", function() {
    
    beforeEach(function() {
        stochastic_doc = new StochasticDoc(5);
        float_doc = new FloatDoc(30);
        ema_doc = new EmaDoc(10);
        greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(stochastic_doc, float_doc);
    });
   
    it("should be able to construct a simple stochastic doc with no modifiers", function() {
       
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile is less than or equal to 30.");
    
    });
    
    
    it("should be able to construct a stochastic doc with days ago modifier on operand 1", function() {
        var days_ago_doc = new DaysAgoDoc(1, stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, float_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where 1 day ago, the percentile is less than or equal to 30.");
    });
    
    it("should be able to construct a stochastic doc with days ago modifier on operand 1 and 2", function() {
        var days_ago_doc = new DaysAgoDoc(1, stochastic_doc);
        var days_ago_doc_2 = new DaysAgoDoc(2, stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc_2);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where 1 day ago, the percentile is less than or equal to 2 days ago Stochastic(5).");
    });
    
    
    it("should be able to construct a stochastic doc with gradient modifier on operand 1", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(change_doc, float_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the the value of the slope (steepness) of the percentile is less than or equal to 30.");
    });
    
    it("should be able to construct a stochastic doc with gradient modifier on operand 1 and 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(change_doc, change_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the the value of the slope (steepness) of the percentile is less than or equal to the value of the slope (steepness) of Stochastic(5).");
    });


    it("should be able to construct a stochastic doc with gradient and days modifier on operand 1 and 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, change_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where 1 day ago, the the value of the slope (steepness) of the percentile is less than or equal to 1 day ago the value of the slope (steepness) of Stochastic(5).");
    });
    
    
    it("should be able to construct a stochastic doc with speed, and days modifier on operand 1 and 2", function() {
        var speed_doc = new SpeedDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, speed_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where 1 day ago, the slope's steepness of the percentile is less than or equal to 1 day ago slope's steepness of Stochastic(5).");
    });
    
    

    it("should be able to construct a float doc with gradient and days modifier on operand 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, change_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(float_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("30 is less than or equal to 1 day ago the value of the slope (steepness) of Stochastic(5).");
    });
    
    
    it("should be able to construct a Greater Than Or Equal To doc", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsGreaterThanOrEqualToDoc(change_doc, change_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the the value of the slope (steepness) of the percentile is greater than or equal to the value of the slope (steepness) of Stochastic(5).");
    });
    
    
    it("should be able to construct a Is Crossing Above doc", function() {
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has crossed above 30.");
    
    });
    
    
    it("should be able to construct a Is Crossing Below doc", function() {
        var is_crossing_below_doc = new IsCrossingBelowDoc(stochastic_doc, float_doc);
        expect(is_crossing_below_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has crossed below 30.");
    
    });
    
    it("should be able to construct a Is Increasing doc", function() {
        var is_increasing_doc = new IsIncreasingDoc(stochastic_doc, float_doc);
        expect(is_increasing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has increased over the previous day.");
    
    });
    
    
    it("should be able to construct a Is Decreasing doc", function() {
        var is_decreasing_doc = new IsDecreasingDoc(stochastic_doc, float_doc);
        expect(is_decreasing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has decreased over the previous day.");
    
    });
    
    
    it("should be able to construct a Is Crossing doc", function() {
        var is_crossing_doc = new IsCrossingDoc(stochastic_doc, float_doc);
        expect(is_crossing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has crossed 30.");
    
    });

    it("should be able to construct a Transform doc", function() {
        var transform_doc = new TransformDoc(stochastic_doc, ema_doc);
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_doc, transform_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates a pullback is happening and an upward move could occur soon. This rule selects the days where the percentile has crossed above its 10 day Exponential Moving Average.");
    
    });

    it("should be able to construct a Transform doc with modifiers", function() {
        var transform_doc = new TransformDoc(stochastic_doc, ema_doc);
        var change_doc = new ChangeDoc(transform_doc);
        var change_doc2 = new ChangeDoc(stochastic_doc);
        var is_crossing_above_doc = new IsCrossingAboveDoc(change_doc, change_doc2);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5)'s 10 day Exponential Moving Average is the 10 day Exponential Moving Average of the Stochastic(5). Indicators moving above its averages are bullish signs. This rule selects the days where the the value of the slope (steepness) of the Stochastic(5)'s 10 day Exponential Moving Average has crossed above the value of the slope (steepness) of Stochastic(5).");
    
    });
    
    it("should be able to construct an sma doc", function() {
        var sma_doc = new SmaDoc(10);
        var is_crossing_above_doc = new IsCrossingAboveDoc(sma_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("10 day Simple Moving Average is the mean of the price over the past 10 days. Indicators moving above its averages are bullish signs. This rule selects the days where this average has crossed above 30.")
        
    });
    
    it("should be able to construct an rsi doc", function() {
        var rsi_doc = new RsiDoc(14);
        var is_crossing_above_doc = new IsCrossingAboveDoc(rsi_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Rsi(14) is the 14 day Relative Strength Index. This is the ratio of up versus down days for the past 14 days, expressed as a percentage. A low rsi that is moving up above the 30 or 50 value is a bullish sign. This rule selects the days where this percentage has crossed above 30.")
        
    });

    

    it("should be able to construct a stochastic signal doc", function() {
        var stochastic_signal_doc = new StochasticSignalDoc(10,5);
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_signal_doc, stochastic_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic Signal(10,5) is the 5 day moving average of the Stochastic(10). The Stochastic greater than the Stochastic Signal is a bullish sign. This rule selects the days where the Stochastic Signal(10,5) has crossed above Stochastic(5).")
    });
    
    
    it("should be able to construct a slow stochastic doc", function() {
        var slow_stochastic_doc = new SlowStochasticDoc(5);
        var is_crossing_above_doc = new IsCrossingAboveDoc(slow_stochastic_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Slow Stochastic(5) is the 3 day moving average of the Stochastic(5). The Slow Stochastic value less than 30 is considered oversold; a value over 70 is considered overbought. The Slow Stochastic that is increasing or is greater than the Slow Stochastic Signal is a bullish sign. This rule selects the days where the Slow Stochastic(5) has crossed above 30.");
    });
    
    
    it("should be able to construct a slow stochastic doc", function() {
        var slow_stochastic_doc = new SlowStochasticDoc(5);
        var slow_stochastic_signal_doc = new SlowStochasticSignalDoc(5, 7);
        var is_crossing_above_doc = new IsCrossingAboveDoc(slow_stochastic_signal_doc, slow_stochastic_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Slow Stochastic Signal(5,7) is the 7 day moving average of the Slow Stochastic(5). The Slow Stochastic that is greater than or crossing above the Slow Stochastic Signal is a bullish sign. This rule selects the days where the Slow Stochastic Signal(5,7) has crossed above Slow Stochastic(5).");
    });
    
    it("should be able to construct a macd doc", function() {
        var macd_doc = new MacdDoc(5, 14);
        var float_doc = new FloatDoc(0);
        var is_crossing_above_doc = new IsCrossingAboveDoc(macd_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) has crossed above 0.");
    });
    
    it("should be able to construct a Transform doc with macd", function() {
        var macd_doc = new MacdDoc(5, 14);
        var transform_doc = new TransformDoc(stochastic_doc, macd_doc);
        var change_doc = new ChangeDoc(transform_doc);
        var change_doc2 = new ChangeDoc(stochastic_doc);
        var is_crossing_above_doc = new IsCrossingAboveDoc(change_doc, change_doc2);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5)'s MACD(5,14) is the MACD(5,14) of the Stochastic(5). The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the the value of the slope (steepness) of the Stochastic(5)'s MACD(5,14) has crossed above the value of the slope (steepness) of Stochastic(5).");
    
    });
    
    
    it("should be able to construct a macd signal doc", function() {
        var macd_doc = new MacdDoc(5, 14);
        var macd_signal_doc = new MacdSignalDoc(5,14,9)
        var is_crossing_above_doc = new IsCrossingAboveDoc(macd_doc, macd_signal_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) has crossed above MACD Signal(5,14,9).");
    });    
    
    
    it("should be able to construct a macd signal doc 2", function() {
        var macd_doc = new MacdDoc(5, 14);
        var macd_signal_doc = new MacdSignalDoc(5,14,9)
        var is_crossing_above_doc = new IsCrossingAboveDoc(macd_signal_doc, macd_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("MACD Signal(5,14,9) is the 9 day moving average of the MACD(5,14). A MACD that is greater than the MACD Signal suggests a bullish uptrend. A MACD that is less than the MACD Signal suggests a bearish downtrend. This rule selects the days where the MACD Signal(5,14,9) has crossed above MACD(5,14).");
    }); 
    
    
    it("should be able to construct a difference doc", function() {
        var macd_doc = new MacdDoc(5, 14);
        var macd_signal_doc = new MacdSignalDoc(5,14,9);
        var difference_doc = new DifferenceDoc(macd_doc, macd_signal_doc);
        var greater_than_or_equal_to_doc = new IsGreaterThanOrEqualToDoc(difference_doc, float_doc);
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) 's difference between MACD Signal(5,14,9) is greater than or equal to 30.");
    }); 
    
    
    it("should be able to construct a absolute difference doc", function() {
        var macd_doc = new MacdDoc(5, 14);
        var macd_signal_doc = new MacdSignalDoc(5,14,9);
        var difference_doc = new AbsoluteDifferenceDoc(macd_doc, macd_signal_doc);
        var greater_than_or_equal_to_doc = new IsGreaterThanOrEqualToDoc(difference_doc, float_doc);
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. MACD(5,14) measures the convergence/divergence between the 5 day and 14 day moving average. The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend. This rule selects the days where the MACD(5,14) 's absolute difference between MACD Signal(5,14,9) is greater than or equal to 30.");
    }); 
    

    
    
}); 