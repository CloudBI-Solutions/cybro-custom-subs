odoo.define('survey_extension.survey_cust', function (require) {
'use strict';
    var ajax = require('web.ajax');
    $(document).on('change','.slider_bar',function(){
        console.log("this", $(this).val())
        $(this).prop('title', $(this).val())
    })
//    $(".slider_bar").on('change',function(){
//        console.log(">>>>>>>>>>>>>>>>>>>>",$(this))
//        $(this).prop('title', $(this).val())
//    });


//    $(document).on('change','#togBtn',function(){
////    $("#togBtn").on('change',function(){
//        if($(this).is(":checked")){
//            $('.on_class').removeClass('d-none');
//            $('.off_class').addClass('d-none');
//        }else{
//            $('.off_class').removeClass('d-none');
//            $('.on_class').addClass('d-none');
//        }
//            $(this).prop('checked', $(this).is(":checked"));
//        });


    })
//    $(".o_survey_form .form-control").on("change", function(){
//        var question_id = $(this).prop('name');
//        ajax.jsonRpc("/survey/used_in_computation", 'call', {
//            'question_id': question_id,
//        }).then(function (result) {
//        });
//    })
