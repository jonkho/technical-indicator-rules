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
var QUERYDATA = js;
function showTour() {
	  Modalbox.show('/tour/', {title: 'WELCOME TO TRADESPARROW', width: 600});
	}

function tourStart(tic) {
  Modalbox.hide();
  s = $('symbol');
  s.value = tic;
}
jQuery('document').ready(function(){
	
	window.timer = null;
	window.onresize = function() {
		if (window.timer === null) {
			window.timer = window.setTimeout(function() {
				window.timer = null;
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
				jQuery('#finance').html("<div id=\"labels\"><div id=\"dateRange\">&nbsp;</div></div>");
				delete rdata;
				chartData(QUERYDATA.contents);
			}, 100);
		}
	}

	/* load data if supplied */
	if(js){
	  chartData(js.contents);
	  chartSummary(js.contents.summary);
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
			//redraw flags
			//TODO: redraw slider
			HumbleFinance.drawFlags();
			HumbleFinance.graphs.summary.setSelection(HFarea);
		}	
	});

	/* prepopulated queries */
	jQuery('ul.query_bank li').draggable({revert:true});

	/* remove query from query area */
	jQuery('.rm_query').live('click',function(){
		jQuery(this).parent('li').remove();
		
		HumbleFinance.graphs.summary.setSelection(HFarea);
		HumbleFinance.drawFlags();
		return false;
	});
	jQuery('.add_query').click(function(){
		var list = jQuery(this).parent('div').next('ul');
		var type = 'buy'
		if(jQuery(this).hasClass('sell_query')){
			type = 'sell';
		}
		jQuery('<li><a href="" class="rm_query">x</a><input name="'+type+'_query" type="hidden" value=""/><p class="query_string" style="display:none"></p><input class="query_input" type="text" value=""/><button class="modify_query" type="button">Save</button></li>').appendTo(list).find('input.query_input').focus();
		
		HumbleFinance.graphs.summary.setSelection(HFarea);
		HumbleFinance.drawFlags();
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
		
		HumbleFinance.graphs.summary.setSelection(HFarea);
		HumbleFinance.drawFlags();
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



	function chartSummary(summary){
		if(summary){
			jQuery('div.query_summary').show();
			jQuery('#buy_and_hold_value').text(summary.buy_and_hold_value);
			jQuery('#strategy_value').text(summary.strategy_value);
			jQuery('#performance_delta').text(summary.performance_delta+'%');
			jQuery('div.trade_history table').remove();
			var table = '<table><tr><th>Date</th><th>Action</th><th>Price</th><th>Shares Balance</th><th>Cash Balance</th><th>Account Value</th></tr>';
			summary.trade_history.each(function(n){
				table += '<tr><td>'+n[0]+'</td><td>'+n[1]+'</td><td>$'+n[2]+'</td><td>'+n[3]+'</td><td>$'+n[4]+'</td><td>$'+n[5]+'</td>';
			});
			table += '</table>';
			jQuery(table).prependTo('div.trade_history');
		} else{
			jQuery('div.query_summary').hide();
			jQuery('div.trade_history table').remove();
		}
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
				QUERYDATA = data;
				chartSummary(data.contents.summary);
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
