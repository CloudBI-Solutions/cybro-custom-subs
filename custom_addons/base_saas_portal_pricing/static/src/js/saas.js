odoo.define('base_saas_portal_pricing.pricing',function(require){
    "use strict";
    var rpc = require('web.rpc');
    $(document).ready(function() {
        $(".card").click(function() {
            if (! $(this).children('input').prop( "checked")){
                $(this).children('input').prop( "checked", true );
                $(this).children('i').attr("aria-hidden", "false")
                $(this).css({"background-color": "#fafafa",
                    "box-shadow":"rgba(0, 0, 0, 0.25) 0px 4px 14px"})
                rpc.query({
                    model: 'saas.pricing',
                    method: 'get_depend_module',
                    args: [[$(this).children('input').val()]],
                }).then(function (result) {
                    console.log('res', result)
                    console.log($(this))
                });
            }
            else{
                $(this).children('input').prop( "checked", false );
                $(this).css({"box-shadow": "rgba(0, 0, 0, 0.1) 0px 4px 12px",
                    "background-color": "#FFFFFF"});
                $(this).children('i').attr("aria-hidden", "true");
            }
            var app_count = $('.form-check-input:checked').length;
            $('#apps_annual').val(app_count)
            $('#apps_monthly').val(app_count)
        });

        $("#users_count").change(function() {
            $('#users_annual').val($('#users_count').val());
            $('#users_monthly').val($('#users_count').val());
        });
    });
});
