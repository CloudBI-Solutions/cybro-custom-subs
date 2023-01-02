odoo.define('paceflow.videoRecord',function(require){
    "use strict";

//DEFAULT DATE

    $(document).ready(function () {
        if (document.getElementById('date_1')){
            document.getElementById('date_1').valueAsDate = new Date();
            }
        if (document.getElementById('date_2')){
            document.getElementById('date_2').valueAsDate = new Date();
            }
    });
});
