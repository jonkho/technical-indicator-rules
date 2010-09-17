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
    $('querybank').prototip.show();
    $('query').prototip.show();
  }

  if (i == 16) {
    $('query').prototip.hide();
    $('querybank').prototip.hide();
    $('fsubmit').prototip.show();
  }

  if (i == 20) {
    $('fsubmit').prototip.hide();
  }

  if (i != 20) {
    window.setTimeout(function(){tourStep(++i);}, 1000);
  }
}

function tourStart(tic) {
  Modalbox.hide();
  s = $('symbol');
  s.value = tic;

  window.setTimeout(function(){tourStep(1);}, 1000);
}

jQuery('document').ready(function(){
	jQuery('div.container').css('min-width',jQuery('div.container').width());

  

  new Tip($('symbol'), 'TICKER SYMBOL');
  new Tip($('start_date'), 'START DATE (YYYYMMDD)');
  new Tip($('end_date'), 'END DATE (YYYYMMDD)');
  new Tip($('querybank'), 'DRAG FROM HERE');
  new Tip($('query'), "TO HERE");
  new Tip($('fsubmit'), "AND CLICK GO", {
    offset: {x:-110, y:0},
  });
  
  document.observe('prototip:shown', function(event) {
    event.element().pulsate({pulses:2, duration: 1.5});
  });

  jQuery('#start_date').datepicker({dateFormat: 'yymmdd'});
  jQuery('#end_date').datepicker({dateFormat: 'yymmdd'});

	/* load data if supplied */
	if(js){
	  chartData(js.contents);
	}

	/* active query area */
	jQuery('.query_area').droppable({
		accept: 'ul.query_bank li',
		drop: function(event, ui){
			var li = jQuery(ui.draggable).clone();
			var query = jQuery(li).text();
			if(jQuery(this).hasClass('buy_queries')){
				jQuery('<li><a href="" class="rm_query">x</a><input name="buy_query" type="hidden" value="'+query+'"/><p class="query_string">'+query+'</p></li>').appendTo(this);
			} else{
				jQuery('<li><a href="" class="rm_query">x</a><input name="sell_query" type="hidden" value="'+query+'"/><p class="query_string">'+query+'</p></li>').appendTo(this);
			}
			//HumbleFinance.drawFlags();
		}	
	});

	/* prepopulated queries */
	jQuery('ul.query_bank li').draggable({revert:true, helper: 'clone'});

	/* remove query from query area */
	jQuery('.rm_query').live('click',function(){
		jQuery(this).parent('li').remove();
		return false;
	});
	jQuery('.add_query').click(function(){
		var list = jQuery(this).parent('div').next('ul');
		var type = 'buy'
		if(jQuery(this).hasClass('sell_query')){
			type = 'sell';
		}
		jQuery('<li><a href="" class="rm_query">x</a><input name="'+type+'_query" type="hidden" value=""/><p class="query_string" style="display:none"></p><input class="query_input" type="text" value=""/><button class="modify_query" type="button">Save</button></li>').appendTo(list).find('input.query_input').focus();
		return false;
	});


	jQuery('.query_string').live('click',function(){
		var query = jQuery(this).text();
		jQuery(this).hide();
		var edit_field = jQuery('<input type="text" value="'+query+'"/><button class="modify_query" type="button">Save</button>').insertBefore(this);
		return false;
	});

	jQuery('button.modify_query').live('click',function(){
		var new_query = jQuery(this).prev('input');	
		jQuery(this).siblings('.query_string').text(new_query.val()).show();
		jQuery(this).siblings('input[type="hidden"]').val(new_query.val());
		if(jQuery(this).parent().data('link')){
			var link = jQuery(this).parent().data('link');
			if(!link.hasClass('immutable')){
				link.text(new_query.val());
			}
		} else{
			if(jQuery(this).parents('ul').hasClass('buy_queries')){
				var list = jQuery('.query_bank.buy_queries');
			} else{
				var list = jQuery('.query_bank.sell_queries');
			}
			var link = jQuery('<li>'+new_query.val()+'</li>').appendTo(list).draggable({revert:true, helper: 'clone'});
			jQuery(this).parent().data('link',link);
		}
		jQuery(this).remove();
		new_query.remove();
	});



  //check for cookie
	jar = new CookieJar({
	  expires:60*60*24*365,
	  path: '/'
  });
	
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
		
		$('loader').show();

		jQuery.ajax({
			type: 'GET',
			url: jQuery(this).attr('action'),
			success: function(data){
				jQuery('#finance').html("<div id=\"labels\"><div id=\"dateRange\">&nbsp;</div></div>");
				delete rdata;
				chartData(data.contents);
				$('loader').hide();
			},
			dataType: 'json',
			data: jQuery(this).serialize()
		});
		
		return false;
	}
	
	jQuery('#queryform').submit(formsub);	
	
	});

