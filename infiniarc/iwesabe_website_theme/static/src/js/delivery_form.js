odoo.define('iwesabe_website_theme.delivery_form', function(require) {
    $(document).on("change", "#inlineCheckbox1", function() {
    console.log("del", this)
     var partner_name = $("#name")[0].value
     console.log("del", partner_name)
     var partner_addr = $("#street")[0].value
     console.log("del", partner_addr)
     var partner_phone = $("#phone")[0]
     console.log("delph", partner_phone)
//     var partner_country = $("country_val")[0].value
//     console.log("del", partner_country)
     var partner_city = $("#city_val")[0].value
     console.log("del", partner_city)
     var partner_zip = $("#zip_val")[0].value
     console.log("del", partner_zip)
     var del_name = $("#del_name")[0]
     var del_phone = $("#del_phone")[0]
     var del_addr = $("#del_addr")[0]
     var del_city_name = $("#del_city_name")[0]
     var del_zip_v = $("#del_zip_v")[0]
          del_name.value = partner_name
//          del_phone.value = partner_phone
          del_addr.value = partner_addr
          del_city_name.value = partner_city
          del_zip_v.value =  partner_zip

    });
    })
