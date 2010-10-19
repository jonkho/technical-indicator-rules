describe("Documentation", function() {
    
    beforeEach(function() {
        stochastic_doc = new StochasticDoc(5);
        float_doc = new FloatDoc(30);
        greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(stochastic_doc, float_doc);
    });
   
    it("should be able to construct a simple stochastic doc with no modifiers", function() {
       
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile is less than or equal to 30.");
    
    });
    
    
    it("should be able to construct a stochastic doc with days ago modifier on operand 1", function() {
        var days_ago_doc = new DaysAgoDoc(1, stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, float_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where 1 day back, this percentile is less than or equal to 30.");
    });
    
    it("should be able to construct a stochastic doc with days ago modifier on operand 1 and 2", function() {
        var days_ago_doc = new DaysAgoDoc(1, stochastic_doc);
        var days_ago_doc_2 = new DaysAgoDoc(2, stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc_2);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where 1 day back, this percentile is less than or equal to 2 days back's Stochastic(5).");
    });
    
    
    it("should be able to construct a stochastic doc with gradient modifier on operand 1", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(change_doc, float_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where the change in this percentile is less than or equal to 30.");
    });
    
    it("should be able to construct a stochastic doc with gradient modifier on operand 1 and 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(change_doc, change_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where the change in this percentile is less than or equal to the day's change in Stochastic(5).");
    });


    it("should be able to construct a stochastic doc with gradient and days modifier on operand 1 and 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, change_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where 1 day back, the change in this percentile is less than or equal to 1 day back's change in Stochastic(5).");
    });
    
    
    it("should be able to construct a stochastic doc with speed, and days modifier on operand 1 and 2", function() {
        var speed_doc = new SpeedDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, speed_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(days_ago_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where 1 day back, the absolute change of this percentile is less than or equal to 1 day back's absolute change of Stochastic(5).");
    });
    
    

    it("should be able to construct a float doc with gradient and days modifier on operand 2", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var days_ago_doc = new DaysAgoDoc(1, change_doc);
        var greater_than_or_equal_to_doc = new IsLessThanOrEqualToDoc(float_doc, days_ago_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("30 is less than or equal to 1 day back's change in Stochastic(5).");
    });
    
    
    it("should be able to construct a Greater Than Or Equal To doc", function() {
        var change_doc = new ChangeDoc(stochastic_doc);
        var greater_than_or_equal_to_doc = new IsGreaterThanOrEqualToDoc(change_doc, change_doc);
        
        expect(greater_than_or_equal_to_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where the change in this percentile is greater than or equal to the day's change in Stochastic(5).");
    });
    
    
    it("should be able to construct a Is Crossing Above doc", function() {
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_doc, float_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5) calculates the day's price as a percentile of the entire price range over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile has crossed above 30.");
    
    });
    
    
    it("should be able to construct a Is Crossing Below doc", function() {
        var is_crossing_below_doc = new IsCrossingBelowDoc(stochastic_doc, float_doc);
        expect(is_crossing_below_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile has crossed below 30.");
    
    });
    
    it("should be able to construct a Is Increasing doc", function() {
        var is_increasing_doc = new IsIncreasingDoc(stochastic_doc, float_doc);
        expect(is_increasing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile has increased over the previous day.");
    
    });
    
    
    it("should be able to construct a Is Decreasing doc", function() {
        var is_decreasing_doc = new IsDecreasingDoc(stochastic_doc, float_doc);
        expect(is_decreasing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile has decreased over the previous day.");
    
    });
    
    
    it("should be able to construct a Is Crossing doc", function() {
        var is_crossing_doc = new IsCrossingDoc(stochastic_doc, float_doc);
        expect(is_crossing_doc.compose_lead_in()).toEqual("Stochastic(5) is the percentile of where the price ranks over the past 5 days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. This rule selects the days where this percentile has crossed 30.");
    
    });

    it("should be able to construct a Transform doc", function() {
        var transform_doc = new TransformDoc(stochastic_doc, ema_doc);
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_doc, transform_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5)->ema(9) takes the day's Stochastic(5) and then calculates its 9 day exponential moving average.");
    
    });

/*
    it("should be able to construct a Transform doc", function() {
        var transform_doc = new TransformDoc(stochastic_doc, ema_doc);
        var is_crossing_above_doc = new IsCrossingAboveDoc(stochastic_doc, transform_doc);
        expect(is_crossing_above_doc.compose_lead_in()).toEqual("Stochastic(5)->ema(9) takes the day's Stochastic(5) and then calculates its 9 day exponential moving average. Indicators with values greater than its moving averages are generally bullish signs. This rule selects the days where the its Stochastic(5) has crossed above its 9 day exponential moving average.");
    
    });
*/
    
}); 