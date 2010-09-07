function chartData(rawJson) {
    rawJsonData = rawJson['data'];
    
    bgCount = 0;
    delta = 0;
    
    //process the raw json into our needed arrays
    for (i = 0; i < rawJsonData.length; i++) {
      r = rawJsonData[i];
      jsonData[i] = {
        date:r[0],
        open:parseFloat(r[1]),
        high:parseFloat(r[2]),
        low:parseFloat(r[3]),
        close:parseFloat(r[4]),
        volume:parseInt(r[5]),
        aclose:parseFloat(r[6]),
        flag:parseInt(r[7])
      };
    }

    for (i = 0; i < jsonData.length; i++) {
      j = jsonData[i];
      priceData[i] = [i,j.open,j.high,j.low,j.close];
      volumeData[i] = [i,j.volume];
      summaryData[i] = [i, j.close];
      
      if (j.flag) {
        flagData.push([i, j.flag]);
      }
      
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
    
    if (bgCount > 0 && bgCount < rawJsonData.length) {
      delta = bgCount;
      l = bgData.length;
      bgData[l] = [rawJsonData.length - delta, delta];
    }
    
    for (i = 0; i < bgData.lenth; i++) {
      var bg = bgData[i];
    }

    /*
    for (i = 0; i < 100; i++) {
      j = Math.floor((i * jsonData.length) / 100);
      summaryData[i] = [i,jsonData[j].close];
    }
    */
    
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
        date = date[2]+"/"+date[1]+"/"+date[0];
        
        return date; 
    }
    
    HumbleFinance.init('finance', priceData, volumeData, summaryData, []);
    HumbleFinance.setFlags(flagData); 
    
    var xaxis = HumbleFinance.graphs.summary.axes.x;
    var prevSelection = HumbleFinance.graphs.summary.prevSelection;
    var xmin = 0;
    var xmax = jsonData.length - 1;
    var area = {
        x1: xmin,
        y1: 0,
        x2: xmax,
        y2: 0
    };
    
    HumbleFinance.graphs.summary.setSelection(area);
    
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