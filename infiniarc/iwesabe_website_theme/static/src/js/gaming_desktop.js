odoo.define('iwesabe_website_theme.gaming_desktop', function (require) {
	
	var ajax = require('web.ajax');

	$(document).ready(function() {


	    var ex_fils = $('.ial-filter__checkbox')
	    var cur_fils = $('.cur_filters').attr('id')
	    if (cur_fils != undefined){
            arr = JSON.parse(cur_fils)
            $.each(ex_fils, function(i,elem){
                var fil_id = parseInt($(elem).attr('id'))
                if( arr.includes(fil_id) ){
                    $(elem).prop( "checked", true )
                    var par = $(elem).parent().parent().parent()
                    console.log('parr', par)
                    if(par.hasClass('d-none')){
                        par.removeClass('d-none')
                    }
                }
            })
	    }

        //This part keeps the price filter remain filtered
        var min_price = parseInt($(".min-price-gpc").val());
        var max_price = parseInt($(".mix-price-gpc").val());
        var drops = $('.shop_top_bar').find('.dropdown-item')

        $.each(drops, function(i, anchor) {
          var cur_href = $(anchor).attr("href")
          if(cur_href.indexOf('&{') != -1){
              test = cur_href.slice(0,cur_href.indexOf('&{') )
              test += '&{' + min_price +','+ max_price +'&}'
              var new_href = $(anchor).attr("href", test)
          }else{
              cur_href += '&{'+ min_price + ',' + max_price + '&}'
              var new_href = $(anchor).attr("href", cur_href)
          }
        })

        //This part adds the applied filters to the url on document ready
        var existing_filters = $('.ial-filter__checkbox')
        var filters = []

        $.each(existing_filters, function(i,elem){
           if( $(elem).is(':checked') ){
               filters.push(parseInt($(elem).attr("id")))
           }
        })

        $.each(drops, function(i, anchor) {
            var cur_href = $(anchor).attr("href")
            var test = '';
            if(cur_href.indexOf('[') != -1){
                test = cur_href.slice(0,cur_href.indexOf('[') )
                test += '[' + filters.join(',') + ']'
                var new_href = $(anchor).attr("href", test)
            }else{
                cur_href += '&[' + filters.join(',') + ']'
                var new_href = $(anchor).attr("href", cur_href)
            }
        })
        //End of filter functions


		function formatted_url(r){
			var a={search:{},hash:{}},
				e=new URL(r);
			for(var s of Array(2).keys())
				for(var n=1==s?"hash":"search",h=e[n].substring(1).split("&"),t=0;t<h.length; t++){
					var o=h[t].split("=");
					o[0]&&(a[n][o[0]] = decodeURIComponent(o[1]))
				}
			return a
		}
		
        function url_to_string(obj) {
            var str = [];
            for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + obj[p]);
            return `?${str.join("&")}`;
        }
        $('.filter-reset').click(function(e){
            $('#min_price_gpc').val('');
            $('#max_price_gpc').val('');
            var attr_brand_input = $(".attr-model-input-gpc");
            console.log('attr_brand_input',attr_brand_input)
            for (var i=0;i<attr_brand_input.length;i++){
               filter = $(attr_brand_input[i]).prop("checked", false)
            }
            var func = price_page_load(e);
        })
		
		function price_page_load(e){
		    console.log('price_page_load')
			var min_price = parseInt($(".min-price-gpc").val());
			var max_price = parseInt($(".mix-price-gpc").val());

			$.each(drops, function(i, anchor) {
              var cur_href = $(anchor).attr("href")
              if(cur_href.indexOf('&{') != -1){
                  test = cur_href.slice(0,cur_href.indexOf('&{') )
                  test += '&{' + min_price +','+ max_price +'&}'
                  var new_href = $(anchor).attr("href", test)
              }else{
                  cur_href += '&{'+ min_price + ',' + max_price + '&}'
                  var new_href = $(anchor).attr("href", cur_href)
              }
            })

			var price_change_warning = $(".price_change_warning");
			price_change_warning.addClass('d-none');
			var price_query = '';
			if (min_price && max_price){
				if (min_price > max_price){
					price_change_warning.removeClass('d-none');
				}
				else {
					price_query = `${min_price}-${max_price}`
				}
			}
			else if (min_price){
				price_query = `${min_price}-`
			}
			else if (max_price){
				price_query = `-${max_price}`
			}
			else {
				price_query = ''
			}
			var url_query = formatted_url(location.href);
			if (price_query){
				url_query.search.price = price_query;
			}
			else {
				delete url_query.search.price;
			}
			url_query.search[filters] = filters
			var new_query = url_to_string(url_query.search);
			$.post("/get_gaming_desktop_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		}
		
		$(".widget-content .search-attribute-gpc").on('keyup',function(e){
			if (e.which == 13){
				var search_query = $(this).val();
				var url_query = formatted_url(location.href);
				if (search_query){
					url_query.search.q = search_query;
				}
				else{
					delete url_query.search.q;
				}
				var new_query = url_to_string(url_query.search);
				$.post("/get_gaming_desktop_view", url_query.search, function( data ) {
					$("#product-view-list").html( data );
				});
				history.pushState(null, null, new_query);
			}
		})
		
		$(".attr-brand-gpc").click(function(){
			var attr_brand_input = $(".attr-brand-input-gpc");
			var branch_ids = [];
			for (var i=0;i<attr_brand_input.length;i++){
				if ($(attr_brand_input[i]).prop("checked")){
					branch_ids.push($(attr_brand_input[i]).attr("filter-data"))
				}
			}
			var branch_query = branch_ids.join("-");
			var url_query = formatted_url(location.href);
			if (branch_query){
				url_query.search.brands = branch_query;
			}else{
				delete url_query.search.brands;
			}
			var new_query = url_to_string(url_query.search);
			$.post("/get_gaming_desktop_view", url_query.search, function( data ) {
			    console.log('data gpc', data)
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		});
		$(".attr-model-gpc").click(function(){
            var existing_filters = $('.ial-filter__checkbox')
            var filters = []
            var drops = $('.shop_top_bar').find('.dropdown-item')

            $.each(existing_filters, function(i,elem){
               if( $(elem).is(':checked') ){
                   filters.push(parseInt($(elem).attr("id")))
               }
            })

            $.each(drops, function(i, anchor) {
                var cur_href = $(anchor).attr("href")
                var test = '';
                if(cur_href.indexOf('[') != -1){
                    test = cur_href.slice(0,cur_href.indexOf('[') )
                    test += '[' + filters.join(',') + ']'
                    var new_href = $(anchor).attr("href", test)
                }else{
                    cur_href += '&[' + filters.join(',') + ']'
                    var new_href = $(anchor).attr("href", cur_href)
                }
                console.log(test)

            })

			var attr_model_input = $(".attr-model-input-gpc");
			var branch_ids = [];
			for (var i=0;i<attr_model_input.length;i++){
				if ($(attr_model_input[i]).prop("checked")){
					branch_ids.push($(attr_model_input[i]).attr("filter-data"))
				}
			}
			var branch_query = branch_ids.join("-");
			var url_query = formatted_url(location.href);
			if (branch_query){
				url_query.search.models = branch_query;
			}else{
				delete url_query.search.models;
			}
			var new_query = url_to_string(url_query.search);
			$.post("/get_gaming_desktop_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		});
		$(".attr-gpu-gpc").click(function(){
			var attr_gpu_input = $(".attr-gpu-input-gpc");
			var branch_ids = [];
			for (var i=0;i<attr_gpu_input.length;i++){
				if ($(attr_gpu_input[i]).prop("checked")){
					branch_ids.push($(attr_gpu_input[i]).attr("filter-data"))
				}
			}
			var branch_query = branch_ids.join("-");
			var url_query = formatted_url(location.href);
			if (branch_query){
				url_query.search.gpus = branch_query;
			}else{
				delete url_query.search.gpus;
			}
			var new_query = url_to_string(url_query.search);
			$.post("/get_gaming_desktop_view", url_query.search, function( data ) {
				$("#product-view-list").html( data );
			});
			history.pushState(null, null, new_query);
		});
		
		$(".min-price-gpc").on('focusout',price_page_load)
		$(".mix-price-gpc").on('focusout',price_page_load)
	});

	$(".o_wish_rm").click(function(ev) {
            console.log('_onRemoveClick......')
            if($('body').hasClass('editor_enable')){
                ev.stopImmediatePropagation();
                ev.preventDefault();
            } else{
                var ajax = require('web.ajax');
                var tr = $(ev.currentTarget).parents('tr');
                var wish = tr.data('wish-id');
                var route = '/shop/wishlist/remove/' + wish;
                ajax.jsonRpc(route, 'call', {
                    'wish': wish
                }).then(function(data) {
                    $(tr).hide();
                    if ($('.t_wish_table tr:visible').length == 0) {
                        window.location.href = '/';
                    }
                })
            }
        });
	
});
