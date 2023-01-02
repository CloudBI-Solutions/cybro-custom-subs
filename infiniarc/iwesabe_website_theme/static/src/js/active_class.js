odoo.define('iwesabe_website_theme.active_class', function(require) {
    const ajax = require('web.ajax');
    $(document).on("click", "#response", function() {
    console.log("one", this)
//    console.log("addr", checkout_addr)
    var parent = $("#collapseOne")[0]
    var parentwo = $("#collapseTwo")[0]
    parent.classList.remove('show');
    parentwo.classList.add('show');


});

    $(document).on("click", "#v-pills-smsa-tab", function() {
        var price_input = $("#smsa_rate")[0]
        price_input.classList.remove('d-none');
        var smsa_addr = $("#street")[0].value
        var smsa_country = $(this)[0].value
        var smsa_city = $("#city_val")[0].value
        var smsa_zip = $("#zip_val")[0].value
        var street = $("#street_val")[0]
        var city = $("#city")[0]
        var zip = $("#zip")[0]
        street.value = smsa_addr
        city.value = smsa_city
        zip.value = smsa_zip
        return ajax.jsonRpc('/checkout/smsa', 'call', {
        }).then(function(result){
         console.log("resultttttt", result['smsa_cost'])
         console.log("price", price_input)
//          $("#summary").load(location.href + "#summary");
         price_input.value = result['smsa_cost']

     })

    });

//
//    $(document).on("change", "#country_val", function() {
//    console.log("add111111111", this)
//    var smsa_addr = $("#street")[0].value
//    var smsa_country = $(this)[0].value
//    var smsa_city = $("#city_val")[0].value
//    var smsa_zip = $("#zip_val")[0].value
//    var street = $("#street_val")[0]
//    var city = $("#city")[0]
//    var zip = $("#zip")[0]
//    street.value = smsa_addr
//    city.value = smsa_city
//    zip.value = smsa_zip
//    });

    $(document).on("click", "#response_two", function() {
        console.log("two", this)
        var parentwo = $("#collapseTwo")[0]
        var parenthree = $("#collapseThree")[0]
        parentwo.classList.remove('show');
        parenthree.classList.add('show');

        });



    });