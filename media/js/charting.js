
priceData = [];
volumeData = [];
summaryData = [];
jsonData = [];
bgData = [];

openData = [];
closeData = [];
highData = [];
lowData = [];


function chartData(rawJsonData) {
    
    bgCount = 0;
    //prettyPrint();
    
    //process the raw json into our needed arrays
    for (i = 0; i < rawJsonData.length; i++) {
      r = rawJsonData[i];
      jsonData[i] = {date:r[0],open:r[1],high:r[2],low:r[3],close:r[4],volume:r[5],aclose:r[6],flag:r[7]};
    }

    for (i = 0; i < jsonData.length; i++) {
      j = jsonData[i];
      priceData[i] = [i,j.open,j.high,j.low,j.close];
      volumeData[i] = [i,j.volume];
      
      //count the number of consecutive flags and use them to tell flotr which columns should be filled
      if (j.flag) {
        bgCount++;
      } else {
        if (bgCount > 0) {
          delta = bgCount;
          l = bgData.length;
          bgData[l] = [i-delta, delta];
          bgCount = 0;
        }
      }
       
    }

    for (i = 0; i < 100; i++) {
      j = Math.floor((i * jsonData.length) / 100);
      summaryData[i] = [i,jsonData[j].close];
    }
    
    HumbleFinance.trackFormatter = function (obj) {
        
        var x = Math.floor(obj.x);
        var data = jsonData[x];
        var text = data.date + " Price: " + data.close + " Vol: " + data.volume;
        
        return text;
    };
    
    HumbleFinance.yTickFormatter = function (n) {
        
        if (n == this.axes.y.max) {
            return false;
        }
        
        return '$'+n;
    };
    
    HumbleFinance.xTickFormatter = function (n) { 
        
        if (n == 0) {
            return false;
        }
        
        var date = jsonData[n].date;
        date = date.split('-');
        date = date[0];
        
        return date; 
    }
    
    HumbleFinance.init('finance', priceData, volumeData, summaryData, bgData);
    //HumbleFinance.setFlags(flagData); 
    
    var xaxis = HumbleFinance.graphs.summary.axes.x;
    var prevSelection = HumbleFinance.graphs.summary.prevSelection;
    var xmin = xaxis.p2d(prevSelection.first.x);
    var xmax = xaxis.p2d(prevSelection.second.x);
    xmax = 40;
    
    $('dateRange').update(jsonData[xmin].date + ' - ' + jsonData[xmax].date);
    
    Event.observe(HumbleFinance.containers.summary, 'flotr:select', function (e) {
        
        var area = e.memo[0];
        xmin = Math.floor(area.x1);
        xmax = Math.ceil(area.x2);
        
        var date1 = jsonData[xmin].date;
        var date2 = jsonData[xmax].date;
        
        $('dateRange').update(jsonData[xmin].date + ' - ' + jsonData[xmax].date);
    });
    
}