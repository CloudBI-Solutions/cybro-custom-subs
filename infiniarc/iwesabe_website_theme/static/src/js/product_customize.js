odoo.define('iwesabe_website_theme.product_customise', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;


    publicWidget.registry.componentsProductsCustomise = publicWidget.Widget.extend({
        selector: '#product_customise_div',
        events: {
           'click .product_individual_single': '_onClickComponentsProducts',
           'click #product_individual_multi': '_onClickComponentsProducts2',
           'click .check_buttons_class': '_onClickSelection_quantities',
           'click .radio_buttons_class': '_onClickRadio_buttons_class',
           'click .selection_quantities': '_onClickSelections',
           'change .selection_quantities': '_onChangeSelections',
           'focus .selection_quantities': '_onFocusSelections',
           'click .not_mandatory_clear_div': '_onClickNotMandatoryClose',
           'click #refresh_button': '_onClickRefreshButton',
           'click #add_total_project_btn': '_onClickAddToCart',
           'click #specifications_pop_up': '_onShowModal',
           'click .pop_up_images_div_ids': '_onShowModalProductCards',
           'mouseover #add_total_project_btn': '_onMouseOverAdd',
           'mouseleave #add_total_project_btn': '_onMouseLeaveAdd',
           'DOMMouseScroll .scroll_main_class': '_onScroll',
           'click #openMobSideBar': '_onclickMobSideBar',
           'click .scroll_components_mob_views': '_onclickMobSideBar'
//           'change .check_buttons_class': '_onChangeCheck_buttons_class',
        },

        init: function () {
            var product_id = document.getElementById('main_product_id').value;
            this._onClickRefresh(product_id);

         },

        start: function () {
            var self = this;
            console.log('2')
//            this._checkCapacityCompatibility()

         },
         _onclickMobSideBar:function(ev){
             if ($(window).width() < 994){
                var categoryEl = document.querySelector('.left_components_wrap_mob_view');
                var iconShow = document.querySelector('#mobSidebarIconShow');
                var iconHide = document.querySelector('#mobSidebarIconHide');
                categoryEl.classList.toggle('mob_sidebar_hide');
                if(categoryEl.classList.contains('mob_sidebar_hide')){
                    iconHide.classList.add('d-none');
                    iconShow.classList.remove('d-none');
                }else{
                    iconShow.classList.add('d-none');
                    iconHide.classList.remove('d-none');
                }
             }
         },

        _onScroll: function(ev){
//            console.log('lol',$(window).width())
             if ($(window).width() > 994){
                var $categoryTitles = $('.scrollpy .component_section');
                var topCat = $categoryTitles.filter((i, el) => $(el).offset().top > $(window).scrollTop()).first();
                var id = $(topCat[0]).attr('id');
                var scrolls = document.getElementsByClassName('scroll_components_main');
                for (const scroll of scrolls) {
                                if(scroll.classList.contains('active')){
                                    scroll.classList.remove("active");
                                    break;
                                }
                            }
                var left_comp = $('.left_components_wrap')
                var categ = left_comp.find('a[href="'+'#'+id+'"]');
                if(categ){
                var categ_div = categ.parents('.categ_heads');
                    if(categ_div[0]){
                    console.log('categ',categ_div[0].id)
                    var buttons_left = $('.main_button_left');
                    console.log('buton_left',buttons_left.length)
                    var Button = left_comp.find('button[data-target="'+'#'+categ_div[0].id+'"]');
                    if(Button){
                        console.log('button',Button[0].id)
                        var btn_to_click = Button[0].id
                        console.log('3',document.getElementById(btn_to_click));
                        var no = document.getElementById(btn_to_click).clicked;
                        console.log('kjjljlk',no);
//                        console.log('h',Button.attr("aria-expanded"))
                        var check = Button.attr("aria-expanded")
//                        console.log('log',check,typeof(check))
//                        console.log('check',check)
                        if(check =='false'){
//                            console.log('false-click')
                            Button.click()
                        }
                    }
                }
                }
                var a_tag = left_comp.find('a[href="'+'#'+id+'"]');
                if(a_tag){
                    a_tag.addClass( "active" );
                }

                //k
//                var categ = $('a[href="'+'#'+id+'"]');
//                if(categ){
//                var categ_div = categ.parents('.categ_heads');
//                    if(categ_div[0]){
//                    var Button = $('button[data-target="'+'#'+categ_div[0].id+'"]');
//                    if(Button){
//                        var check = Button.attr("aria-expanded")
//                        if(check =='false'){
//                            Button.click()
//                        }
//                    }
//                }
//                }
//                var a_tag = $('a[href="'+'#'+id+'"]');
//                if(a_tag){
//                    a_tag.addClass( "active" );
//                }
             }
         },

        _onClickRefreshButton:function(){
            var product_id = document.getElementById('main_product_id').value;
            this._onClickRefresh(product_id);
         },

        _onClickLeftButton:function(){
             var buttons = document.getElementsByClassName('components_buttons');
             if(buttons[0]){
                 buttons[0].click()
             }

        },
        _onClickRefresh:function(data){
            console.log('refresh34')
            var self = this;
            ajax.jsonRpc('/get_refresh_template', 'call',{'id':data}).then(function (result) {
                    if(result){
                        $('#my_custom_div').html(result);
                        self._onClickLeftButton()
                        self._checkCapacityCompatibility(0);
                    }
                });

         },

        _onShowModal:function(ev){
            const radioButtons = this.$target.closest('#product_customise_div').find('.radio_buttons_class');
            const checkboxes = this.$target.closest('#product_customise_div').find('.check_buttons_class');
            const product_id = this.$target.closest('#product_customise_div').find('#main_product_id')[0].value;
            var listofchecked = []
            var listofcomponent = []
            var dictofcheckvalues = {}
            for (const radioButton of radioButtons) {
                            if(radioButton.checked){
                                listofchecked.push(radioButton.dataset['product_id']);
                                listofcomponent.push(radioButton.dataset['component_id']);
                            }
                        }
            for (const checkbox of checkboxes) {
                            if(checkbox.checked){
                                var tag = '#selection_'+checkbox.value;
                                var select_id = this.$target.closest('#product_customise_div').find(tag);
                                if(select_id[0]){
                                    if(parseInt(select_id[0].value)==0){null;}
                                    else{
                                    listofchecked.push(checkbox.value);
                                    listofcomponent.push(checkbox.dataset['component_id']);
                                    dictofcheckvalues[checkbox.value]=parseInt(select_id[0].value);
                                    }
                                }
                                else{
                                    listofchecked.push(checkbox.value);
                                    listofcomponent.push(checkbox.dataset['component_id']);
                                    dictofcheckvalues[checkbox.value]=1;
                                }
                            }
                        }
            ajax.jsonRpc('/get_dialogue_data', 'call',{'id':product_id,'products': listofchecked,'components':listofcomponent,'dict':dictofcheckvalues}).then(function (result) {
                    if(result){
                        $('#dialogue_box_content').html(result);
                    }
                });

         },

         _onShowModalProductCards:function(ev){
            ev.stopPropagation();
            var product_id = ev.currentTarget.dataset['id'];
            console.log('product',product_id)
            ajax.jsonRpc('/get_product_card_pop_up', 'call',{'id':product_id}).then(function (result) {
                    if(result){
                        $('#dialogue_box_product_images').html(result);
                        $('#product_images_modal').modal().show();
                    }
                });
         },

        _onFocusSelections: function(ev){
            var value = ev.currentTarget.value;
            var component_id = ev.currentTarget.dataset['component_id'];
            var product_id = ev.currentTarget.dataset['product_id'];
            var pre_tag = document.getElementById('prev_chose'+product_id)
            if(pre_tag){pre_tag.value = value;}

        },

        _onChangeSelections: function(ev){
            var component_id = ev.currentTarget.dataset['component_id'];
            var product_id = ev.currentTarget.dataset['product_id'];
            var radioButton = document.getElementById('radio_product_component'+product_id);
            if(radioButton.checked){
                var pre_tag = document.getElementById('prev_chose'+product_id)
                if(pre_tag){
                    var old_value = pre_tag.value;
                    var new_value = ev.currentTarget.value;

                    //total sum updation
                    var new_multiple = (parseInt(new_value)-parseInt(old_value))
                    new_multiple = new_multiple ? new_multiple : 0;
                    var current_total_amount = document.getElementById('new_updated_total').value;
                    var current_amount = document.getElementById('current_price_product'+product_id).value;
                    var new_amount = parseInt(current_total_amount)+(parseInt(current_amount)*parseInt(new_multiple));
                    document.getElementById('new_updated_total').value = new_amount;

                    //multi watt increase selection
                    var current_power = document.getElementById('power_watt_product'+product_id).value;
                    current_power = current_power ? current_power : 0;
                    var power_capacity = document.getElementById('power_capacity_sum').value;
                    power_capacity = power_capacity ? power_capacity:0;
                    var new_value_w = parseInt(power_capacity)+(parseInt(current_power)*parseInt(new_multiple))
                    document.getElementById('power_capacity_sum').value = new_value_w;
                    this._checkCapacityCompatibility(component_id)


                    pre_tag.value = new_value;
                    var total_allowed_component_div = document.getElementById('total_allowed_component'+component_id);
                    var total_allowed_component_value = total_allowed_component_div.value;
                    var updated_value = parseInt(old_value) - parseInt(new_value) + parseInt(total_allowed_component_value);
                    }

                if(updated_value){
                    total_allowed_component_div.value = updated_value;
                    }
                 else{
                    total_allowed_component_div.value = 0;
                    var check_class_component = 'check_class_component'+component_id;
                    var checkboxes = document.getElementsByClassName(check_class_component);
                    for (const checkbox of checkboxes) {
                            if(checkbox.checked){
//                                here\
                                  null
                            }
                            else{
//                                here
                                checkbox.disabled = true;
                            }
                        }
                 }
                var check_class_component = 'check_class_component'+component_id;
                var checkboxes = document.getElementsByClassName(check_class_component);
                if(checkboxes){
                        for (const checkbox of checkboxes) {
                            if(checkbox.checked){
//                                here\
                                  var id = checkbox.value;
                                  var selection_id = '#selection_'+id;
                                  var this_value = document.getElementById('selection_'+id).value;
                                  $(selection_id)[0].options.length = 0;
                                  var iteration = parseInt(updated_value)+parseInt(this_value);
                                  console.log('iterari',iteration)
                                    for(var i=1;i<=iteration;i++){
                                        if(i == parseInt(this_value)){
                                            $(selection_id).append('<option selected="selected" value="'+i+'">'+i+'</option>');
                                        }
                                        else{$(selection_id).append('<option value="'+i+'">'+i+'</option>');}
                                    }
                            }
                            else{
//                                here
                                var id = checkbox.value;
                                var selection_id = '#selection_'+id;
                                $(selection_id)[0].options.length = 0;
                                var iteration2 = parseInt(updated_value);
                                console.log('iteration2',iteration2)
                                for(var i=1;i<=iteration2;i++){
                                    $(selection_id).append('<option value="'+i+'">'+i+'</option>');
                                }
                            }
                        }
                    }

            }
        },

        _onClickSelections: function(ev){
            ev.stopPropagation();
           },

        _onClickNotMandatoryClose: function(ev){
            ev.stopPropagation();
            var product_id = ev.currentTarget.value;
            var component_id = ev.currentTarget.dataset['component_id'];
            var radio_tag = 'radio_product_component' + ev.currentTarget.value;
            var radio_tag_id =  document.getElementById(radio_tag);
            if(radio_tag_id.checked) {
                radio_tag_id.checked = false;
                ev.currentTarget.style.display = 'none';
                var current_tick = document.getElementById('tick_product'+product_id);
                if(current_tick){
                    current_tick.style.display='none';
                }
//                here is our
                //border class
                var image_sec = $(ev.currentTarget).parents('.product_image_section');
                image_sec[0].classList.remove('border_selected');
                //borderclass
//                reduce amount
                var current_total_amount = document.getElementById('new_updated_total').value;
                current_total_amount = current_total_amount ? current_total_amount : 0;
                var current_amount = document.getElementById('current_price_product'+product_id).value;
                current_amount = current_amount ? current_amount : 0;
                var new_amount = parseInt(current_total_amount)-parseInt(current_amount);
                new_amount = new_amount ? new_amount : 0;
                document.getElementById('new_updated_total').value = new_amount;
                var selected_amount = document.getElementById('prev_default_price_comp'+component_id).value;
                selected_amount = selected_amount ? selected_amount : 0;
                var updated_selected_amount = parseInt(selected_amount)-parseInt(current_amount);
                document.getElementById('prev_default_price_comp'+component_id).value = updated_selected_amount;


//                remove price tag other
                var current_class = 'test_comp_class'+component_id;
                    var other_price_tag = document.getElementsByClassName(current_class);
                    if(other_price_tag){
                        for (const tag of other_price_tag) {
                            if (tag.value) {
                                tag.value = null;
                            }
                        }
                    }
//                reduce power watt
                //power capacity
                var component_type = ev.currentTarget.dataset['component_type'];
                console.log('component_type',component_type)
                if(component_type != 'power'){
                    console.log('other')
                    var current_power = document.getElementById('power_watt_product'+product_id).value;
                    current_power = current_power ? current_power : 0;
                    var current_sum =  document.getElementById('power_capacity_sum').value;
                    current_sum = current_sum? current_sum:0;
                    var new_value = parseInt(current_sum)-parseInt(current_power);
                    new_value = new_value? new_value:0;

                    document.getElementById('power_capacity_sum').value = new_value;
                    document.getElementById('prev_power'+component_id).value = 0;
//                    call function to check capacity
                    this._checkCapacityCompatibility(component_id)
                }
            }else{
                null;
            }
        },

        _onClickSelection_quantities: function(ev){
            ev.stopPropagation();
            var selection_tag = 'selection_' + ev.currentTarget.value;
            var selection_tag_id =  document.getElementById(selection_tag);
            if(selection_tag_id){
                 if(selection_tag_id.style.display =='none') {
                    selection_tag_id.style.display = 'block';
                }else{
                    selection_tag_id.style.display = 'none';
                }
            }
        },

        _onClickRadio_buttons_class: function(ev){
            ev.stopPropagation();
            var component_id = ev.currentTarget.dataset['component_id'];
            var product_id = ev.currentTarget.dataset['product_id'];
            if(document.getElementById('radio_product_button'+product_id)){
                    var current_class = 'close_components_'+component_id;
                    var current_displayes_buttons = document.getElementsByClassName(current_class);
                    if(current_displayes_buttons){
                        for (const radioButton of current_displayes_buttons) {
                            if (radioButton.style.display == 'block') {
                                radioButton.style.display = 'none';
                                break;
                            }
                        }
                    }
                    var close_button = document.getElementById('radio_product_button'+product_id);
                    if(close_button.style.display == 'none'){
                       close_button.style.display = 'block';
                    }
                    else{
                        null;
                    }
                }
                else{
                    null;
                }
        },

        _onClickComponentsProducts: function (ev) {
            var component_id = ev.currentTarget.dataset['component_id'];
            var product_id = parseInt(ev.currentTarget.id);
            var self = this;
            var test = this.$(ev.currentTarget);
            var radio = self.$(ev.currentTarget).find('input[type="radio"]');
            if(radio[0].checked) {
                null;
            }else{
                radio[0].checked = true;
                //border class
                var glow_components_border = 'glow_component'+component_id;
                    var glow_components_borders = document.getElementsByClassName(glow_components_border);
                    if(glow_components_borders){
                        for (const glow_comp of glow_components_borders) {
                            if(glow_comp.classList.contains('border_selected')){
                                glow_comp.classList.remove("border_selected");
                                break;
                            }
                        }
                    }
                var image_sec = ev.currentTarget.querySelector('.product_image_section');;
                image_sec.classList.toggle('border_selected');
                //borderclass

                if(document.getElementById('radio_product_button'+ev.currentTarget.id)){
                    var current_class = 'close_components_'+component_id;
                    var current_displayes_buttons = document.getElementsByClassName(current_class);
                    if(current_displayes_buttons){
                        for (const radioButton of current_displayes_buttons) {
                            if (radioButton.style.display == 'block') {
                                radioButton.style.display = 'none';
                                break;
                            }
                        }
                    }
                    var close_button = document.getElementById('radio_product_button'+ev.currentTarget.id);
                    if(close_button.style.display == 'none'){
                       close_button.style.display = 'block';
                    }
                    else{
                        null;
                    }
                }
                else{
                    null;
                }
                //tick sections!
                var current_comp_ticks = document.getElementsByClassName('tick_component'+component_id);
                var current_tick = document.getElementById('tick_product'+product_id);
                for (const current of current_comp_ticks) {
                        if(current.style.display=='flex'){
                                    current.style.display = 'none';
                                    break;
                            }
                        }
                current_tick.style.display='flex';

                //total price updation
                var pre_amount = document.getElementById('prev_default_price_comp'+component_id).value;
                pre_amount = pre_amount ? pre_amount : 0;
                var current_amount = document.getElementById('current_price_product'+product_id).value;
                current_amount = current_amount ? current_amount : 0;
                var current_total_amount = document.getElementById('new_updated_total').value;
                current_total_amount = current_total_amount ? current_total_amount : 0;
                var new_amount = parseInt(current_total_amount)-parseInt(pre_amount)+parseInt(current_amount);
                console.log(new_amount,'new_amount33',typeof(new_amount));
                document.getElementById('new_updated_total').value = String(parseFloat(new_amount));;

                //price updations!!
                var prev_list_price_tag = document.getElementById('prev_default_price_comp'+component_id)
                var prev_list_price = prev_list_price_tag.value;
                var current_list_price_tag = document.getElementById('current_price_product'+product_id)
                var current_list_price = current_list_price_tag.value;
                prev_list_price_tag.value = current_list_price;
                var current_list_price_products = document.getElementsByClassName('current_price_class'+component_id);
                 for (const current of current_list_price_products) {
                        if(current.id == current_list_price_tag.id){
                            console.log('update ful price')
                            console.log(current.value);
                            var symbol = document.getElementById('currency_id').value;
                            // comment updation of price of current selected
                            document.getElementById('test_product'+product_id).value=null;
                        }
                        else{
                                var symbol = document.getElementById('currency_id').value;
                                if(parseInt(current.value) > current_list_price){
    //                                heree updation with product value instead of substring
                                    var new_value = parseFloat(parseInt(current.value) - current_list_price);
    //                                var new_id = current.id.substr(current.id.length - 4);
                                    var new_id = current.dataset['product_id'];
                                    var input_tag = document.getElementById('test_product'+new_id);
    //
                                    input_tag.value = '+'+String(new_value)+' '+symbol;
                                    input_tag.style.color = "red";
                                }
                                else if(parseInt(current.value) < current_list_price){
                                    var new_value = parseFloat(current_list_price - parseInt(current.value));
    //                                var new_id = current.id.substr(current.id.length - 4);
                                    var new_id = current.dataset['product_id'];;
                                    var input_tag = document.getElementById('test_product'+new_id);
                                    input_tag.value = '-'+String(new_value)+' '+symbol;
                                    input_tag.style.color = "#00ffd4";
                                }
                                else if(parseInt(current.value) == current_list_price){
    //                                here
    //                                var new_id = current.id.substr(current.id.length - 4);
                                    var new_id = current.dataset['product_id'];
                                    var input_tag = document.getElementById('test_product'+new_id);
                                    input_tag.value = '+'+'0'+' '+symbol;
                                    input_tag.style.color = "#00ffd4";
                                }
                            }
                            }

                //power capacity
                var component_type = ev.currentTarget.dataset['component_type'];
                console.log('component_type',component_type);
                if(component_type == 'power'){
                    var current_capacity = document.getElementById('power_capacity_product'+product_id).value;
                    current_capacity = current_capacity ? current_capacity : 0;
                    document.getElementById('power_capacity_total').value = current_capacity;
//                    call function to check capacity
                    this._checkCapacityCompatibility(component_id)

                }
                else if(component_type != 'power'){
                    var current_power = document.getElementById('power_watt_product'+product_id).value;
                    current_power = current_power ? current_power : 0;
                    var prev_power = document.getElementById('prev_power'+component_id).value;
                    prev_power = prev_power ? prev_power : 0;
                    var current_sum =  document.getElementById('power_capacity_sum').value;
                    var new_value = parseInt(current_sum)-parseInt(prev_power)+parseInt(current_power);
                    new_value = new_value? new_value:0;

                    document.getElementById('power_capacity_sum').value = new_value;
                    document.getElementById('prev_power'+component_id).value = current_power;
                    var main_product_id = document.getElementById('main_product_id').value;
                    var main_dict = {}
                    var specification_values = document.getElementsByClassName('specification_values');
                    for (const value of specification_values) {
                        main_dict[value.id]=value.value;
                    }
                    if((['cpu','board','cooler','case','memory','fans','m_2'].includes(component_type))){

                        var self = this;
                        ajax.jsonRpc('/get_components_data', 'call',{'id':product_id,'type':component_type,'main_product_id':main_product_id,'d':main_dict}).then(function (result) {
                            if(result){

                                if(component_type == 'cpu'){
                                    console.log('result-cpu',result)
                                    console.log('v',component_type)
                                    document.getElementById('prev_cpu_type').value = result['type'];
                                    document.getElementById('prev_cpu_oc').value = result['oc'];
                                    document.getElementById('prev_cpu_k_type').value = result['k'];
                                    console.log('resultdid',result['supported_dict'])
                                    document.getElementById('supported_dictionary').value =JSON.stringify(result['supported_dict']);
                                }
                                else if(component_type == 'board'){
                                    console.log('result-board',result)
                                    console.log('v',component_type)
                                    document.getElementById('board_cpu_type').value = result['pc_support'];
                                    document.getElementById('prev_memory_support_type').value = result['mmry_support'];
                                    document.getElementById('board_m2_num').value = result['m2'];
                                    document.getElementById('board_series_type').value = result['series'];
                                }
                                else if(component_type == 'cooler'){
                                    document.getElementById('cooler_type').value = result['cooler_type'];
                                    document.getElementById('cooler_air_height').value = result['cooler_air_height'];
                                    document.getElementById('cooler_radiator_size').value = result['cooler_radiator_size'];
                                    document.getElementById('cooler_fans_count').value = result['cooler_fans_count'];
                                }
                                else if(component_type == 'case'){
                                    document.getElementById('case_type_cooler').value = result['case_type_cooler'];
                                    document.getElementById('case_cooler_height').value = result['case_cooler_height'];
                                    document.getElementById('case_radiator_size_list').value = result['case_radiator_size_list'];
                                    document.getElementById('case_built_fans_no').value = result['case_built_fans_no'];
                                    document.getElementById('case_fans_support').value = result['case_fans_support'];

                                }
                                else if(component_type == 'memory'){
                                    document.getElementById('memory_type').value = result['type'];
                                }
                                else if(component_type == 'fans'){
                                    document.getElementById('fans_package_no').value = result['fans_package_no'];

                                }
                                else if(component_type == 'm_2'){
                                    document.getElementById('m_2_sum').value = result['m_2_sum'];

                                }
//                                functin call to check compatibility of components
                                self._checkComponentsCompatibility(component_id,component_type,product_id)

                            }
                        });

                    }
//                    call function to check capacity
                    this._checkCapacityCompatibility(component_id)
                }

            }

        },

        _checkComponentsCompatibility: function(component_id,component_type,product_id){
            if(component_type == 'cpu'){

                var cpu_oc = document.getElementById('prev_cpu_oc').value;
                if(cpu_oc == 'yes'){
                    var board_series_type = document.getElementById('board_series_type').value;
                    if(board_series_type != 'z'){
//                        notificatin!!
                        document.getElementById('cpu_board_noti').value = 1;
                        var board_id = $('#board_noti_div')[0].dataset['component_id'];
//                        var cpu_id = $('#cpu_noti_div')[0].dataset['component_id'];
//                        if(board_id && cpu_id){
                        if(board_id){
                            var div_id = '"#component_id'+board_id+'"'
//                            var div_id2 = '"#component_id'+cpu_id+'"'
//                            var result = '<div class="alert alert-warning">'+'The CPU selected is OC supported:Z-series board can be preferred'+'<a href='+div_id+'class="text-decoration-none" style="color: blue !important;">:Board</a>or'+'<a href='+div_id2+'class="text-decoration-none" style="color: blue !important;">:CPU</a></div>'
                            var result = '<div id="noti_123" class="customize_error">'+'The CPU selected is OC supported:Z-series board can be preferred: '+'<a href='+div_id+'class="text-decoration-none" style="color: white !important;">Board</a></div>'
//                            var result2 = '<div class="alert alert-warning">'+'The CPU selected is OC supported:Z-series board can be preferred'+
                            $('#board_noti_div').html(result);
                            document.getElementById('board_noti_div').classList.remove('d-none')
//                            $('#cpu_noti_div').html(result);
                        }

                    }
                    else{
                        document.getElementById('cpu_board_noti').value = 0;
                        $('#board_noti_div').html('');
                        document.getElementById('board_noti_div').classList.add('d-none')
//                        $('#cpu_noti_div').html('');
                    }

                }
                else{
                    document.getElementById('cpu_board_noti').value = 0;
                    $('#board_noti_div').html('');
                    document.getElementById('board_noti_div').classList.add('d-none')
//                    $('#cpu_noti_div').html('');
                }

                var board_cpu_type = document.getElementById('board_cpu_type').value;
                if(board_cpu_type){
                    var prev_cpu_type = document.getElementById('prev_cpu_type').value;
                    prev_cpu_type = prev_cpu_type? prev_cpu_type:0;
                    if (parseInt(prev_cpu_type) != parseInt(board_cpu_type)){
                        document.getElementById('cpu_board_type').value = 1;
//                        var board_comp_id = $('#board_cpu_type')[0].dataset['component_id'];
//                        if(board_comp_id && component_id){
//                            this._showErrorMessageProductCards(component_id,board_comp_id,'cpu','board')
//                        }

//                        var dict = JSON.parse(document.getElementById('supported_dictionary').value);
//                        var list_of_products = dict['cpu_supported_boards'];
//                        this._glow_product_cards(list_of_products)
//                        var list_of_products = dict['board_supported_cpu']
//                        this._glow_product_cards(list_of_products)
                        this._toDisableButton()
                    }
                    else{
                    //continue the flow
                        document.getElementById('cpu_board_type').value = 0;
                        var prev_cpu_k_type = document.getElementById('prev_cpu_k_type').value;
                        if(prev_cpu_k_type == 'yes'){

                            var cooler_type = document.getElementById('cooler_type').value;
                            if(cooler_type != 'air_cooler'){
                                document.getElementById('cpu_cooler_type').value = 1;
                                this._toDisableButton()
                            }
                            else{
                                document.getElementById('cpu_cooler_type').value = 0;
                                this._toEnableButton()
                            }
                        }
                        else{
                            document.getElementById('cpu_cooler_type').value = 0;
                            this._toEnableButton()
                        }
                        }
                }
            }
            else if(component_type == 'board'){
                var board_series_type = document.getElementById('board_series_type').value;
                var board_cpu_type = document.getElementById('board_cpu_type').value;
                var prev_memory_support_type = document.getElementById('prev_memory_support_type').value;
                if(board_series_type != 'z'){
                    var cpu_oc = document.getElementById('prev_cpu_oc').value;
                    if(cpu_oc == 'yes'){
                        document.getElementById('cpu_board_noti').value = 1;
                        var board_id = $('#board_noti_div')[0].dataset['component_id'];
//                        var cpu_id = $('#cpu_noti_div')[0].dataset['component_id'];
//                        if(board_id && cpu_id){
                        if(board_id){
                            var div_id = '"#component_id'+board_id+'"'
//                            var div_id2 = '"#component_id'+cpu_id+'"'
//                            var result = '<div class="customize_error">'+'The CPU selected is OC supported:Z-series board can be preferred: '+'<a href='+div_id+'class="text-decoration-none" style="color: white !important;">Board</a></div>'
                            var result = '<div id="noti_123" class="customize_error">'+'The CPU selected is OC supported:Z-series board can be preferred: '+'<a href='+div_id+'class="text-decoration-none" style="color: white !important;">Board</a></div>'

//                            var result2 = '<div class="alert alert-warning">'+'The CPU selected is OC supported:Z-series board can be preferred'+'<a href='+div_id2+'class="text-decoration-none" style="color: blue !important;">:CPU</a></div>'
                            $('#board_noti_div').html(result);
                            document.getElementById('board_noti_div').classList.remove('d-none')
//                            $('#cpu_noti_div').html(result);
                        }
                    }
                    else{
                        document.getElementById('cpu_board_noti').value = 0;
                        $('#board_noti_div').html('');
                        document.getElementById('board_noti_div').classList.add('d-none')
//                        $('#cpu_noti_div').html('');
                    }
                }
                else{
                    document.getElementById('cpu_board_noti').value = 0;
                    $('#board_noti_div').html('');
                    document.getElementById('board_noti_div').classList.add('d-none')
//                    $('#cpu_noti_div').html('');
                }



                if(board_cpu_type){
                    var prev_cpu_type = document.getElementById('prev_cpu_type').value;
                    prev_cpu_type = prev_cpu_type? prev_cpu_type:0;
                    if (parseInt(prev_cpu_type) != parseInt(board_cpu_type)){
                        document.getElementById('cpu_board_type').value = 1;
                        this._toDisableButton()
                    }
                    else{
                    //continue the flow
                        document.getElementById('cpu_board_type').value = 0;
                        if(prev_memory_support_type){
                            var memory_type = document.getElementById('memory_type').value;
                            memory_type = memory_type? memory_type:0;
                            if(parseInt(memory_type) != parseInt(prev_memory_support_type)){
                                document.getElementById('board_memory_type').value =1;
                                this._toDisableButton()
                            }
                            else{
                                document.getElementById('board_memory_type').value =0;
                                var board_m2_num = document.getElementById('board_m2_num').value;
                                var m_2_sum = document.getElementById('m_2_sum').value;
                                board_m2_num = board_m2_num? board_m2_num:0;
                                m_2_sum = m_2_sum? m_2_sum:0;
                                if(parseInt(m_2_sum) > parseInt(board_m2_num)){
                                    document.getElementById('board_m2_match').value =1;
                                    this._toDisableButton()
                                }
                                else{
                                    document.getElementById('board_m2_match').value =0;
                                    this._toEnableButton()
                                }
//                                this._toEnableButton()
//                                check m2 support
                            }
                        }
                        else{
                            console.log('error-value unfound')
                        }
                    }
                }
                else{
                    console.log('error-value unfound')
                }
            }
            else if(component_type == 'case'){

                var case_type_cooler = document.getElementById('case_type_cooler').value;
                var case_radiator_size_list = document.getElementById('case_radiator_size_list').value;
                var total_fans_support = document.getElementById('case_fans_support').value;
                var case_built_fans_no = document.getElementById('case_built_fans_no').value;
                total_fans_support = total_fans_support? total_fans_support:0;
                case_built_fans_no = case_built_fans_no? case_built_fans_no:0;
                var available_fans_no = parseInt(total_fans_support) - parseInt(case_built_fans_no);
                if(available_fans_no){
                    var cooler_fans_count = document.getElementById('cooler_fans_count').value;
                    cooler_fans_count = cooler_fans_count? cooler_fans_count:0;
                    fans_package_no = document.getElementById('fans_package_no').value;
                    fans_package_no = fans_package_no? fans_package_no:0;
                    var updated_fans = parseInt(cooler_fans_count)+parseInt(fans_package_no)
                    if(parseInt(available_fans_no) < parseInt(updated_fans)){
                        console.log('error-fans-limit-exceed')
                        document.getElementById('fans_error').value = 1;
                        this._toDisableButton()
                        if(parseInt(cooler_fans_count) > parseInt(available_fans_no)){
                            console.log('cooler-fans-count-greater')
                        }
                        if(parseInt(fans_package_no) > parseInt(available_fans_no)){
                            console.log('package-fans-count-greater')
                        }
                    }
                    else{
//                        continue workflow
                                document.getElementById('fans_error').value = 0;
                                if(case_radiator_size_list){
                                        var r_array = case_radiator_size_list.split(',').map(Number);
                                        var cooler_radiator_size = document.getElementById('cooler_radiator_size').value;
                                        cooler_radiator_size = cooler_radiator_size? cooler_radiator_size:0;
                                        if(r_array.includes(parseInt(cooler_radiator_size))){
                                            console.log('size_includes')
                                            document.getElementById('cooler_case_radi').value = 0;
//        //                                    workflow continue
                                            if(case_type_cooler){
                                                var cooler_type = document.getElementById('cooler_type').value;
                                                if(case_type_cooler == 'water_cooler'){

                                                    if(cooler_type != case_type_cooler){
                                                        document.getElementById('cooler_case_type').value = 1;
                                                        this._toDisableButton()
                                                        console.log('case-cooler-water-type-mismatch!!')
                                                    }
                                                    else{
                                                        document.getElementById('cooler_case_type').value = 0;
                                                        this._toEnableButton()
                                                    }
                                                }

                                                else if(case_type_cooler == 'both'){
                                                    if(['air_cooler','water_cooler'].includes(cooler_type)){
                                                        if(cooler_type == 'air_cooler'){
                                                            var case_cooler_height = document.getElementById('case_cooler_height').value;
                                                            case_cooler_height = case_cooler_height? case_cooler_height:0;
                                                            var cooler_air_height = document.getElementById('cooler_air_height').value;
                                                            cooler_air_height = cooler_air_height? cooler_air_height:0;
                                                            if(parseInt(case_cooler_height) <= parseInt(cooler_air_height)){
                                                                console.log('case-coooler-height-exceeded!!')
                                                                document.getElementById('cooler_case_height').value = 1;
                                                                this._toDisableButton()
                                                            }
                                                            else{
                                                                document.getElementById('cooler_case_height').value = 0;
                                                                this._toEnableButton()
                                                            }
                                                        }
                                                        else{
                                                            document.getElementById('cooler_case_type').value = 1;
                                                            this._toDisableButton()
                                                        }
                                                    }
                                                    else{
                                                        document.getElementById('cooler_case_type').value = 1;
                                                        this._toDisableButton()
                                                    }

                            }
                                                else if(case_type_cooler == 'air_cooler'){
                                                    if(cooler_type == 'air_cooler') {
                                                        var case_cooler_height = document.getElementById('case_cooler_height').value;
                                                        case_cooler_height = case_cooler_height? case_cooler_height:0;
                                                        var cooler_air_height = document.getElementById('cooler_air_height').value;
                                                        cooler_air_height = cooler_air_height? cooler_air_height:0;
                                                        if(parseInt(case_cooler_height) <= parseInt(cooler_air_height)){
                                                            console.log('case-coooler-height-exceeded!!')
                                                            document.getElementById('cooler_case_height').value = 1
                                                            this._toDisableButton()
                                                        }
                                                        else{
                                                            document.getElementById('cooler_case_height').value = 0
                                                            this._toEnableButton()
                                                        }
                                                    }
                                                    else{
                                                        document.getElementById('cooler_case_type').value = 1;
                                                        this._toDisableButton()
                                                        console.log('cooler-type-should be air')
                                                    }
                                                }
                                            }
                                            else{
                                                console.log('error-value-unknown!!')
                                            }
//
                                        }
                                        else{
                                            this._toDisableButton()
                                            console.log('error-case-r-list-not include!!!')
                                            document.getElementById('cooler_case_radi').value = 1;
                                        }
                                }
                                else{
                                    this._toEnableButton()
                                    console.log('eror-value-unknwn')
                               }
                    }
//                    workend
                }
                else{
                    console.log('eror-value-unknwn')
                }

            }
            else if(component_type == 'cooler'){
                var cooler_type = document.getElementById('cooler_type').value;
                var prev_cpu_k_type = document.getElementById('prev_cpu_k_type').value;
                var case_type_cooler = document.getElementById('case_type_cooler').value;
                if(cooler_type == 'air_cooler'){
                    if(!['air_cooler','both'].includes(case_type_cooler)){
                        console.log('error-cooler need to be this case type!!')
                        document.getElementById('cooler_case_type').value = 1;
                        this._toDisableButton()
                    }
                    else{
                        document.getElementById('cooler_case_type').value = 0;
                        var cooler_radiator_size = document.getElementById('cooler_radiator_size').value;
                        var case_radiator_size_list = document.getElementById('case_radiator_size_list').value;
                        if(case_radiator_size_list){
                            var r_array = case_radiator_size_list.split(',').map(Number);
                            if(!r_array.includes(parseInt(cooler_radiator_size))){
                                console.log('cooler-radiator-not-included')
                                document.getElementById('cooler_case_radi').value = 1;
                                this._toDisableButton()
                            }
                           //end
                            else{
                                document.getElementById('cooler_case_radi').value = 0;
                                var cooler_air_height = document.getElementById('cooler_air_height').value;
                                var case_cooler_height = document.getElementById('case_cooler_height').value;
                                cooler_air_height = cooler_air_height? cooler_air_height:0;
                                case_cooler_height = case_cooler_height? case_cooler_height:0;
                                if(parseInt(cooler_air_height)>parseInt(case_cooler_height)){
                                    console.log('eror-cooler-size-exceed')
                                    document.getElementById('cooler_case_height').value = 1;
                                    this._toDisableButton()
                                }
                                else{
                                    document.getElementById('cooler_case_height').value = 0;
                                    var total_fans_support = document.getElementById('case_fans_support').value;
                                    var case_built_fans_no = document.getElementById('case_built_fans_no').value;
                                    total_fans_support = total_fans_support? total_fans_support:0;
                                    case_built_fans_no = case_built_fans_no? case_built_fans_no:0;
                                    var available_fans_no = parseInt(total_fans_support) - parseInt(case_built_fans_no);
                                    if(available_fans_no){
                                        var cooler_fans_count = document.getElementById('cooler_fans_count').value;
                                        cooler_fans_count = cooler_fans_count? cooler_fans_count:0;
                                        fans_package_no = document.getElementById('fans_package_no').value;
                                        fans_package_no = fans_package_no? fans_package_no:0;
//
                                        if(parseInt(available_fans_no)>parseInt(fans_package_no)){
                                            var check_fans_latest = parseInt(available_fans_no)-parseInt(fans_package_no)
                                            if(check_fans_latest){
                                                if(parseInt(cooler_fans_count)<=parseInt(check_fans_latest)){
                                                    console.log('ok')
                                                    document.getElementById('fans_error').value = 0;
                                                    this._toEnableButton()
                                                }
                                                else{
                                                    document.getElementById('fans_error').value = 1;
                                                    this._toDisableButton()
                                                    console.log('rror-cooler-fans-count-not-valid!!')
                                                }
                                            }
                                            else{
                                                document.getElementById('fans_error').value = 1;
                                                this._toDisableButton()
                                            }
                                        }
                                        else{
                                            document.getElementById('fans_error').value = 1;
                                            console.log('error')
                                            this._toDisableButton()
                                        }
//
                                            }
                                    else{
                                        this._toDisableButton()
                                        console.log('unknonw vaulue')
                                    }
                                }
                            }//end
                        }
                        else{
                            console.log('nothing')
                        }
                    }
//
//
//
                    }
                else if(cooler_type == 'water_cooler'){
                    if(prev_cpu_k_type == 'yes'){
                          console.log('cooler-liquid-need')
                          document.getElementById('cooler_case_type').value = 1;
                          this._toDisableButton()
                    }
                    else{
                        document.getElementById('cooler_case_type').value = 0;
                        console.log('let go')
                        if(!['water_cooler','both'].includes(case_type_cooler)){
                            document.getElementById('cooler_case_type').value = 1;
                            console.log('error-cooler need to be this case type!!')
                            this._toDisableButton()
                        }
                        else{
                            document.getElementById('cooler_case_type').value = 0;
                            var cooler_radiator_size = document.getElementById('cooler_radiator_size').value;
                            var case_radiator_size_list = document.getElementById('case_radiator_size_list').value;
                            if(case_radiator_size_list){
                            var r_array = case_radiator_size_list.split(',').map(Number);
                            if(!r_array.includes(parseInt(cooler_radiator_size))){
                                console.log('cooler-radiator-not-included')
                                document.getElementById('cooler_case_radi').value = 1;
                                this._toDisableButton()
                            }
                           //end
                            else{
                                    document.getElementById('cooler_case_radi').value = 0;
                                    var total_fans_support = document.getElementById('case_fans_support').value;
                                    var case_built_fans_no = document.getElementById('case_built_fans_no').value;
                                    total_fans_support = total_fans_support? total_fans_support:0;
                                    case_built_fans_no = case_built_fans_no? case_built_fans_no:0;
                                    var available_fans_no = parseInt(total_fans_support) - parseInt(case_built_fans_no);
                                    if(available_fans_no){
                                        document.getElementById('fans_error').value = 0;
                                        var cooler_fans_count = document.getElementById('cooler_fans_count').value;
                                        cooler_fans_count = cooler_fans_count? cooler_fans_count:0;
                                        fans_package_no = document.getElementById('fans_package_no').value;
                                        fans_package_no = fans_package_no? fans_package_no:0;
//
//                                    //again removing the packafge count if:
                                        if(parseInt(available_fans_no)>parseInt(fans_package_no)){
                                            var check_fans_latest = parseInt(available_fans_no)-parseInt(fans_package_no)
                                            if(check_fans_latest){
                                                if(parseInt(cooler_fans_count)<=parseInt(check_fans_latest)){
                                                    document.getElementById('fans_error').value = 0;
                                                    this._toEnableButton()
                                                }
                                                else{
                                                    document.getElementById('fans_error').value = 1;
                                                    this._toDisableButton()
                                                    console.log('rror-cooler-fans-count-not-valid!!')
                                                }
                                            }
                                            else{
                                                document.getElementById('fans_error').value = 1;
                                                this._toDisableButton()

                                            }
                                        }
                                        else{
                                            console.log('error')
                                            document.getElementById('fans_error').value = 1;
                                            this._toDisableButton()
                                        }
//
                                            }
                                    else{
                                        document.getElementById('fans_error').value = 1;
                                        this._toDisableButton()
                                    }
                            }
                            //end
                            }
                            else{
                                this._toDisableButton()
                            }
                        }
                    }
                }
            }
            else if(component_type == 'fans'){
                var fans_package_no = document.getElementById('fans_package_no').value;
                var total_fans_support = document.getElementById('case_fans_support').value;
                var case_built_fans_no = document.getElementById('case_built_fans_no').value;
                total_fans_support = total_fans_support? total_fans_support:0;
                case_built_fans_no = case_built_fans_no? case_built_fans_no:0;
                var available_fans_no = parseInt(total_fans_support) - parseInt(case_built_fans_no);
                if(available_fans_no){
                        document.getElementById('fans_error').value = 0;
                        var cooler_fans_count = document.getElementById('cooler_fans_count').value;
                        cooler_fans_count = cooler_fans_count? cooler_fans_count:0;
                        fans_package_no = document.getElementById('fans_package_no').value;
                        fans_package_no = fans_package_no? fans_package_no:0;
                        var updated_fans = parseInt(available_fans_no)-parseInt(cooler_fans_count)
                        if(parseInt(updated_fans) < parseInt(fans_package_no)){
                            console.log('error-fans package-limit-exceed')
                            document.getElementById('fans_error').value = 1;
                            this._toDisableButton()
                        }
                        else{
                            document.getElementById('fans_error').value = 0;
                            console.log('error-offff')
                            this._toEnableButton()
                        }
                    }
                else{
                    console.log('error')
                    document.getElementById('fans_error').value = 1;
                    this._toDisableButton()
                }
            }
            else if(component_type == 'memory'){
                console.log('lmemeory')
                var prev_memory_support_type = document.getElementById('prev_memory_support_type').value;
                var memory_type = document.getElementById('memory_type').value;
                memory_type = memory_type? memory_type:0;
                prev_memory_support_type = prev_memory_support_type? prev_memory_support_type:0;
                if(parseInt(memory_type) != parseInt(prev_memory_support_type)){
                        console.log('memorya-memory-mis!!error');
                        document.getElementById('board_memory_type').value = 1;
                        this._toDisableButton()
                }
                else{
                    document.getElementById('board_memory_type').value = 0;
                    console.log('memory-off');
                    this._toEnableButton()
                }
            }
            else if(component_type == 'm_2'){
                var board_m2_num = document.getElementById('board_m2_num').value;
                var m_2_sum = document.getElementById('m_2_sum').value;
                board_m2_num = board_m2_num? board_m2_num:0;
                m_2_sum = m_2_sum? m_2_sum:0;
                if(parseInt(m_2_sum) > parseInt(board_m2_num)){
                        console.log('board-m2-mis!!error');
                        document.getElementById('board_m2_match').value = 1;
                        this._toDisableButton()
                }
                else{
                    console.log('board-m2-off');
                    document.getElementById('board_m2_match').value = 0;
                    this._toEnableButton()
                }
            }
            this._check_errors()
//
        },

        _check_errors:function(){
            var switches = document.getElementsByClassName('switch_cases');
                    var test = []
                    for (const sw of switches) {
                        if(parseInt(sw.value)){
                            sw.value
                            test.push(sw.dataset['error_msg'])
                        }
                    }
                    if(test.length){
                        var ul = document.getElementById("errors_list_ul");
                        ul.innerHTML = '';
                        for (const l of test) {
                            var li = document.createElement('li');
                            li.appendChild(document.createTextNode(l));
                            ul.appendChild(li);
                        }
                    }
//                    else{
//                        document.getElementById('total_errors_2').classList.add("d-none")
//                        console.log('j')
//                    }
        },

        _glow_product_cards:function(list_of_products){
            console.log('list_of_products',list_of_products)
            for (const id of list_of_products) {
//                                here\
                  var glow_id = 'glow_'+id;
                  var g_id = document.getElementById(glow_id);
                  console.log(g_id)
                  if(g_id){
                    g_id.classList.add("ia-selectables--glow-green")
                  }
            }
        },

        _checkCapacityCompatibility: function (component_id) {
                console.log('component12',component_id)
                var power_capacity_sum = document.getElementById('power_capacity_sum').value;
                power_capacity_sum = power_capacity_sum ? power_capacity_sum:0;
                var total_capacity = document.getElementById('power_capacity_total').value;
                var current_power_div_id = document.getElementById('power_supply_uniq').value;
                current_power_div_id = current_power_div_id? current_power_div_id:0;
                total_capacity = total_capacity? total_capacity:0;
                console.log(power_capacity_sum,total_capacity)
                if(parseInt(power_capacity_sum) > parseInt(total_capacity)){
                    document.getElementById('power_capacity_sum').style.color = "red";
                    document.getElementById('power_capacity_total').style.color = "red";
                    $('#add_total_project_btn').prop('disabled', true);
                    $('#add_total_project_btn').css('cursor', 'not-allowed');
                    document.getElementById('power_supply_error').value =1;
                    this._hideGlowingPowerCards();
                    this._fetchGlowingPowerCards(component_id,power_capacity_sum);
                    this._showErrorMessage();

                }
                else{
//                    here new code
                    document.getElementById('power_capacity_sum').style.color = "#00ffd4";
                    document.getElementById('power_capacity_total').style.color = "#00ffd4";
                    document.getElementById('power_supply_error').value =0;
                    this._hideGlowingPowerCards();
                    this._hideErrorMessage();
                    var switcheinputs = document.getElementsByClassName('switch_cases');
                    var test = []
                    for (const switcheinput of switcheinputs) {
                        test.push(parseInt(switcheinput.value))
                    }
                    if(!test.includes(1)){
                        $('#add_total_project_btn').prop('disabled', false);
                        $('#add_total_project_btn').css('cursor', 'pointer');
                    }


                }
        },

        _onMouseOverAdd:function(ev){
                var btn = $('#add_total_project_btn')
                if(btn.prop('disabled')){
                    document.getElementById('total_errors_2').classList.remove('d-none');
                }
                else{
                    document.getElementById('total_errors_2').classList.add('d-none');
//                    var error_div = $('#total_errors_2')
//                    error_div.classList.add("d-none")
                }
        },

        _onMouseLeaveAdd:function(ev){
            document.getElementById('total_errors_2').classList.add('d-none');
        },

//        _showErrorMessageProductCards:function(id,name){
//            var div = '#error'+id;
//            if(div){
//                var div_id = '"#component_id'+id+'"'
//                var result = '<div class="alert alert-warning">'+'There are some compatibility issues:please change'+'<a href='+div_id+'class="text-decoration-none" style="color: blue !important;">:'+name+'</a></div>'
//                $(div).html(result);
//            }
//        },
//        _showErrorMessageProductCards:function(id,id2,name1,name2){
//            console.log(id,id2,name1,name2)
//            var div = '#error'+id;
//            var div2 = '#error'+id2;
//            if(div && div2){
//                var div_id = '"#component_id'+id+'"'
//                var div_id2 = '"#component_id'+id2+'"'
//                console.log(div_id,div_id2,'<==>')
//                var result = '<div class="alert alert-warning">'+'There are some compatibility issues:please change to highlighted ones'+'<a href='+div_id+'class="text-decoration-none" style="color: blue !important;">:'+name1+'</a>or'+'<a href='+div_id2+'class="text-decoration-none" style="color: blue !important;">:'+name2+'</a></div>'
//                $(div).empty().html(result);
//                $(div2).empty().html(result);
//            }
//        },


        _showErrorMessage:function(){
            var pow_component_id = document.getElementById('power_supply_uniq').value;
            console.log('pow_component_id',pow_component_id)
            var div = '#error_power'+pow_component_id;
            console.log(div)
            if(div){
                console.log('div',div);
                var div_id = '"#component_id'+pow_component_id+'"'
                var result = '<div class="customize_error mb-3">'+'Error in powersupply please change to highlighted One: '+'<a href='+div_id+'class="text-decoration-none" style="color: white !important;">PowerSupply</a></div>'
                $(div).html(result);
            }
        },

        _hideErrorMessage:function(){
            var pow_component_id = document.getElementById('power_supply_uniq').value;
            var div = '#error_power'+pow_component_id;
            if(div){
                $(div).html('');
            }
        },

        _hideGlowingPowerCards:function(){
            var pow_component_id = document.getElementById('power_supply_uniq').value;
            var power_cards = document.getElementsByClassName('glow_component'+pow_component_id);
                        for (const power_card of power_cards) {
                            if(power_card.classList.contains('ia-selectables--glow-green')){
                                power_card.classList.remove("ia-selectables--glow-green");
                            }
                        }
        },

        _fetchGlowingPowerCards: function(id,sum){
            var current_power_div_id = document.getElementById('power_supply_uniq').value;
            console.log(current_power_div_id)
            current_power_div_id = current_power_div_id? current_power_div_id:0;
            var last_click_section_id = id;
            var sum = sum;
            var product_id = document.getElementById('main_product_id').value;
            ajax.jsonRpc('/get_glowing_power_cards', 'call',{'sum':sum,'id':last_click_section_id,'power_id':current_power_div_id,'product_id':product_id}).then(function (result) {
                    if(result){
                        console.log('result',result)
                        for (const id of result) {
//                                here\
                                  var glow_id = 'glow_'+id;
                                  var g_id = document.getElementById(glow_id);
                                  console.log(g_id)
                                  if(g_id){
                                    console.log('gid',g_id.id)
                                    g_id.classList.add("ia-selectables--glow-green")
                                  }
                        }
                    }
                });

        },

        _toDisableButton: function (ev) {
                $('#add_total_project_btn').prop('disabled', true);
                $('#add_total_project_btn').css('cursor', 'not-allowed');
        },

        _toEnableButton: function (ev) {
            var switcheinputs = document.getElementsByClassName('switch_cases');
            var test = []
            for (const switcheinput of switcheinputs) {
                test.push(parseInt(switcheinput.value))
            }
            if(!test.includes(1)){
                 $('#add_total_project_btn').prop('disabled', false);
                $('#add_total_project_btn').css('cursor', 'pointer');
            }
//                        if()
//                        if(!test){
//                            $('#add_total_project_btn').prop('disabled', false);
//                            $('#add_total_project_btn').css('cursor', 'pointer');
//                        }

//                            else{
//                                $('#add_total_project_btn').prop('disabled', false);
//                                $('#add_total_project_btn').css('cursor', 'pointer');
//                            }


        },

        _onClickComponentsProducts2: function (ev) {
            var checkbox = self.$(ev.currentTarget).find('input[type="checkbox"]')
            var selection = self.$(ev.currentTarget).find('select[name="number_quantities"]');
            var component_id = ev.currentTarget.dataset['component_id'];
            var product_id = ev.currentTarget.dataset['product_id'];
            var allowed_selection_count = document.getElementById('allowed_sel_component'+component_id).value;
            var total_allowed = document.getElementById('total_allowed_component'+component_id).value;
            if(checkbox[0].checked) {
//                tick section
                var current_tick = document.getElementById('tick_product'+product_id);
                if(current_tick){
                    current_tick.style.display='none'
                }
                checkbox[0].checked = false;


                var price_d_class = document.getElementById('test_product'+product_id)
//                price_d_class.classList.remove("d-none")
                console.log('yesi te')


                selection.css('display','none');
                var pre_tag = document.getElementById('prev_chose'+product_id);
                if(pre_tag){
                            //total amount updation new
                        var current_multiple = pre_tag.value;
                        pre_tag.value =0;
                        console.log(current_multiple,'lll')
                        current_multiple = current_multiple ? current_multiple : 0;

                        var current_price = document.getElementById('current_price_product'+product_id).value;
                        var current_total = document.getElementById('new_updated_total').value;
                        console.log('j',current_total,current_price,current_multiple)
                        var new_amount = parseInt(current_total)-(parseInt(current_price)*parseInt(current_multiple))
                        console.log(current_multiple,current_price)
                        document.getElementById('new_updated_total').value = String(parseFloat(new_amount));

                        //multi watt decrease
                        var current_power = document.getElementById('power_watt_product'+product_id).value;
                        current_power = current_power ? current_power : 0;
                        var power_capacity = document.getElementById('power_capacity_sum').value;
                        power_capacity = power_capacity ? power_capacity:0;
                        var new_value = parseInt(power_capacity)-(parseInt(current_power)*parseInt(current_multiple))
                        document.getElementById('power_capacity_sum').value = new_value;
                        this._checkCapacityCompatibility()
                }
                else{
//                    new sel
                      var no_of_sel = document.getElementById('allowed_sel_component'+component_id).value;
                      console.log(no_of_sel,typeof(no_of_sel))
                      if(parseInt(no_of_sel) ==1){

                                //total amount updation
                                console.log('enter')
                                var current_price = document.getElementById('current_price_product'+product_id).value;
                                var current_multiple = 1;
                                var current_total = document.getElementById('new_updated_total').value;
                                var new_amount = parseInt(current_total)-(parseInt(current_price)*parseInt(current_multiple))
                                console.log(new_amount,'new_amount44',typeof(new_amount));
                                document.getElementById('new_updated_total').value = String(parseFloat(new_amount));


                                //single multi watt decrease
                                 var component_type = ev.currentTarget.dataset['component_type'];
                                 console.log('component_type',component_type)
                                 if(component_type != 'power'){
                                       var current_power = document.getElementById('power_watt_product'+product_id).value;
                                       current_power = current_power ? current_power : 0;
                                       var power_capacity = document.getElementById('power_capacity_sum').value;
                                       power_capacity = power_capacity ? power_capacity:0;
                                       var new_value = parseInt(power_capacity) - parseInt(current_power)
                                       document.getElementById('power_capacity_sum').value = new_value;
                                       this._checkCapacityCompatibility()
                                }
                            }
                }

                var selection_tag = document.getElementById('selection_'+product_id);
//                if(pre_tag){pre_tag.value = 0;}
                if(selection_tag){
                    var new_sum= selection_tag.value;
                    selection_tag.value = 0;
                }
                var component_total_div = document.getElementById('total_allowed_component'+component_id);
                component_total_div.value= parseInt(component_total_div.value)+parseInt(new_sum);
                var check_class_component = 'check_class_component'+component_id;
                var checkboxes = document.getElementsByClassName(check_class_component);
                if(component_total_div.value){
                    if(checkboxes){
                        for (const checkbox of checkboxes) {
                            if(checkbox.checked){
//                                here\
                                  var id = checkbox.value;
                                  var selection_id = '#selection_'+id;
                                  if(selection_id){
                                  var current_value = document.getElementById('selection_'+id).value;
                                  $(selection_id)[0].options.length = 0;
                                    for(var i=1;i<(parseInt(component_total_div.value)+parseInt(current_value)+1);i++){
                                        if(i == parseInt(current_value)){
                                            $(selection_id).append('<option selected="selected" value="'+i+'">'+i+'</option>');
                                        }
                                        else{$(selection_id).append('<option value="'+i+'">'+i+'</option>');}
                                    }
                                }
                            }
                            else{
//                                here
                                var id = checkbox.value;
                                var selection_id = '#selection_'+id;
                                if($(selection_id)[0]){
                                $(selection_id)[0].options.length = 0;
                                for(var i=1;i<parseInt(component_total_div.value)+1;i++){
                                    $(selection_id).append('<option value="'+i+'">'+i+'</option>');
                                    }
                                }
                            }
                        }
                    }}

            }else{
                var checkboxes = document.getElementsByClassName('check_class_component'+component_id);
                var selections = document.getElementsByClassName('selection_class_component'+component_id);
                var selected=0;
                var total= 0;
                var selected_ids = [];
                for (const checkbox_current of checkboxes) {
                        if(checkbox_current.checked){
                                selected=selected+1;
                                selected_ids.push(checkbox_current.value);
                            }
                        }
                if(selected<allowed_selection_count){
                    var check_zero = parseInt(document.getElementById('total_allowed_component'+component_id).value);
                    if(check_zero){
                        checkbox[0].checked = true;

                        //price show
                        var price_d_class = document.getElementById('test_product'+product_id)
//                        price_d_class.classList.add("d-none")


                        selection.css('display','block');

                         //                tick section2
                        var current_tick = document.getElementById('tick_product'+product_id);
                        if(current_tick){
                            current_tick.style.display='block'
                        }
                        //allowed updation
                        var current_selected_no = document.getElementById('selection_'+product_id).value;
                        current_selected_no = current_selected_no? current_selected_no:0;
                        var prev_allowed_no = document.getElementById('total_allowed_component'+component_id).value;
                        prev_allowed_no = prev_allowed_no? prev_allowed_no:0;
                        var new_allowed_no_up = parseInt(prev_allowed_no)-parseInt(current_selected_no)
                        document.getElementById('total_allowed_component'+component_id).value = new_allowed_no_up;

                        //total amount updation
                        var current_price = document.getElementById('current_price_product'+product_id).value;
                        var current_multiple = document.getElementById('selection_'+product_id).value;
                        current_multiple = current_multiple ? current_multiple : 0;
                        var current_total = document.getElementById('new_updated_total').value;
                        var new_amount = parseInt(current_total)+(parseInt(current_price)*parseInt(current_multiple))
                        console.log(new_amount,'new_amount55',typeof(new_amount));
                        document.getElementById('new_updated_total').value = String(parseFloat(new_amount));

                        var pre_tag22 = document.getElementById('prev_chose'+product_id);
                        if(pre_tag22){
                            pre_tag22.value = parseInt(current_multiple);
                        }
                        //multi watt increase
                        var current_power = document.getElementById('power_watt_product'+product_id).value;
                        current_power = current_power ? current_power : 0;
                        var power_capacity = document.getElementById('power_capacity_sum').value;
                        power_capacity = power_capacity ? power_capacity:0;
                        var new_value = parseInt(power_capacity)+(parseInt(current_power)*parseInt(current_multiple))
                        document.getElementById('power_capacity_sum').value = new_value;
                        this._checkCapacityCompatibility()
                    }
                    else{
                        var no_of_sel = document.getElementById('allowed_sel_component'+component_id).value;
                        if(parseInt(no_of_sel) ==1){
                                checkbox[0].checked = true;
                                selection.css('display','block');

                                 //                tick section2
                                var current_tick = document.getElementById('tick_product'+product_id);
                                if(current_tick){
                                    current_tick.style.display='block'
                                }

                                //total amount updation
                                var current_price = document.getElementById('current_price_product'+product_id).value;
                                var current_multiple = 1;
                                var current_total = document.getElementById('new_updated_total').value;
                                var new_amount = parseInt(current_total)+(parseInt(current_price)*parseInt(current_multiple))
                                console.log(new_amount,'new_amount66',typeof(new_amount));
                                document.getElementById('new_updated_total').value = String(parseFloat(new_amount));

                                 //single multi watt increase
                                 var component_type = ev.currentTarget.dataset['component_type'];
                                 console.log('component_type',component_type)
                                 if(component_type != 'power'){
                                       var current_power = document.getElementById('power_watt_product'+product_id).value;
                                       current_power = current_power ? current_power : 0;
                                       var power_capacity = document.getElementById('power_capacity_sum').value;
                                       power_capacity = power_capacity ? power_capacity:0;
                                       var new_value = parseInt(current_power)+parseInt(power_capacity)
                                       document.getElementById('power_capacity_sum').value = new_value;
                                       this._checkCapacityCompatibility()
                                }
                            }
                    }
                }
                else{
                        for (const check of checkboxes) {
                            if(selected_ids.includes(check.value)){
                                    null;
                                }
                            else{
                                 check.disabled = true;
                                }
                        }
                }
            }
        }
    });
});
