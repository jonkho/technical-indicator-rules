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

	/* submit query */
	jQuery('#queryform').submit(function(){
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
				console.log(data.contents);
				chartData(data.contents.data);
			},
			dataType: 'json',
			data: jQuery(this).serialize()
		});
		return false;
	});	

});
