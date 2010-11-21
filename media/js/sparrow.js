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

jQuery('document').ready(function(){

	//alert pop up
	jQuery('#alert_me_link').click(function(){
		var fb = jQuery.facebox('<div id="alert_box"><h2>Sign up to receive alerts</h2><form action="alert/" method="post"><label>Email</label><input name="email" type="text" value=""/><input type="submit" value="Sign Up"/></form><img src="/django-lean/goal/emailclick" height="1" width="1" /></div>');
		return false;
	});

	jQuery('#alert_box form').live('submit',function(){
		var form_wrapper = jQuery(this).parent();
		jQuery.ajax({
			type: 'post',
			url: 'alert/',
			success: function(data){
				form_wrapper.append('<p style="color:green;">Thank you for signing up</p>');
			},
			data: jQuery(this).serialize()
		});
		return false;
	});
	//*********************************************************//


	//stop loss event handler
	jQuery('div.stop_loss_control ul li').click(function(){
		var slp = jQuery(this);
		slp.siblings('li').removeClass('active').end().toggleClass('active');
		if(slp.hasClass('active')){
			jQuery('#stop_loss_input').val(slp.text());
		} else{
			jQuery('#stop_loss_input').val('');
		}
	});






	//init from and to date mask
	jQuery('#end_date').mask('9999/99/99');
	jQuery('#start_date').mask('9999/99/99');

	jQuery('div.date_changer a').click(function(e){
		var modifier = jQuery(this).attr('rel');
		var d = new Date();
		var modifiedDate = '';
		if(modifier === 'today'){
			modifiedDate = jQuery.datepicker.formatDate('yy/mm/dd',d);
		} else if(modifier == 'start_of_year'){
			modifiedDate = jQuery.datepicker.formatDate('yy/mm/dd',new Date(d.getFullYear()+'/01/01'));
		} else{
			var type = modifier[modifier.length - 1];
			var num = parseInt(modifier.substr(0,modifier.length - 1));
			if(type === 'm'){
				modifiedDate = jQuery.datepicker.formatDate('yy/mm/dd',new Date(d.getFullYear()+'/'+(d.getMonth() - num + 1)+'/'+d.getDate()));
			} else if(type === 'y'){
				modifiedDate = jQuery.datepicker.formatDate('yy/mm/dd',new Date((d.getFullYear() - num)+'/'+(d.getMonth() + 1)+'/'+d.getDate()));
			}
		}
		jQuery(this).parent().siblings('input').val(modifiedDate);
		return false;
	});
	//**************************************************//

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
				jQuery('#finance').html("<div id=\"labels\"><div id='legend'><p id='buy_legend'>Buy</p><p id='sell_legend'>Sell</p></div><div id=\"dateRange\">&nbsp;</div></div>");
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
	initDropArea(jQuery('ul.buy_queries'),1);
	initDropArea(jQuery('ul.sell_queries'),1);

	function initDropArea(ele,index){
		/* active query area */
		jQuery(ele).droppable({
			accept: 'ul.query_bank li',
			drop: function(event, ui){
				var li = jQuery(ui.draggable).clone();
				var query = jQuery(li).text();
				if(jQuery(this).hasClass('buy_queries')){
					jQuery('<li><a href="" class="rm_query">x</a><input name="buy_query_'+index+'" type="hidden" value="'+query+'"/><p class="query_string">'+query+'</p></li>').appendTo(this);
				} else{
					jQuery('<li><a href="" class="rm_query">x</a><input name="sell_query_'+index+'" type="hidden" value="'+query+'"/><p class="query_string">'+query+'</p></li>').appendTo(this);
				}
				//redraw flags
				//TODO: redraw slider
				HumbleFinance.drawFlags();
				HumbleFinance.graphs.summary.setSelection(HFarea);
			}	
		});
	};




	/* prepopulated queries */
	jQuery('ul.query_bank li').draggable({revert:true,zIndex: 200});

	/* remove query from query area */
	jQuery('.rm_query').live('click',function(){
		jQuery(this).parent('li').remove();
		HumbleFinance.graphs.summary.setSelection(HFarea);
		HumbleFinance.drawFlags();
		return false;
	});


	jQuery('.add_query').live('click',function(){
		var list = jQuery(this).parent('div').next('ul');
		var index = jQuery(this).parent().parent().siblings().length + 1;
		var type = 'buy'
		if(jQuery(this).hasClass('sell_query')){
			type = 'sell';
		}
		jQuery('<li><a href="" class="rm_query">x</a><input name="'+type+'_query_'+index+'" type="hidden" value=""/><p class="query_string" style="display:none"></p><input class="query_input" type="text" value=""/><button class="modify_query" type="button">Save</button></li>').appendTo(list).find('input.query_input').focus();
		
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
			var link = jQuery('<li>'+new_query.val()+'</li>').appendTo(list).draggable({revert:true, zIndex:200});
			jQuery(this).parent().data('link',link);
		}
		jQuery(this).remove();
		new_query.remove();
		
		HumbleFinance.graphs.summary.setSelection(HFarea);
		HumbleFinance.drawFlags();
	});


	//clone the drop area
	jQuery('.add_or').live('click',function(e){
		var orig_drop_area = jQuery(this).parent('div');
		var or_count = 	orig_drop_area.siblings().length + 2;
		if(or_count <= 3){ 
			var new_drop_area = orig_drop_area.clone();
			var query_area = new_drop_area.find('ul.query_area');

			
			query_area.children('li').remove();
			new_drop_area.find('div.stop_loss_control').remove();
			new_drop_area.find('a.remove_or_query').remove();

			if(or_count == 3){
				new_drop_area.find('a.add_or').remove();
			}

			initDropArea(query_area,or_count);
			jQuery('<a href="" class="remove_or_query">x</a>').appendTo(new_drop_area.find('div.drop_header'));

			orig_drop_area.parent('div').append(new_drop_area);
			HumbleFinance.drawFlags();
			HumbleFinance.graphs.summary.setSelection(HFarea);
		} else{
			alert('asdf');
		}
		e.preventDefault();
	});


	jQuery('a.remove_or_query').live('click',function(e){
		jQuery(this).parent().parent().remove();
    HumbleFinance.drawFlags();
		HumbleFinance.graphs.summary.setSelection(HFarea);
		e.preventDefault()
	});


	function chartSummary(summary){
		if(summary){
			jQuery('div.query_summary').show();
			jQuery('#buy_and_hold_value').text('$'+summary.buy_and_hold_value);
			jQuery('#strategy_value').text('$'+summary.strategy_value);
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
				jQuery('#finance').html("<div id=\"labels\"><div id='legend'><p id='buy_legend'>Buy</p><p id='sell_legend'>Sell</p></div><div id=\"dateRange\">&nbsp;</div></div>");
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
