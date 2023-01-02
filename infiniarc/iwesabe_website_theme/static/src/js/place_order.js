odoo.define('iwesabe_website_theme.place_order', function(require) {
    const ajax = require('web.ajax');
    var core = require('web.core');
    var QWeb = core.qweb;
    $(document).on("click", "#paynow", function() {
    console.log("paynow", this)
    var mer_reference = $("#merchantrfr").val()
    console.log("mercrefer", mer_reference)
    var radio_btn = $("#v-pills-tab")[0]
    console.log("rad", radio_btn)
    var buttons = $(".ia-radio-tab__link")
    console.log("button", buttons)
    var test = []
    for (const active_btn of buttons) {
        if(active_btn.classList.contains("active")){
        test.push(active_btn)
        }
}
    var form = $("#request_order")
    console.log("form", form)
    console.log('test', test[0])
    if(test[0]){
    var active_acquirer = test[0].dataset.provider
    var active_acquirer_id = test[0].id
    console.log('acaq', active_acquirer)
    return ajax.jsonRpc('/payment/transaction/custom', 'call', {
        'active':active_acquirer
        }).then(function(result){
         console.log("resu", result['merchant_reference'])
//         mer_reference = result['merchant_reference']
                if(result['provider']=="payfort"){
                form.submit()
                console.log(form)}
        else{
          var modal = document.getElementById("quick_view_special_shop")
          console.log("modal", modal)
            window.location = '/page_render';
        }
         });
        }
    else{
     $("#chose_payment").show()
    }
    $(document).on("click", "#v-pills-tab", function() {
     console.log("change")
     $("#chose_payment").hide()
    })
   })
   })