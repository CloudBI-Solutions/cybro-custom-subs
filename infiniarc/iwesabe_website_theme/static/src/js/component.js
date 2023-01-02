odoo.define('iwesabe_website_theme.update_components', function (require) {
	
	var ajax = require('web.ajax');
	var clear_no_value = true;

	$(document).ready(function() {
	
		function remove_product(current_ele){
			if (current_ele.length > 0){
				var selling_price_ele = $(".selling_price .price");
				var selling_price = parseFloat(selling_price_ele.text());
				var remove_price = current_ele.find(".component_price");
				var remove_price = parseFloat(remove_price.text());
				var new_price = selling_price - remove_price;
				selling_price_ele.text(new_price.toFixed(2));
				current_ele.remove();
			}
		}
		// Brand Base Filter
		$(".brand-filter").click(function(){
			var filter_id = $(this).attr('filter-id');
			var line_id = $(this).attr('line-id');
			
			var componet_iteam = $('#all_'+line_id).find('.componet_iteam');
			var showing_components = [];
			var hiding_components = [];
			$(componet_iteam).each(function(e, i) {
				if($(i).attr('id') == filter_id){
					showing_components.push($(i));
				}
			});
			$(componet_iteam).fadeOut(200);
			setTimeout(()=>{
				for (var i=0;i<showing_components.length;i++){
					showing_components[i].fadeIn(1000);
				}
			},200)
		});
		// All Filter Data Show
		$(".all-data").click(function(){
			var line_id = $(this).attr('line-id');
			var componet_iteam = $('#all_'+line_id).find('.componet_iteam');
			$(componet_iteam).each(function(e, i) {
				$(i).show(1000);
			});
		});
		// Grid View Show
		$(".th-block").click(function(){
			var grid_id = $(this).attr('grid-id');
			var grid_elem = $('#grid_' + grid_id);
			var list_elem = $('#list_' + grid_id);
			grid_elem.show('3000');
			list_elem.hide('3000');
			$(this).addClass('active');
			$('.bar-block').removeClass('active');
			
			// updating checkbox
			var list_input = list_elem.find(`[name=${grid_id}]:checked`);
			if (list_input){
				var grid_input_elem = grid_elem.find(`[id=${list_input.attr("id")}]`);
				grid_input_elem.click()
			}
		});
		$(".bar-block").click(function(){
			var list_id = $(this).attr('list-id');
			var grid_elem = $('#grid_' + list_id);
			var list_elem = $('#list_' + list_id);
			grid_elem.hide('3000');
			list_elem.show('3000');
			$(this).addClass('active');
			$('.th-block').removeClass('active');
			
			// updating checkbox
			var grid_input = grid_elem.find(`[name=${list_id}]:checked`);
			if (grid_input){
				var list_input_elem = list_elem.find(`[id=${grid_input.attr("id")}]`);
				list_input_elem.click()
			}
		});
		
		function add_product(current_ele,data){
			var to_html = `<div class="component_part" section_id="${current_ele.attr("name")}" id="${current_ele.attr("id")}"><div class="component_text">${data['product_name']}</div><div class="component_price">${data['price']}</div></div>`;
			var product_component = $(".product_component");
			product_component.append(to_html);
			var selling_price_ele = $(".selling_price .price");
			var selling_price = selling_price_ele.text();
			var product_price = parseFloat(data['price']);
			var new_total = parseFloat(selling_price) + product_price;
			selling_price_ele.text(new_total.toFixed(2));
		}
	
		//Lits View Check Out
		var checked_items = $(".componet_iteam input:checked");
		if (checked_items.length > 0){
			var product_component = $(".product_component");
			product_component.empty();
			clear_no_value = false;
		}
		for (var i=0;i<checked_items.length;i++){
			var target_ele = $(checked_items[i]);
			var json_data = JSON.parse(target_ele.attr("data"));
			add_product(target_ele,json_data)
		}
	
		$(".componet_iteam input").on('change',function(e){
			if (clear_no_value){
				var product_component = $(".product_component");
				product_component.empty();
				clear_no_value = false;
			}
			var target_ele = $(e.currentTarget);
			var section_id = target_ele.attr("name");
			remove_product($(`.product_component .component_part[section_id=${section_id}]`));
			var json_data = JSON.parse(target_ele.attr("data"));
			add_product(target_ele,json_data);
		})
	
		
		//Gird View Check Out
		var checked_items_list = $(".componet_iteam_list input:checked");
		if (checked_items_list.length > 0){
			var product_component = $(".product_component");
			product_component.empty();
			clear_no_value = false;
		}
		for (var i=0;i<checked_items_list.length;i++){
			var target_ele = $(checked_items_list[i]);
			var json_data = JSON.parse(target_ele.attr("data"));
			add_product(target_ele,json_data)
		}
	
		$(".componet_iteam_list input").on('change',function(e){
			if (clear_no_value){
				var product_component = $(".product_component");
				product_component.empty();
				clear_no_value = false;
			}
			var target_ele = $(e.currentTarget);
			var section_id = target_ele.attr("name");
			remove_product($(`.product_component .component_part[section_id=${section_id}]`));
			var json_data = JSON.parse(target_ele.attr("data"));
			add_product(target_ele,json_data);
		})
	
		
		$(".com-cart-btn").click(function(){
			var added_products = $(".product_component .component_part");
			var main_product_id = $(this).attr('data-product-id');
			console.log("main_product_id",main_product_id)
			var product_ids = [];
			product_ids.push(main_product_id);
			if (added_products.length > 0){
				for (var i=0; i < added_products.length;i++){
					product_ids.push($(added_products[i]).attr("id"))
				}
				$(this).attr("disabled",true)
				var processing_icon = `
					<i class="fa fa-spin fa-spinner waiting" style="margin-top: -3px;margin-left: 6px;font-size: 20px;"/>
				`;
				$(this).append(processing_icon);
				ajax.jsonRpc('/shop/cart/update_components', 'call',{'product_ids':product_ids}).then(function(data) {
					if (data === true){
						window.location.replace("/shop/cart");
					}
					else {
						$(".com-cart-btn i.waiting").remove();
						$(".com-cart-btn").removeAttr("disabled");
					}
				})
			}
		})
	
		$(".add-to-cart-shop").click(function(event){
			var product_id = [$(this).attr('data-product-id')];
			ajax.jsonRpc('/shop/cart/update_components', 'call',{'product_ids':product_id}).then(function(data) {
				if (data === true){
					window.location.replace("/shop/cart");
				}
			})
		})
		
		$(".add-to-cart").click(function(event){
			var product_id = [$(this).attr('data-id')];
			ajax.jsonRpc('/shop/cart/update_components', 'call',{'product_ids':product_id}).then(function(data) {
				if (data === true){
					window.location.replace("/shop/cart");
				}
			})
		})
		
		$(".btn-add-cart").click(function(event){
			var product_id = [$(this).attr('data-id')];
			ajax.jsonRpc('/shop/cart/update_components', 'call',{'product_ids':product_id}).then(function(data) {
				if (data === true){
					window.location.replace("/shop/cart");
				}
			})
		})
		
		$(".cart-icon").click(function(event){
		    console.log('$(this)',$(this))
			var product_id = [$(this).attr('data-id')];
			console.log('product_id', product_id)
			ajax.jsonRpc('/shop/cart/update_components', 'call',{'product_ids':product_id}).then(function(data) {
				if (data === true){
				    console.log('datraetfc', data)
					window.location.replace("/shop/cart");
				}
			})
		})
	
		$(".scroll-animate").click(function(event){
			var current_elem = event.currentTarget;
			var page_number = $(current_elem).attr("href").replace("#","");
			$('html, body').animate({
				scrollTop: $(`.component_list_part#${page_number} .component_name`).position().top + 5
			}, 1000);
		})
	
	});
});