priceData = [];
volumeData = [];
summaryData = [];
jsonData = [];
bgData = [];
flagData = [];

openData = [];
closeData = [];
highData = [];
lowData = [];

function showTour() {
	  Modalbox.show('/tour/', {title: 'WELCOME TO TRADESPARROW', width: 600});
	}

function tourStep(i) {
  if (i == 1) {
    $('symbol').prototip.show();
  }
  
  if (i == 4) {
    $('symbol').prototip.hide();
    $('start_date').prototip.show();
  }
  
  if (i == 7) {
    $('start_date').prototip.hide();
    $('end_date').prototip.show();
  }
  
  if (i == 10) {
    $('end_date').prototip.hide();
    $('query').prototip.show();
  }
  
  if (i == 16) {
    $('query').prototip.hide();
  }
  
  if (i < 20)
    window.setTimeout(function(){tourStep(++i);}, 1000)
}

function tourStart(tic) {
  Modalbox.hide();
  s = $('symbol');
  s.value = tic;

  window.setTimeout(function(){tourStep(1);}, 1000);
}
	
document.observe("dom:loaded", function() {		  
  new Tip($('symbol'), 'TICKER SYMBOL');
  new Tip($('start_date'), 'START DATE (YYYYMMDD)');
  new Tip($('end_date'), 'END DATE (YYYYMMDD)');
  new Tip($('query'), 'TYPE YOUR QUERY AND PRESS ENTER');
  
  document.observe('prototip:shown', function(event) {
    event.element().pulsate({pulses:2, duration: 1.5});
    $(event.element().prototip).appear({duration: 0.5}); // our target element, we shake it with Scriptaculous
  });
  
  document.observe('prototip:hidden', function(event) {
    $(event.element().prototip).fade({duration: 1.5}); // our target element, we shake it with Scriptaculous
  });

jQuery('document').ready(function(){

	/* load data if supplied */
	if(js){
		chartData(js.contents.data);
	}


	/* active query area */
	jQuery('.query_area').droppable({
		accept: 'ul.query_bank li',
		drop: function(event, ui){
			var li = jQuery(ui.draggable).clone();
			var query = jQuery(li).text();
			jQuery('<a href="" class="rm_query">x</a><input name="query" type="hidden" value="'+query+'"/>').prependTo(li);
			jQuery(this).append(li);
		}	
	});

	/* prepopulated queries */
	jQuery('ul.query_bank li').draggable({revert:true, helper: 'clone'});

	/* remove query from query area */
	jQuery('.rm_query').live('click',function(){
		jQuery(this).parent('li').remove();
		return false;
	});

  //check for cookie
	jar = new CookieJar({
	  expires:60*60*24*365,
	  path: '/'
	
	c = jar.get('firstvisit');
	if (c == null) {
	  //this is the first visit, show the tour
	  showTour();
	  jar.put('firstvisit', 1)
	}

	/* submit query */
	function formsub(){
		priceData = [];
		volumeData = [];
		summaryData = [];
		jsonData = [];
		bgData = [];
		flagData = [];

		openData = [];
		closeData = [];
		highData = [];
		lowData = [];

		jQuery.ajax({
			type: 'GET',
			url: jQuery(this).attr('action'),
			success: function(data){
				jQuery('#finance').html("<div id=\"labels\"><div id=\"dateRange\">&nbsp;</div></div>");
				delete rdata;
				chartData(data.contents.data);
			},
			dataType: 'json',
			data: jQuery(this).serialize()
		});
		
		return false;
	}
	
	jQuery('#queryform').submit(formsub);	
	

});
