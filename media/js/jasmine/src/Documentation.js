function Modifiers() {
    this.days_ago_with_comma = "";
    this.change_no_comma = "";
    this.days_ago_no_comma = "";
    this.change_no_the = "";
    this.literal_days_ago = ""
}

Modifiers.prototype.set_days_ago = function(value) {
    this.days_ago_with_comma = " " + value + ",";
    this.days_ago_no_comma = " " + value;
    this.literal_days_ago = value.replace("back", "back's") + " ";
}

Modifiers.prototype.set_change = function(value) {
    this.change_no_comma = " the " + value;
    this.change_no_the = value + " ";
}






function EmaDoc(period) {
    this.text = period + " day Exponential Moving Average";
    this.hint = "Indicators moving above its averages are bullish signs."
    this.description = this.text + " is a weighted average of the price over the past " + period + " days with greater weight given to later days."
    this.description_lead_in = this.description + " " + this.hint; 
}

EmaDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " this average ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where this average ";
}

EmaDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};






function SmaDoc(period) {
    this.text = period + " day Simple Moving Average";
    this.hint = "Indicators moving above its averages are bullish signs."
    this.description = this.text + " is the mean of the price over the past " + period + " days."
    this.description_lead_in = this.description + " " + this.hint;
}

SmaDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " this average ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where this average ";    
}

SmaDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;  
}






function RsiDoc(period) {
    this.text = "Rsi(" + period + ")";
    this.hint = "A low rsi that is moving up above the 30 or 50 value is a bullish sign."
    this.description = this.text + " is the " + period + " day Relative Strength Index. This is the ratio of up versus down days for the past " + period + " days, expressed as a percentage.";
    this.description_lead_in = this.description + " " + this.hint;
}

RsiDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " this percentage ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where this percentage ";    

}

RsiDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;          
}






function StochasticDoc(period) {
    this.text = "Stochastic(" + period + ")";
    this.hint = "A lower percentile indicates a pullback is happening and an upward move could occur soon.";
    this.description = this.text + " is the percentile of where the price ranks over the past " + period + " days.";
    this.description_lead_in = this.description + " " + this.hint;
};

StochasticDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the percentile ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the percentile ";
};

StochasticDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};








function StochasticSignalDoc(period, n) {
    this.text = "Stochastic Signal(" + period + "," + n + ")";
    this.hint = "The Stochastic greater than the Stochastic Signal is a bullish sign.";
    this.description = this.text + " is the " + n + " day moving average of the Stochastic(" + period + ").";
    this.description_lead_in = this.description + " " + this.hint;
};

StochasticSignalDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

StochasticSignalDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};







function SlowStochasticDoc(period) {
    this.text = "Slow Stochastic(" + period + ")";
    this.hint = "The Slow Stochastic value less than 30 is considered oversold; a value over 70 is considered overbought. The Slow Stochastic that is increasing or is greater than the Slow Stochastic Signal is a bullish sign.";
    this.description = this.text + " is the 3 day moving average of the Stochastic(" + period + ").";
    this.description_lead_in = this.description + " " + this.hint; 
};


SlowStochasticDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

SlowStochasticDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};







function SlowStochasticSignalDoc(period, n) {
    this.text = "Slow Stochastic Signal(" + period + "," + n + ")"
    this.hint = "The Slow Stochastic that is greater than or crossing above the Slow Stochastic Signal is a bullish sign.";
    this.description = this.text + " is the " + n + " day moving average of the Slow Stochastic(" + period + ").";
    this.description_lead_in = this.description + " " + this.hint; 
}

SlowStochasticSignalDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

SlowStochasticSignalDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};






function PriceDoc() {
    this.text = "Price";
    this.hint = "Prices that are greater than or crossing above its moving averages (ema or sma )can be considered a bullish sign.";
    this.description = "Price is the price of the equity.";
    this.description_lead_in = this.description + " " + this.hint; 
}

PriceDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

PriceDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;    
};








function MacdDoc(short_ma, long_ma) {
    this.text = "MACD(" + short_ma + "," + long_ma + ")";
    this.hint = "The MACD is used to identify the start and end of trends. MACD greater than zero suggests an uptrend; MACD less than zero suggests a downtrend. A MACD that is deeply negative but is crossing strongly above the MACD Signal suggests a start of an bullish uptrend."
    this.description = "The Moving Average Convergence/Divergence (MACD) measures the convergence or divergence between a short and long moving average. " + this.text + " measures the convergence/divergence between the " + short_ma + " day and " + long_ma + " day moving average."
    this.description_lead_in = this.description + " " + this.hint;
}

MacdDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

MacdDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;
}






function MacdSignalDoc(short_ma, long_ma, n) {
    this.text = "MACD Signal(" + short_ma + "," + long_ma + "," + n + ")";
    this.hint = "A MACD that is greater than the MACD Signal suggests a bullish uptrend. A MACD that is less than the MACD Signal suggests a bearish downtrend."
    this.description = this.text + " is the " + n + " day moving average of the MACD(" + short_ma + "," + long_ma + ")."
    this.description_lead_in = this.description + " " + this.hint;
}

MacdSignalDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description_lead_in + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
        return this.description_lead_in;
    }
    return this.description_lead_in + " This rule selects the days where the " + this.text + " ";
};

MacdSignalDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return this.text;
}






function IsLessThanOrEqualToDoc(operand1, operand2) {
    this.text = "is less than or equal to ";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;    
};

IsLessThanOrEqualToDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + ".";   
};





function IsGreaterThanOrEqualToDoc(operand1, operand2) {
    this.text = "is greater than or equal to ";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;  
};

IsGreaterThanOrEqualToDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + ".";
}







function IsCrossingDoc(operand1, operand2) {
    this.text = "has crossed ";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;
};

IsCrossingDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + ".";
}







function IsCrossingAboveDoc(operand1, operand2) {
    this.text = "has crossed above ";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;
};

IsCrossingAboveDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + ".";
}







function IsCrossingBelowDoc(operand1, operand2) {
    this.text = "has crossed below ";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;
};

IsCrossingBelowDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + ".";
}






function DifferenceDoc(operand1, operand2) {
    this.text = "'s difference between ";
    this.description = this.text;
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;
};

DifferenceDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + " ";
}





function AbsoluteDifferenceDoc(operand1, operand2) {
    this.text = "'s absolute difference between ";
    this.description = this.text;
    this.description_lead_in = this.text;
    this.operand1 = operand1;
    this.operand2 = operand2;
}

AbsoluteDifferenceDoc.prototype.compose_lead_in = function() {
    return this.operand1.compose_lead_in() + this.description_lead_in + this.operand2.compose_literal() + " ";
}





function IsIncreasingDoc(operand) {
    this.text = "has increased over the previous day.";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand = operand;    
};

IsIncreasingDoc.prototype.compose_lead_in = function() {
    return this.operand.compose_lead_in() + this.description_lead_in;
}






function IsDecreasingDoc(operand) {
    this.text = "has decreased over the previous day.";
    this.description = this.text; 
    this.description_lead_in = this.text;
    this.operand = operand;    
};

IsDecreasingDoc.prototype.compose_lead_in = function() {
    return this.operand.compose_lead_in() + this.description_lead_in;
}






function FloatDoc(value) {
    this.text = value.toString();
    this.description = this.text;
    this.description_lead_in = this.text + " ";
};

FloatDoc.prototype.compose_lead_in = function() {
    return this.description_lead_in;
    
};

FloatDoc.prototype.compose_literal = function() {
    return this.text;
};







function DaysAgoDoc(value, operand) {
    this.text = value.toString() + " days ago";
    if (value == 1) {
        this.text = value.toString() + " day ago";
    }
    
    this.description = this.text;
    this.description_lead_in = this.text;
    this.operand = operand
};

DaysAgoDoc.prototype.compose_lead_in = function() {
    modifiers = new Modifiers();
    modifiers.days_ago = modifiers.set_days_ago(this.description_lead_in);
    return this.operand.compose_lead_in(modifiers);   
};

DaysAgoDoc.prototype.compose_literal = function() {
    modifiers = new Modifiers();
    modifiers.days_ago = modifiers.set_days_ago(this.description_lead_in);
    return this.operand.compose_literal(modifiers);
};






function SpeedDoc(operand) {
    this.text = "slope's steepness of";
    this.description = this.text;
    this.description_lead_in = this.text;
    this.operand = operand;
}

SpeedDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers == undefined) {
        modifiers = new Modifiers();
    }
    
    modifiers.speed = modifiers.set_change(this.description_lead_in);
    return this.operand.compose_lead_in(modifiers);
}

SpeedDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers == undefined) {
        modifiers = new Modifiers();
    }

    modifiers.days_ago = modifiers.set_change(this.description_lead_in);
    return this.operand.compose_literal(modifiers);
}






function ChangeDoc(operand) {
    this.text = "slope";
    this.description = this.text;
    this.description_lead_in = "the value of the slope (steepness) of";
    this.operand = operand;        
};

ChangeDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers == undefined) {
        modifiers = new Modifiers();   
    }
    
    modifiers.days_ago = modifiers.set_change(this.description_lead_in);
    return this.operand.compose_lead_in(modifiers);
}

ChangeDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers == undefined) {
        modifiers = new Modifiers();
    }

    modifiers.days_ago = modifiers.set_change(this.description_lead_in);
    return this.operand.compose_literal(modifiers);
}






function TransformDoc(operand1, operand2) {
    this.operand1 = operand1;
    this.operand2 = operand2;
    this.text = operand1.text + "'s " + operand2.text;
    this.description = this.text + " is the " + this.operand2.text + " of the " + this.operand1.text + ".";
}

TransformDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        return this.description + " " + this.operand2.hint + " This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " the " + this.text + " ";
    }
    return this.description + " " + this.operand2.hint + " This rule selects the days where its " + this.text + " ";


}

TransformDoc.prototype.compose_literal = function(modifiers) {
    return "its " + this.operand2.text;
}