odoo.define('iwesabe_website_theme.discount', function(require) {
    const ajax = require('web.ajax');
    $(document).on("click", "#discountBtn", function() {
    var discount_val = $("#discountCodeInput")[0].value
    return ajax.jsonRpc('/shop/discount', 'call', {
            'promo': discount_val
        }).then(function(result) {
        var status = result['coupon_status']
        if (status['error']){
         var pro = $('#promo_code')[0]
         $('#promo_code').show()
        }
        else{
        location.reload()
        }
        })
    });

     $(document).on("click", "#revdiscountBtn", function() {
       return ajax.jsonRpc('/shop/rev/discount', 'call', {
        }).then(function(result) {
           var flag = result['flag']
            console.log("f", result)
           if(result==2){
           location.reload()
           }
        })

     })
    })
