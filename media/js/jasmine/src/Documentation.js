function Modifiers() {
    this.days_ago_with_comma = "";
    this.change_no_comma = "";
    this.days_ago_no_comma = "";
    this.change_no_the = "";
    this.literal_days_ago = "the day's "
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





function StochasticDoc(period) {
    this.text = "Stochastic(" + period + ")";
    this.description = this.text + " Stochastic(5) is the percentile of where the price ranks over the past " + period + " days. A lower percentile indicates that the price is relatively depressed and could be poised to move up. ";
    this.description_lead_in = this.description + "This rule selects the days where this percentile ";
};

StochasticDoc.prototype.compose_lead_in = function(modifiers) {
    if (modifiers != undefined) {
        this.description_lead_in = this.description + "This rule selects the days where" + modifiers.days_ago_with_comma + modifiers.change_no_comma + " this percentile ";
    }
    return this.description_lead_in;
};

StochasticDoc.prototype.compose_literal = function(modifiers) {
    if (modifiers != undefined) {
        return modifiers.literal_days_ago + modifiers.change_no_the + this.text;
    }
    
    return modifiers.literal_days_ago + this.text;    
};






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
    this.text = value.toString() + " days back";
    if (value == 1) {
        this.text = value.toString() + " day back";
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
    this.text = "absolute change of";
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
    this.text = "change";
    this.description = this.text;
    this.description_lead_in = "change in";
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
    this.text = operand1.text + "->" + operand2.text;
    this.description = this.text + "takes"
}

TransformDoc.prototype.compose_lead_in = function(modifiers) {

}