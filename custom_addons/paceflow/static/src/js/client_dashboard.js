odoo.define('paceflow.client_dashboard', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');

    //To check if an inline style exists
    (function ($) {
      $.fn.inlineStyle = function (prop) {
        var styles = this.attr("style"),
          value;

        styles && styles.split(";").forEach(function (e) {
          var style = e.split(":");
          if ($.trim(style[0]) === prop) {
            value = style[1];
          }
        });
        return value;
      };
    }(jQuery));


    $(document).ready(function(){
        //To show expanded cards
        $(".db-card-toggler").click(function () {
            var target = $(this).attr("data-expand-id");
            //To close all expanded cards except the one that's clicked.
            $('.db-card-expand.show').not(`#${target}`).removeClass('show').addClass('hide');
            //To add remove margin padding from all the cards except the current one.
            //$('.db-card-toggler').not(this).removeClass('margin-bottom');
            $('.db-card-toggler').not(this).attr('style', '');
            //Toggle expanded card visibilty
            $(`#${target}`).toggleClass('hide show');
            //Adds bottom margin below the clicked card, so that the expanded card with absolute position can be properly displayed
            // $(this).toggleClass('margin-bottom');
            if ($(this).inlineStyle('margin-bottom')) {
              $(this).attr('style', '');
            } else {
               let targetHeight = $(`#${target}-card`).outerHeight();
               $(this).css({ marginBottom: `${targetHeight + 80}px` });
            }

          });
        //Shuffle Content
        $('.db-card-expand__shuffle').click(function (e) {
            //Prevent default link behavior on click
            e.preventDefault();
            //Get the target to be shuffled.
            var slideTarget = $(this).attr("data-slide-id");
            //Toggle display classes so that the currently displayed slide will be hidden and the hidden one is shown.
            $(`.${slideTarget}`).toggleClass('show hide');
          });
        var assessment_id = $("select[id='filter_selection']").val();
        if(assessment_id){
            ajax.jsonRpc('/get_dashboard_data', 'call',{'assessment_id': assessment_id})
            .then(function (result) {
            $('#div_legality_container').hide();
                var eL_red = document.getElementById("legality_red");
                var eL_yellow = document.getElementById("legality_yellow");
                var eL_green = document.getElementById("legality_green");
                eL_red.className = ''
                eL_yellow.className = ''
                eL_green.className = ''
                if(result.legality_score === 3){
                    eL_red.classList.add("circle");
                    eL_red.classList.add("red");
                    eL_yellow.classList.add("circle");
                    eL_green.classList.add("circle");
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 2){
                    eL_red.classList.add("circle");
                    eL_yellow.classList.add("circle");
                    eL_yellow.classList.add("yellow");
                    eL_green.classList.add("circle");
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 1){
                    eL_red.classList.add("circle");
                    eL_yellow.classList.add("circle");
                    eL_green.classList.add("circle");
                    eL_green.classList.add("green");
                    $('#div_legality_container').show();
                }
                $('#drills_tbody').empty();
                $('#notes_tbody').empty();
                $('#l_summary_drills_tbody1').empty();
                $('#m_summary_drills_tbody1').empty();
                $('#s_summary_drills_tbody1').empty();
                $('#p_summary_drills_tbody1').empty();
                $('#l_summary_notes_tbody1').empty();
                $('#m_summary_notes_tbody1').empty();
                $('#s_summary_notes_tbody1').empty();
                $('#p_summary_notes_tbody1').empty();
                $('#l_summary_drills_tbody2').empty();
                $('#m_summary_drills_tbody2').empty();
                $('#s_summary_drills_tbody2').empty();
                $('#p_summary_drills_tbody2').empty();
                $('#l_summary_notes_tbody2').empty();
                $('#m_summary_notes_tbody2').empty();
                $('#s_summary_notes_tbody2').empty();
                $('#p_summary_notes_tbody2').empty();
                $('#drills_notifier').empty();
                $('#notes_notifier').empty();
                $('#legality_drills_tbody').empty();
                $('#legality_notes_tbody').empty();
                $('#legality_drills_notifier').empty();
                $('#legality_notes_notifier').empty();
                $('#momentum_drills_tbody').empty();
                $('#momentum_notes_tbody').empty();
                $('#momentum_drills_notifier').empty();
                $('#momentum_notes_notifier').empty();
                $('#stability_drills_tbody1').empty();
                $('#stability_notes_tbody1').empty();
                $('#stability_drills_notifier1').empty();
                $('#stability_notes_notifier1').empty();
                $('#stability_drills_tbody2').empty();
                $('#stability_notes_tbody2').empty();
                $('#stability_drills_notifier2').empty();
                $('#stability_notes_notifier2').empty();
                $('#paceflow_drills_tbody1').empty();
                $('#paceflow_notes_tbody1').empty();
                $('#paceflow_drills_notifier1').empty();
                $('#paceflow_notes_notifier1').empty();
                $('#paceflow_drills_tbody2').empty();
                $('#paceflow_notes_tbody2').empty();
                $('#paceflow_drills_notifier2').empty();
                $('#paceflow_notes_notifier2').empty();
                $('#summary_drills_notifier1').empty();
                $('#summary_drills_notifier2').empty();
                $('#summary_notes_notifier1').empty();
                $('#summary_notes_notifier2').empty();
                $('#velocity').empty().append('<span>' + result.velocity + '</span>');
                $('#summary_summary_score').empty().append('<span>' + result.summary_summary_score + '</span>');
                $('#summary_legality_score').empty().append('<span>' + result.summary_legality_score + '</span>');
                $('#summary_momentum_score').empty().append('<span>' + result.summary_momentum_score + '</span>');
                $('#summary_stability_score').empty().append('<span>' + result.summary_stability_score + '</span>');
                $('#summary_paceflow_score').empty().append('<span>' + result.summary_paceflow_score + '</span>');
                $('#overall').empty().append('<h2 class="title-container__count blue-font"><span>' + result.overall_summary_score + '</span> %</h2>');
                if (result.rear_video){
                    $('#attachment1').empty().append('<video style="width: 100%; height: 300px" class="video-js vjs-default-skin" controls="" preload="none" data-setup="{ }"><source src="/web/image?model=assessment.assessment&amp;field=rear_video&amp;id=' + assessment_id + '" type="video/mp4"/><source src="/web/image?model=assessment.assessment&amp;field=rear_video&amp;id=' + assessment_id + '" type="video/ogg"/></video>');
                }
                else{
                    $('#attachment1').empty();
                }
                if (result.side_video){
                    $('#attachment2').empty().append('<video style="width: 100%; height: 300px" class="video-js vjs-default-skin" controls="" preload="none" data-setup="{ }"><source src="/web/image?model=assessment.assessment&amp;field=side_video&amp;id=' + assessment_id + '" type="video/mp4"/><source src="/web/image?model=assessment.assessment&amp;field=side_video&amp;id=' + assessment_id + '" type="video/ogg"/></video>');
                }
                else{
                    $('#attachment2').empty();
                }
                var summary_chart_ctx = document.getElementById("summary_summary").getContext('2d');
                var momentum_chart_ctx = document.getElementById("summary_momentum").getContext('2d');
                var stability_chart_ctx = document.getElementById("summary_stability").getContext('2d');
                var paceflow_chart_ctx = document.getElementById("summary_paceflow").getContext('2d');
                const summary_data = {
                      datasets: [{
                        data: [result.summary_summary_score, 100 - result.summary_summary_score],
                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var summary_chart = new Chart(summary_chart_ctx, {
                        type: "doughnut",
                        data: summary_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const momentum_data = {
                      datasets: [{
                        data: [result.summary_momentum_score, 100 - result.summary_momentum_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var momentum_chart = new Chart(momentum_chart_ctx, {
                        type: "doughnut",
                        data: momentum_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const stability_data = {
                      datasets: [{
                        data: [result.summary_stability_score, 100 - result.summary_stability_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var stability_chart = new Chart(stability_chart_ctx, {
                        type: "doughnut",
                        data: stability_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const paceflow_data = {
                      datasets: [{
                        data: [result.summary_paceflow_score, 100 - result.summary_paceflow_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var paceflow_chart = new Chart(paceflow_chart_ctx, {
                        type: "doughnut",
                        data: paceflow_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                    if(result.drills){
                        if(result.legality_drills){
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#l_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#l_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.momentum_drills){
                        for (var i=0; i<result.momentum_drills.length; i++){
                            $('#m_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.momentum_drills.length; i++){
                            $('#m_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.stability_drills){
                        for (var i=0; i<result.stability_drills.length; i++){
                            $('#s_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.stability_drills[i].slug + '">' + result.stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.stability_drills.length; i++){
                            $('#s_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.stability_drills[i].slug + '">' + result.stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.paceflow_drills){
                        for (var i=0; i<result.paceflow_drills.length; i++){
                            $('#p_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.paceflow_drills[i].slug + '">' + result.paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.paceflow_drills.length; i++){
                            $('#p_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.paceflow_drills[i].slug + '">' + result.paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        }
                    $('#div_summary_drills1').show();
                    $('#div_summary_drills2').show();
                    }
                    else{
                        $('#div_summary_drills1').hide();
                        $('#summary_drills_notifier1').empty().append('<div class="alert alert-warning mt8" role="alert">There are no rear summary drills for this assessment</div>');
                        $('#div_summary_drills2').hide();
                        $('#summary_drills_notifier2').empty().append('<div class="alert alert-warning mt8" role="alert">There are no summary drills for this assessment</div>');
                    }
                    if(result.notes){
                        if(result.legality_notes){
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#l_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#l_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.momentum_notes){
                        for (var i=0; i<result.momentum_notes.length; i++){
                            $('#m_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.momentum_notes.length; i++){
                            $('#m_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.stability_notes){
                        for (var i=0; i<result.stability_notes.length; i++){
                            $('#s_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.stability_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.stability_notes.length; i++){
                            $('#s_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.stability_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.paceflow_notes){
                        for (var i=0; i<result.paceflow_notes.length; i++){
                            $('#p_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.paceflow_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.paceflow_notes.length; i++){
                            $('#p_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.paceflow_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        $('#div_summary_notes1').show();
                        $('#div_summary_notes2').show();
                        }
                        else{
                            $('#div_summary_notes1').hide();
                            $('#summary_notes_notifier1').empty().append('<div class="alert alert-warning mt8" role="alert">There are no summary comments for this assessment</div>');
                            $('#div_summary_notes2').hide();
                            $('#summary_notes_notifier2').empty().append('<div class="alert alert-warning mt8" role="alert">There are no side stability comments for this assessment</div>');
                        }
                    if(result.legality_drills){
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#legality_drills_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.legality_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_legality_drills').show();
                        }
                        else{
                            $('#div_legality_drills').hide();
                            $('#legality_drills_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no legality drills for this assessment</div>');
                        }
                    if(result.momentum_drills){
                        for (var i=0; i<result.momentum_drills.length; i++){
                            $('#momentum_drills_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.momentum_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_momentum_drills').show();
                        }
                        else{
                            $('#div_momentum_drills').hide();
                            $('#momentum_drills_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no momentum drills for this assessment</div>');
                        }
                    if(result.rear_stability_drills){
                        for (var i=0; i<result.rear_stability_drills.length; i++){
                            $('#stability_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.rear_stability_drills[i].slug + '">' + result.rear_stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.rear_stability_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_stability_drills1').show();
                        }
                        else{
                            $('#div_stability_drills1').hide();
                            $('#stability_drills_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear stability drills for this assessment</div>');
                        }
                    if(result.side_stability_drills){
                        for (var i=0; i<result.side_stability_drills.length; i++){
                            $('#stability_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.side_stability_drills[i].slug + '">' + result.side_stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.side_stability_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_stability_drills2').show();
                        }
                        else{
                            $('#div_stability_drills2').hide();
                            $('#stability_drills_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side stability drills for this assessment</div>');
                        }
                    if(result.rear_paceflow_drills){
                        for (var i=0; i<result.rear_paceflow_drills.length; i++){
                            $('#paceflow_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.rear_paceflow_drills[i].slug + '">' + result.rear_paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.rear_paceflow_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_paceflow_drills1').show();
                        }
                        else{
                            $('#div_paceflow_drills1').hide();
                            $('#paceflow_drills_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear paceflow drills for this assessment</div>');
                        }
                    if(result.side_paceflow_drills){
                        for (var i=0; i<result.side_paceflow_drills.length; i++){
                            $('#paceflow_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.side_paceflow_drills[i].slug + '">' + result.side_paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.side_paceflow_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_paceflow_drills2').show();
                        }
                        else{
                            $('#div_paceflow_drills2').hide();
                             $('#paceflow_drills_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side paceflow drills for this assessment</div>');
                        }
                    if(result.legality_notes){
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#legality_notes_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_legality_notes').show();
                        }
                        else{
                            $('#div_legality_notes').hide();
                            $('#legality_notes_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no legality comments for this assessment</div>');
                        }
                    if(result.momentum_notes){
                        for (var i=0; i<result.momentum_notes.length; i++){
                            $('#momentum_notes_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_momentum_notes').show();
                        }
                        else{
                            $('#div_momentum_notes').hide();
                            $('#momentum_notes_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no momentum comments for this assessment</div>');
                        }
                    if(result.rear_stability_notes){
                        for (var i=0; i<result.rear_stability_notes.length; i++){
                            $('#stability_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.rear_stability_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_stability_notes1').show();
                        }
                        else{
                            $('#div_stability_notes1').hide();
                            $('#stability_notes_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear stability comments for this assessment</div>');
                        }
                    if(result.side_stability_notes){
                        for (var i=0; i<result.side_stability_notes.length; i++){
                            $('#stability_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.side_stability_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_stability_notes2').show();
                        }
                        else{
                            $('#div_stability_notes2').hide();
                            $('#stability_notes_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are side no stability comments for this assessment</div>');
                        }
                    if(result.rear_paceflow_notes){
                        for (var i=0; i<result.rear_paceflow_notes.length; i++){
                            $('#paceflow_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.rear_paceflow_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_paceflow_notes1').show();
                        }
                        else{
                            $('#div_paceflow_notes1').hide();
                            $('#paceflow_notes_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear paceflow comments for this assessment</div>');
                        }
                    if(result.side_paceflow_notes){
                        for (var i=0; i<result.side_paceflow_notes.length; i++){
                            $('#paceflow_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.side_paceflow_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_paceflow_notes2').show();
                        }
                        else{
                            $('#div_paceflow_notes2').hide();
                            $('#paceflow_notes_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side paceflow comments for this assessment</div>');
                        }
                    })
                }
        var child_id = $("select[id='child_id']").val();
        if(child_id){
        rpc.query({
            model: 'paceflow.child',
            method: 'get_dob',
            args: [child_id],
            })
            .then(function (result) {
                if (result){
                    $('#div_dob').empty().append('<input id="dob" type="text" class="form-control s_website_form_input" name="dob" readonly="" required="" value=' + result.dob + '></input>');

                }
            })
        }
    });

    publicWidget.registry.websiteUploadForm = publicWidget.Widget.extend({
        selector: '#submit_form',
        events: {
               'change #child_id': '_onChangeChild',
    },
     _onChangeChild: function (ev) {
        var child_id = $("select[id='child_id']").val();
        rpc.query({
            model: 'paceflow.child',
            method: 'get_dob',
            args: [child_id],
            })
            .then(function (result) {
                $('#div_dob').empty().append('<input id="dob" type="text" class="form-control s_website_form_input" name="dob" readonly="" required="" value=' + result.dob + '></input>');

            })
     },

    });

    publicWidget.registry.websiteClientDashboardAssessments = publicWidget.Widget.extend({
        selector: '#filter',
        events: {
               //tile filter
               'change #date_from': '_onChangeDateFilter',
               'change #date_to': '_onChangeDateFilter',
               'change #filter_selection': '_onChangeFilter',
               'click #clear_dates': '_onClickClear',
    },
    _onClickClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='child_id']").val();
         $("input[id='date_from']").val(null);
         $("input[id='date_to']").val(null);
         ajax.jsonRpc('/get_filter_clear_data', 'call',{'child_id': child_id})
                .then(function (result) {
                    $('#filter_selection option').remove();
                    for (var i=0; i<result.length; i++){
            $('#filter_selection').append($('<option>',
                 {
                    value: result[i].id,
                    text : result[i].name
                 }));
                 }
                 self._onChangeFilter(ev)
                });
         },
    _onChangeDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='child_id']").val();
         var date_from = $("input[id='date_from']").val();
         var date_to = $("input[id='date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    $('#filter_selection option').remove();
                    for (var i=0; i<result.length; i++){
                        $('#filter_selection').append($('<option>',
                         {
                            value: result[i].id,
                            text : result[i].name
                         }));
                         }
                    self._onChangeFilter(ev)
                });
         }
         },
    _onChangeFilter: function (ev) {
         ev.preventDefault();
         console.log("_onChangeFilter")
         var assessment_id = $("select[id='filter_selection']").val();
         if (assessment_id){
            ajax.jsonRpc('/get_dashboard_data', 'call',{'assessment_id': assessment_id})
            .then(function (result) {
                $('#div_legality_container').hide();
                var eL_red = document.getElementById("legality_red");
                var eL_yellow = document.getElementById("legality_yellow");
                var eL_green = document.getElementById("legality_green");
                eL_red.className = ''
                eL_yellow.className = ''
                eL_green.className = ''
                if(result.legality_score === 3){
//                    $('#legality_selection').empty().append('<h5><span class="badge badge-danger">Red</span></h5>');
                    eL_red.classList.add("circle");
                    eL_red.classList.add("red");
                    eL_yellow.classList.add("circle");
                    eL_green.classList.add("circle");
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 2){
//                    $('#legality_selection').empty().append('<h5><span class="badge badge-warning">Amber</span></h5>');
                    eL_red.classList.add("circle");
                    eL_yellow.classList.add("circle");
                    eL_yellow.classList.add("yellow");
                    eL_green.classList.add("circle");
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 1){
//                    $('#legality_selection').empty().append('<h5><span class="badge badge-success">Green</span></h5>');
                    eL_red.classList.add("circle");
                    eL_yellow.classList.add("circle");
                    eL_green.classList.add("circle");
                    eL_green.classList.add("green");
                    $('#div_legality_container').show();
                }
                $('#drills_tbody').empty();
                $('#notes_tbody').empty();
                $('#drills tbody').empty();
                $('#notes tbody').empty();
                $('#drills_notifier').empty();
                $('#notes_notifier').empty();
                $('#legality_drills_tbody').empty();
                $('#legality_notes_tbody').empty();
                $('#legality_drills_notifier').empty();
                $('#legality_notes_notifier').empty();
                $('#momentum_drills_tbody').empty();
                $('#momentum_notes_tbody').empty();
                $('#momentum_drills_notifier').empty();
                $('#momentum_notes_notifier').empty();
                $('#stability_drills_tbody1').empty();
                $('#stability_notes_tbody1').empty();
                $('#summary_drills_notifier1').empty();
                $('#summary_drills_notifier2').empty();
                $('#stability_drills_notifier1').empty();
                $('#stability_notes_notifier1').empty();
                $('#stability_drills_tbody2').empty();
                $('#stability_notes_tbody2').empty();
                $('#stability_drills_notifier2').empty();
                $('#stability_notes_notifier2').empty();
                $('#paceflow_drills_tbody1').empty();
                $('#paceflow_notes_tbody1').empty();
                $('#paceflow_drills_notifier1').empty();
                $('#paceflow_notes_notifier1').empty();
                $('#paceflow_drills_tbody2').empty();
                $('#paceflow_notes_tbody2').empty();
                $('#paceflow_drills_notifier2').empty();
                $('#paceflow_notes_notifier2').empty();
                $('#img_summary1').empty();
                $('#img_summary2').empty();
                $('#img_legality').empty();
                $('#img_momentum').empty();
                $('#img_stability1').empty();
                $('#img_stability2').empty();
                $('#img_paceflow1').empty();
                $('#img_paceflow2').empty();
                $('#summary_notes_notifier1').empty();
                $('#summary_notes_notifier2').empty();
                console.log(result.img_summary_overall_1)
                if(result.img_summary_overall_1){
                    $('#img_summary1').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_summary_overall_1" alt="Summary/>');
                }
                if(result.img_summary_overall_2){
                    $('#img_summary2').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_summary_overall_2" alt="Summary/>');
                }
                if(result.img_legality_overall){
                    $('#img_legality').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_legality_overall" alt="Legality"/>');
                }
                if(result.img_momentum_overall){
                    $('#img_momentum').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_momentum_overall" alt="Momentum/>');
                }
                if(result.img_stability_overall_1){
                    $('#img_stability1').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_stability_overall_1" alt="Stability/>');
                }
                if(result.img_stability_overall_2){
                    $('#img_stability2').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_stability_overall_2" alt="Stability/>');
                }
                if(result.img_paceflow_overall_1){
                    $('#img_paceflow1').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_paceflow_overall_1" alt="Paceflow/>');
                }
                if(result.img_paceflow_overall_2){
                    $('#img_paceflow2').append('<img class="db-card-expand__image" src="/web/image/assessment.assessment/' + assessment_id + '/img_paceflow_overall_2" alt="Paceflow/>');
                }
                if(result.drills){
                    if(result.legality_drills){
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#l_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#l_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.momentum_drills){
                        for (var i=0; i<result.momentum_drills.length; i++){
                            $('#m_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.momentum_drills.length; i++){
                            $('#m_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.stability_drills){
                        for (var i=0; i<result.stability_drills.length; i++){
                            $('#s_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.stability_drills[i].slug + '">' + result.stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.stability_drills.length; i++){
                            $('#s_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.stability_drills[i].slug + '">' + result.stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                    }
                    if(result.paceflow_drills){
                        for (var i=0; i<result.paceflow_drills.length; i++){
                            $('#p_summary_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.paceflow_drills[i].slug + '">' + result.paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        for (var i=0; i<result.paceflow_drills.length; i++){
                            $('#p_summary_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.paceflow_drills[i].slug + '">' + result.paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.drills[i].slide_type + '</span></div></div>');
                            }
                        }
                    $('#div_summary_drills1').show();
                    $('#div_summary_drills2').show();
                    }
                    else{
                        $('#div_summary_drills1').hide();
                        $('#summary_drills_notifier1').empty().append('<div class="alert alert-warning mt8" role="alert">There are no rear summary drills for this assessment</div>');
                        $('#div_summary_drills2').hide();
                        $('#summary_drills_notifier2').empty().append('<div class="alert alert-warning mt8" role="alert">There are no summary drills for this assessment</div>');
                    }
                    if(result.notes){
                        if(result.legality_notes){
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#l_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#l_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.momentum_notes){
                        for (var i=0; i<result.momentum_notes.length; i++){
                            $('#m_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.momentum_notes.length; i++){
                            $('#m_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.stability_notes){
                        for (var i=0; i<result.stability_notes.length; i++){
                            $('#s_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.stability_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.stability_notes.length; i++){
                            $('#s_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.stability_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        if(result.paceflow_notes){
                        for (var i=0; i<result.paceflow_notes.length; i++){
                            $('#p_summary_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.paceflow_notes[i].description + '</span></div></div>');
                            }
                        for (var i=0; i<result.paceflow_notes.length; i++){
                            $('#p_summary_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.paceflow_notes[i].description + '</span></div></div></div>');
                            }
                        }
                        $('#div_summary_notes1').show();
                        $('#div_summary_notes2').show();
                        }
                        else{
                            $('#div_summary_notes1').hide();
                            $('#summary_notes_notifier1').empty().append('<div class="alert alert-warning mt8" role="alert">There are no summary comments for this assessment</div>');
                            $('#div_summary_notes2').hide();
                            $('#summary_notes_notifier2').empty().append('<div class="alert alert-warning mt8" role="alert">There are no side stability comments for this assessment</div>');
                        }
                if(result.legality_drills){
                        for (var i=0; i<result.legality_drills.length; i++){
                            $('#legality_drills_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.legality_drills[i].slug + '">' + result.legality_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.legality_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_legality_drills').show();
                        }
                        else{
                            $('#div_legality_drills').hide();
                            $('#legality_drills_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no legality drills for this assessment</div>');
                        }
                if(result.momentum_drills){
                    for (var i=0; i<result.momentum_drills.length; i++){
                        $('#momentum_drills_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.momentum_drills[i].slug + '">' + result.momentum_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.momentum_drills[i].slide_type + '</span></div></div>');
                        }
                        $('#div_momentum_drills').show();
                    }
                    else{
                        $('#div_momentum_drills').hide();
                        $('#momentum_drills_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no momentum drills for this assessment</div>');
                    }
                if(result.rear_stability_drills){
                        for (var i=0; i<result.rear_stability_drills.length; i++){
                            $('#stability_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.rear_stability_drills[i].slug + '">' + result.rear_stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.rear_stability_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_stability_drills1').show();
                        }
                        else{
                            $('#div_stability_drills1').hide();
                            $('#stability_drills_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear stability drills for this assessment</div>');
                        }
                    if(result.side_stability_drills){
                        for (var i=0; i<result.side_stability_drills.length; i++){
                            $('#stability_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.side_stability_drills[i].slug + '">' + result.side_stability_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.side_stability_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_stability_drills2').show();
                        }
                        else{
                            $('#div_stability_drills2').hide();
                            $('#stability_drills_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side stability drills for this assessment</div>');
                        }
                if(result.rear_paceflow_drills){
                        for (var i=0; i<result.rear_paceflow_drills.length; i++){
                            $('#paceflow_drills_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.rear_paceflow_drills[i].slug + '">' + result.rear_paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.rear_paceflow_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_paceflow_drills1').show();
                        }
                        else{
                            $('#div_paceflow_drills1').hide();
                            $('#paceflow_drills_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear paceflow drills for this assessment</div>');
                        }
                    if(result.side_paceflow_drills){
                        for (var i=0; i<result.side_paceflow_drills.length; i++){
                            $('#paceflow_drills_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><a class="o_wslides_js_slides_list_slide_link" href="/slides/slide/' + result.side_paceflow_drills[i].slug + '">' + result.side_paceflow_drills[i].name + '</a></div></div><div class="db-tutorial-item__kind"><span class="badge badge-info"><span>' + result.side_paceflow_drills[i].slide_type + '</span></div></div>');
                            }
                            $('#div_paceflow_drills2').show();
                        }
                        else{
                            $('#div_paceflow_drills2').hide();
                             $('#paceflow_drills_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side paceflow drills for this assessment</div>');
                        }
                if(result.legality_notes){
                        for (var i=0; i<result.legality_notes.length; i++){
                            $('#legality_notes_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.legality_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_legality_notes').show();
                        }
                        else{
                            $('#div_legality_notes').hide();
                            $('#legality_notes_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no legality comments for this assessment</div>');
                        }
                if(result.momentum_notes){
                    for (var i=0; i<result.momentum_notes.length; i++){
                        $('#momentum_notes_tbody').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.momentum_notes[i].description + '</span></div></div></div>');
                        }
                        $('#div_momentum_notes').show();
                    }
                    else{
                        $('#div_momentum_notes').hide();
                        $('#momentum_notes_notifier').append('<div class="alert alert-warning mt8" role="alert">There are no momentum comments for this assessment</div>');
                    }
                if(result.rear_stability_notes){
                        for (var i=0; i<result.rear_stability_notes.length; i++){
                            $('#stability_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.rear_stability_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_stability_notes1').show();
                        }
                        else{
                            $('#div_stability_notes1').hide();
                            $('#stability_notes_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear stability comments for this assessment</div>');
                        }
                    if(result.side_stability_notes){
                        for (var i=0; i<result.side_stability_notes.length; i++){
                            $('#stability_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.side_stability_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_stability_notes2').show();
                        }
                        else{
                            $('#div_stability_notes2').hide();
                            $('#stability_notes_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are side no stability comments for this assessment</div>');
                        }
                if(result.rear_paceflow_notes){
                        for (var i=0; i<result.rear_paceflow_notes.length; i++){
                            $('#paceflow_notes_tbody1').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.rear_paceflow_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_paceflow_notes1').show();
                        }
                        else{
                            $('#div_paceflow_notes1').hide();
                            $('#paceflow_notes_notifier1').append('<div class="alert alert-warning mt8" role="alert">There are no rear paceflow comments for this assessment</div>');
                        }
                    if(result.side_paceflow_notes){
                        for (var i=0; i<result.side_paceflow_notes.length; i++){
                            $('#paceflow_notes_tbody2').append('<div class="db-tutorial-item"><div class="db-tutorial-item__info"><div class="db-tutorial-item__name"><span>' + result.side_paceflow_notes[i].description + '</span></div></div></div>');
                            }
                            $('#div_paceflow_notes2').show();
                        }
                        else{
                            $('#div_paceflow_notes2').hide();
                            $('#paceflow_notes_notifier2').append('<div class="alert alert-warning mt8" role="alert">There are no side paceflow comments for this assessment</div>');
                        }
                $('#velocity').empty().append('<span>' + result.velocity + '</span>');
                $('#summary_summary_score').empty().append('<span>' + result.summary_summary_score + '</span>');
                $('#summary_legality_score').empty().append('<span>' + result.summary_legality_score + '</span>');
                $('#summary_momentum_score').empty().append('<span>' + result.summary_momentum_score + '</span>');
                $('#summary_stability_score').empty().append('<span>' + result.summary_stability_score + '</span>');
                $('#summary_paceflow_score').empty().append('<span>' + result.summary_paceflow_score + '</span>');
                $('#overall').empty().append('<h2 class="title-container__count blue-font"><span>' + result.overall_summary_score + '</span> %</h2>');
                var summary_chart_ctx = document.getElementById("summary_summary").getContext('2d');
                var momentum_chart_ctx = document.getElementById("summary_momentum").getContext('2d');
                var stability_chart_ctx = document.getElementById("summary_stability").getContext('2d');
                var paceflow_chart_ctx = document.getElementById("summary_paceflow").getContext('2d');
                const summary_data = {
                      datasets: [{
                        data: [result.summary_summary_score, 100 - result.summary_summary_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var summary_chart = new Chart(summary_chart_ctx, {
                        type: "doughnut",
                        data: summary_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const momentum_data = {
                      datasets: [{
                        data: [result.summary_momentum_score, 100 - result.summary_momentum_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var momentum_chart = new Chart(momentum_chart_ctx, {
                        type: "doughnut",
                        data: momentum_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const stability_data = {
                      datasets: [{
                        data: [result.summary_stability_score, 100 - result.summary_stability_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var stability_chart = new Chart(stability_chart_ctx, {
                        type: "doughnut",
                        data: stability_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                const paceflow_data = {
                      datasets: [{
                        data: [result.summary_paceflow_score, 100 - result.summary_paceflow_score],

                        backgroundColor: [
                            '#B80062',
                            'rgb(211,211,211)'
                        ],
                        hoverOffset: 4
                      }]
                    };
                    var paceflow_chart = new Chart(paceflow_chart_ctx, {
                        type: "doughnut",
                        data: paceflow_data,
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            rotation : Math.PI,
                        },
                    });
                if (result.rear_video){
                    $('#attachment1').empty().append('<video style="width: 100%; height: 300px" class="video-js vjs-default-skin" controls="" preload="none" data-setup="{ }"><source src="/web/image?model=assessment.assessment&amp;field=rear_video&amp;id=' + assessment_id + '" type="video/mp4"/><source src="/web/image?model=assessment.assessment&amp;field=rear_video&amp;id=' + assessment_id + '" type="video/ogg"/></video>');
                }
                else{
                    $('#attachment1').empty();
                }
                if (result.side_video){
                    $('#attachment2').empty().append('<video style="width: 100%; height: 300px" class="video-js vjs-default-skin" controls="" preload="none" data-setup="{ }"><source src="/web/image?model=assessment.assessment&amp;field=side_video&amp;id=' + assessment_id + '" type="video/mp4"/><source src="/web/image?model=assessment.assessment&amp;field=side_video&amp;id=' + assessment_id + '" type="video/ogg"/></video>');
                }
                else{
                    $('#attachment2').empty();
                }
            })}
    },
    });

});