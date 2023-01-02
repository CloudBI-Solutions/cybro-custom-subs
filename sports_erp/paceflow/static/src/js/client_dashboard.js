odoo.define('paceflow.client_dashboard', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var summary_chart = null;
    var momentum_chart = null;
    var stability_chart = null;
    var paceflow_chart = null;



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
        var assessment_id = $("select[id='filter_selection']").val();
        if(assessment_id){
            ajax.jsonRpc('/get_dashboard_data', 'call',{'assessment_id': assessment_id})
            .then(function (result) {
            $('#div_legality_container').hide();
            var legality_elt = document.getElementById("legality_light");

            legality_elt.className = '';

                if(result.legality_score === 100){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--red')
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 66){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--yellow');
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 33){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--green');
                    $('#div_legality_container').show();
                }
                $('#velocity').empty().append('<span>' + result.velocity + '</span>');
                $('#summary_summary_score').empty().append('<span>' + result.summary_summary_score + '</span>');
                $('#summary_momentum_score').empty().append('<span>' + result.summary_momentum_score + '</span>');
                $('#summary_stability_score').empty().append('<span>' + result.summary_stability_score + '</span>');
                $('#summary_paceflow_score').empty().append('<span>' + result.summary_paceflow_score + '</span>');
                $('#overall').empty().append('<h2 class="title-container__count blue-font"><span>' + result.overall_summary_score + '</span> %</h2>');

//            CAROUSEL

                $('#img_summary_overall_1').empty();
                $('#img_summary_overall_2').empty();
                if (result.img_summary_overall_1) {
                    $('#img_summary_overall_1').attr('src', 'data:image/png;base64, '+result.img_summary_overall_1);
                }
                else{
                    $('#img_summary_overall_1').attr('src', '/paceflow/static/description/images/ui/image-thumbnail.png');
                }
                if (result.img_summary_overall_2) {
                    $('#img_summary_overall_2').attr('src', 'data:image/png;base64, '+result.img_summary_overall_2);
                }
                else{
                    $('#img_summary_overall_2').attr('src', '/paceflow/static/description/images/ui/image-thumbnail.png');
                }

//                LEGALITY COMMENTS
                $('#legality_comments').empty();
                if(result.legality_notes){
                    for (var i=0; i<result.legality_notes.length; i++){
                        $('#legality_comments').append('<li class="paceflow-comment"><strong>' + result.legality_notes[i].name + '</strong>' + result.legality_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#legality_comments').append('There are no legality comments for this assessment');
                }
//                MOMENTUM COMMENTS
                $('#momentum_comments').empty();
                if(result.momentum_notes){
                    for (var i=0; i<result.momentum_notes.length; i++){
                        $('#momentum_comments').append('<li class="paceflow-comment"><strong>' + result.momentum_notes[i].name + '</strong>' + result.momentum_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#momentum_comments').append('There are no momentum comments for this assessment');
                }

//                STABILITY COMMENTS
                $('#stability_comments').empty();
                if(result.stability_notes){
                    for (var i=0; i<result.momentum_notes.length; i++){
                        $('#stability_comments').append('<li class="paceflow-comment"><strong>' + result.stability_notes[i].name + '</strong>' + result.stability_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#stability_comments').append('There are no stability comments for this assessment');
                }

//                PACEFLOW COMMENTS

                $('#paceflow_comments').empty();
                if(result.paceflow_notes){
                    for (var i=0; i<result.paceflow_notes.length; i++){
                        $('#paceflow_comments').append('<li class="paceflow-comment"><strong>' + result.paceflow_notes[i].name + '</strong>' + result.paceflow_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#paceflow_comments').append('There are no paceflow comments for this assessment');
                }

//              VIDEO CAROUSEL - LEGALITY

                $('#video_carousel_legality').empty();
                if(result.legality_drills){
                    var video = [];
                    var div_id = 0;
                    for(var i=0; i<result.legality_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_legality').append('<div id="legality_div_'+div_id+'" class="carousel-item"><div id="legality_row_'+div_id+'" class="row"/></div>');
                            video = [result.legality_drills[i], result.legality_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.legality_drills[i]['name'];
                                if (result.legality_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.legality_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                    vid_1 = result.legality_drills[i]['url'];
                                }
                                var id_1 = 'legality_0div'+div_id;
                                $('#legality_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.legality_drills[i].slug+'">'+result.legality_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = ''
                                var title = result.legality_drills[i+1]['name'];
                                if (result.legality_drills[i+1]['url'].includes('watch?v=')) {
                                    var vid_2 = result.legality_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                    vid_2 = result.legality_drills[i+1]['url'];
                                }
                                var id_2 = 'legality_1div'+div_id;
                                $('#legality_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.legality_drills[i+1].slug+'">'+result.legality_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('legality_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_legality').show();
                        $('#next_button_legality').show();
                    }
                else{
                        $('#video_carousel_legality').append('<span class="paceflow-comment ml-5">No Legality Drills for this assessment. </span>');
                        $('#prev_button_legality').hide();
                        $('#next_button_legality').hide();
                    }

//                MOMENTUM DRILLS VIDEO CAROUSEL

                $('#video_carousel_momentum').empty();
                if(result.momentum_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.momentum_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_momentum').append('<div id="momentum_div_'+div_id+'" class="carousel-item"><div id="momentum_row_'+div_id+'" class="row"/></div>');
                            video = [result.momentum_drills[i], result.momentum_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.momentum_drills[i]['name'];
                                if (result.momentum_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.momentum_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.momentum_drills[i]['url'];
                                }
                                var id_1 = 'momentum_0div'+div_id;
                                $('#momentum_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.momentum_drills[i].slug+'">'+result.momentum_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.momentum_drills[i+1]['name'];
                                if (result.momentum_drills[i+1]['url'].includes('watch?v=')) {
                                    vid_2 = result.momentum_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_2 = result.momentum_drills[i+1]['url'];
                                }
                                var id_2 = 'momentum_1div'+div_id;
                                $('#momentum_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.momentum_drills[i+1].slug+'">'+result.momentum_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('momentum_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_momentum').show();
                        $('#next_button_momentum').show();
                    }
                else{
                        $('#video_carousel_momentum').append('<span class="paceflow-comment ml-5">No Momentum Drills for this assessment. </span>');
                        $('#prev_button_momentum').hide();
                        $('#next_button_momentum').hide();
                    }

//                    Stability Drills VIDEO CAROUSEL

                $('#video_carousel_stability').empty();
                if(result.stability_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.stability_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_stability').append('<div id="stability_div_'+div_id+'" class="carousel-item"><div id="stability_row_'+div_id+'" class="row"/></div>');
                            video = [result.stability_drills[i], result.stability_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.stability_drills[i]['name'];
                                if (result.stability_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.stability_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.stability_drills[i]['url'];
                                }
                                var id_1 = 'stability_0div'+div_id;
                                $('#stability_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.stability_drills[i].slug+'">'+result.stability_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.stability_drills[i+1]['name'];
                                if (result.stability_drills[i+1]['url'].includes('watch?v=')) {
                                    vid_2 = result.stability_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_2 = result.stability_drills[i+1]['url'];
                                }
                                var id_2 = 'stability_1div'+div_id;
                                $('#stability_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.stability_drills[i+1].slug+'">'+result.stability_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('stability_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_stability').show();
                        $('#next_button_stability').show();
                    }
                else{
                        $('#video_carousel_stability').append('<span class="paceflow-comment ml-5">No Stability Drills for this assessment. </span>');
                        $('#prev_button_stability').hide();
                        $('#next_button_stability').hide();
                    }

//                  PACEFLOW DRILLS VIDEO CAROUSEL

                $('#video_carousel_paceflow').empty();
                if(result.paceflow_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.paceflow_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_paceflow').append('<div id="paceflow_div_'+div_id+'" class="carousel-item"><div id="paceflow_row_'+div_id+'" class="row"/></div>');
                            video = [result.paceflow_drills[i], result.paceflow_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.paceflow_drills[i]['name'];
                                if (result.paceflow_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.paceflow_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.paceflow_drills[i]['url'];
                                }
                                var id_1 = 'paceflow_0div'+div_id;
                                $('#paceflow_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.paceflow_drills[i].slug+'">'+result.paceflow_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.paceflow_drills[i+1]['name']
                                if (result.paceflow_drills[i+1]['url'].includes('watch?v=')) {
                                    vid_2 = result.paceflow_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_2 = result.paceflow_drills[i+1]['url'];
                                }
                                var id_2 = 'paceflow_1div'+div_id;
                                $('#paceflow_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.paceflow_drills[i+1].slug+'">'+result.paceflow_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('paceflow_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_paceflow').show();
                        $('#next_button_paceflow').show();
                    }
                else{
                        $('#video_carousel_paceflow').append('<span class="paceflow-comment ml-5">No Paceflow Drills for this assessment. </span>');
                        $('#prev_button_paceflow').hide();
                        $('#next_button_paceflow').hide();
                    }

//              CHARTS

                var summary_chart_ctx = document.getElementById("summary_summary").getContext('2d');
                var momentum_chart_ctx = document.getElementById("summary_momentum").getContext('2d');
                var stability_chart_ctx = document.getElementById("summary_stability").getContext('2d');
                var paceflow_chart_ctx = document.getElementById("summary_paceflow").getContext('2d');
                const summary_data = {
                      datasets: [{
                        data: [result.summary_summary_score, 100 - result.summary_summary_score],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    summary_chart = new Chart(summary_chart_ctx, {
                        type: "doughnut",
                        data: summary_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                 enabled: false,
                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });
                const momentum_data = {
                      datasets: [{
                        data: [result.summary_momentum_score, 100 - result.summary_momentum_score],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    momentum_chart = new Chart(momentum_chart_ctx, {
                        type: "doughnut",
                        data: momentum_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                    enabled: false,

                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });

                const stability_data = {
                      datasets: [{
                        data: [result.summary_stability_score, 100 - result.summary_stability_score],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    stability_chart = new Chart(stability_chart_ctx, {
                        type: "doughnut",
                        data: stability_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                    enabled: false,
                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });

                const paceflow_data = {
                      datasets: [{
                        data: [result.summary_paceflow_score, 100 - result.summary_paceflow_score],

                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    paceflow_chart = new Chart(paceflow_chart_ctx, {
                        type: "doughnut",
                        data: paceflow_data,
                        options: {
                            hover: {
                                mode: null
                            },

                                tooltips: {
                                    enabled: false,

                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });
                });
            }
        });


        publicWidget.registry.websiteClientDashboardAssessments = publicWidget.Widget.extend({
        selector: '#filter',
        events: {
               //tile filter
               'change #filter_selection': '_onChangeFilter',
        },

        _onChangeFilter: function (ev) {
         ev.preventDefault();
         var assessment_id = $("select[id='filter_selection']").val();
         if (assessment_id) {
            ajax.jsonRpc('/get_dashboard_data', 'call',{'assessment_id': assessment_id})
            .then(function (result) {

                $('#div_legality_container').hide();
                var legality_elt = document.getElementById("legality_light");

                legality_elt.className = '';

                if(result.legality_score === 100){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--red')
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 66){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--yellow');
                    $('#div_legality_container').show();
                }
                if(result.legality_score === 33){
                    legality_elt.classList.add(
                    'paceflow-card-item__dot',
                    'paceflow-card-item__dot--square',
                    'paceflow-shadow',
                    'paceflow-card-item__dot--green');
                    $('#div_legality_container').show();
                }

                $('#velocity').empty().append('<span>' + result.velocity + '</span>');
                $('#summary_summary_score').empty().append('<span>' + result.summary_summary_score + '</span>');
                $('#summary_legality_score').empty().append('<span>' + result.summary_legality_score + '</span>');
                $('#summary_momentum_score').empty().append('<span>' + result.summary_momentum_score + '</span>');
                $('#summary_stability_score').empty().append('<span>' + result.summary_stability_score + '</span>');
                $('#summary_paceflow_score').empty().append('<span>' + result.summary_paceflow_score + '</span>');
                $('#overall').empty().append('<h2 class="title-container__count blue-font"><span>' + result.overall_summary_score + '</span> %</h2>');

//            CAROUSEL
                $('#img_summary_overall_1').empty();
                $('#img_summary_overall_2').empty();
                if (result.img_summary_overall_1) {
                    $('#img_summary_overall_1').attr('src', 'data:image/png;base64, '+result.img_summary_overall_1);
                }
                else{
                    $('#img_summary_overall_1').attr('src', '/paceflow/static/description/images/ui/image-thumbnail.png');
                }
                if (result.img_summary_overall_2) {
                    $('#img_summary_overall_2').attr('src', 'data:image/png;base64, '+result.img_summary_overall_2);
                }
                else{
                    $('#img_summary_overall_2').attr('src', '/paceflow/static/description/images/ui/image-thumbnail.png');
                }

//                VIDEO CAROUSEL - LEGALITY

                $('#video_carousel_legality').empty();
                if(result.legality_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.legality_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_legality').append('<div id="legality_div_'+div_id+'" class="carousel-item"><div id="legality_row_'+div_id+'" class="row"/></div>');
                            video = [result.legality_drills[i], result.legality_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.legality_drills[i]['name'];
                                if (result.legality_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.legality_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                    vid_1 = result.legality_drills[i]['url'];
                                }
                                var id_1 = 'legality_0div'+div_id;
                                $('#legality_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.legality_drills[i].slug+'">'+result.legality_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = ''
                                var title = result.legality_drills[i+1]['name'];
                                if (result.legality_drills[i+1]['url'].includes('watch?v=')) {
                                    var vid_2 = result.legality_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                    vid_2 = result.legality_drills[i+1]['url'];
                                }
                                var id_2 = 'legality_1div'+div_id;
                                $('#legality_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.legality_drills[i+1].slug+'">'+result.legality_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('legality_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_legality').show();
                        $('#next_button_legality').show();
                    }
                else{
                        $('#video_carousel_legality').append('<span class="paceflow-comment ml-5">No Legality Drills for this assessment. </span>');
                        $('#prev_button_legality').hide();
                        $('#next_button_legality').hide();
                    }

//                MOMENTUM DRILLS VIDEO CAROUSEL

                $('#video_carousel_momentum').empty();
                if(result.momentum_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.momentum_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_momentum').append('<div id="momentum_div_'+div_id+'" class="carousel-item"><div id="momentum_row_'+div_id+'" class="row"/></div>');
                            video = [result.momentum_drills[i], result.momentum_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.momentum_drills[i]['name'];
                                if (result.momentum_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.momentum_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.momentum_drills[i]['url'];
                                }
                                var id_1 = 'momentum_0div'+div_id;
                                $('#momentum_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.momentum_drills[i].slug+'">'+result.momentum_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.momentum_drills[i+1]['name'];
                                var vid_2 = result.momentum_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                var id_2 = 'momentum_1div'+div_id;
                                $('#momentum_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.momentum_drills[i+1].slug+'">'+result.momentum_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('momentum_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_momentum').show();
                        $('#next_button_momentum').show();
                    }
                else{
                        $('#video_carousel_momentum').append('<span class="paceflow-comment ml-5">No Momentum Drills for this assessment. </span>');
                        $('#prev_button_momentum').hide();
                        $('#next_button_momentum').hide();
                    }

//                    Stability Drills VIDEO CAROUSEL

                $('#video_carousel_stability').empty();
                if(result.stability_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.stability_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_stability').append('<div id="stability_div_'+div_id+'" class="carousel-item"><div id="stability_row_'+div_id+'" class="row"/></div>');
                            video = [result.stability_drills[i], result.stability_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.stability_drills[i]['name'];
                                if (result.stability_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.stability_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.stability_drills[i]['url'];
                                }
                                var id_1 = 'stability_0div'+div_id;
                                $('#stability_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.stability_drills[i].slug+'">'+result.stability_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.stability[i+1]['name'];
                                if (result.stability_drills[i+1]['url'].includes('watch?v=')) {
                                    vid_2 = result.stability_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else{
                                    vid_2 = result.stability_drills[i+1]['url'];
                                }
                                var id_2 = 'stability_1div'+div_id;
                                $('#stability_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.stability_drills[i+1].slug+'">'+result.stability_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('stability_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_stability').show();
                        $('#next_button_stability').show();
                    }
                else{
                        $('#video_carousel_stability').append('<span class="paceflow-comment ml-5">No Stability Drills for this assessment. </span>');
                        $('#prev_button_stability').hide();
                        $('#next_button_stability').hide();
                    }

//                  PACEFLOW DRILLS VIDEO CAROUSEL

                $('#video_carousel_paceflow').empty();
                if(result.paceflow_drills){
                    var video = [];
                    var div_id = 0;
                    for(i=0; i<result.paceflow_drills.length; i++){
                        if(i % 2 == 0){
                            div_id += 1;
                            $('#video_carousel_paceflow').append('<div id="paceflow_div_'+div_id+'" class="carousel-item"><div id="paceflow_row_'+div_id+'" class="row"/></div>');
                            video = [result.paceflow_drills[i], result.paceflow_drills[i+1]];
                            if (video[0]) {
                                var vid_1 = '';
                                var title = result.paceflow_drills[i]['name'];
                                if (result.paceflow_drills[i]['url'].includes('watch?v=')) {
                                    vid_1 = result.paceflow_drills[i]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_1 = result.paceflow_drills[i]['url'];
                                }
                                var id_1 = 'paceflow_0div'+div_id;
                                $('#paceflow_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_1+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_1).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_1+'"/>');
                                $('#'+id_1).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.paceflow_drills[i].slug+'">'+result.paceflow_drills[i].name+'</a>');
                                }
                            if (video[1]) {
                                var vid_2 = '';
                                var title = result.paceflow_drills[i+1]['name'];
                                if (result.paceflow_drills[i+1]['url'].includes('watch?v=')) {
                                    vid_2 = result.paceflow_drills[i+1]['url'].replace("watch?v=", 'embed/');
                                }
                                else {
                                   vid_2 = result.paceflow_drills[i+1]['url'];
                                }
                                var id_2 = 'paceflow_1div'+div_id;
                                $('#paceflow_row_'+div_id).append('<div class="col-12 col-md-6 col-lg-6 my-3"><div id="'+id_2+'" class="paceflow-upload-video-thumbnail"/></div>');
                                $('#'+id_2).append('<iframe class="paceflow-upload-video-thumbnail__image" src="'+vid_2+'"/>');
                                $('#'+id_2).append('<a class="paceflow-upload-video-thumbnail__text" href="/slides/slide/'+result.paceflow_drills[i+1].slug+'">'+result.paceflow_drills[i+1].name+'</a>');
                                }
                            }
                        }
                        var first_carousel = document.getElementById('paceflow_div_'+'1');
                        first_carousel.classList.add('active');
                        $('#prev_button_paceflow').show();
                        $('#next_button_paceflow').show();
                    }
                else{
                        $('#video_carousel_paceflow').append('<span class="paceflow-comment ml-5">No Paceflow Drills for this assessment. </span>');
                        $('#prev_button_paceflow').hide();
                        $('#next_button_paceflow').hide();
                    }

//                LEGALITY COMMENTS
                $('#legality_comments').empty();
                if(result.legality_notes){
                    for (var i=0; i<result.legality_notes.length; i++){
                        $('#legality_comments').append('<li class="paceflow-comment"><strong>' + result.legality_notes[i].name + '</strong>' + result.legality_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#legality_comments').append('There are no legality comments for this assessment');
                }
//                MOMENTUM COMMENTS
                $('#momentum_comments').empty();
                if(result.momentum_notes){
                    for (var i=0; i<result.momentum_notes.length; i++){
                        $('#momentum_comments').append('<li class="paceflow-comment"><strong>' + result.momentum_notes[i].name + '</strong>' + result.momentum_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#momentum_comments').append('There are no momentum comments for this assessment');
                }

//                STABILITY COMMENTS
                $('#stability_comments').empty();
                if(result.stability_notes){
                    for (var i=0; i<result.momentum_notes.length; i++){
                        $('#stability_comments').append('<li class="paceflow-comment"><strong>' + result.stability_notes[i].name + '</strong>' + result.stability_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#stability_comments').append('There are no stability comments for this assessment');
                }

//                PACEFLOW COMMENTS
                $('#paceflow_comments').empty();
                if(result.paceflow_notes){
                    for (var i=0; i<result.paceflow_notes.length; i++){
                        $('#paceflow_comments').append('<li class="paceflow-comment"><strong>' + result.paceflow_notes[i].name + '</strong>' + result.paceflow_notes[i].description + '</li>');
                        }
                    }
                else{
                    $('#paceflow_comments').append('There are no paceflow comments for this assessment');
                }
                $("summary_summary").empty();
                $("summary_momentum").empty();
                $("summary_stability").empty();
                $("summary_paceflow").empty();

                var summary_chart_ctx = document.getElementById("summary_summary").getContext('2d');
                var momentum_chart_ctx = document.getElementById("summary_momentum").getContext('2d');
                var stability_chart_ctx = document.getElementById("summary_stability").getContext('2d');
                var paceflow_chart_ctx = document.getElementById("summary_paceflow").getContext('2d');
                const summary_data = {
                      datasets: [{
                        data: [result.summary_summary_score, 100 - result.summary_summary_score],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    summary_chart.destroy();
                    summary_chart = new Chart(summary_chart_ctx, {
                        type: "doughnut",
                        data: summary_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                 enabled: false,
                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });
                const momentum_data = {
                      datasets: [{
                        data: [result.summary_momentum_score, 100 - Math.round(result.summary_momentum_score)],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    momentum_chart.destroy();
                    momentum_chart = new Chart(momentum_chart_ctx, {
                        type: "doughnut",
                        data: momentum_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                    enabled: false,

                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });

                const stability_data = {
                      datasets: [{
                        data: [result.summary_stability_score, 100 - result.summary_stability_score],
                        backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    stability_chart.destroy();
                    stability_chart = new Chart(stability_chart_ctx, {
                        type: "doughnut",
                        data: stability_data,
                        options: {
                            hover: {
                                mode: null
                            },
                                tooltips: {
                                    enabled: false,
                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });

                const paceflow_data = {
                      datasets: [{
                          data: [result.summary_paceflow_score, 100 - result.summary_paceflow_score],

                          backgroundColor: [
                            'rgb(59, 33, 93)',
                            'rgb(255, 255, 255)'
                        ],
                      }]
                    };
                    paceflow_chart.destroy();
                    paceflow_chart = new Chart(paceflow_chart_ctx, {
                        type: "doughnut",
                        data: paceflow_data,
                        options: {
                            hover: {
                                mode: null
                            },

                                tooltips: {
                                    enabled: false,

                            },
                            cutoutPercentage: 75,
                            responsive: true,
                            maintainAspectRatio: false,
                        },
                    });
                })
            }
        }
    });
});