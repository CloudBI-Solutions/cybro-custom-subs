odoo.define('paceflow.history_dashboard', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');

    $(document).ready(function(){
    var assessment_id = $("select[id='h_filter_selection']").val();
    var child_id = $("input[id='h_child_id']").val();
    if(assessment_id){
        rpc.query({
            model: 'assessment.assessment',
            method: 'get_history_dashboard_data',
            args: [assessment_id],
            })
            .then(function (result) {

                var progress_chart = document.getElementById("progress_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;
                var progressData = {
                      labels: x_axis,
                      datasets: [{
                        label: "Score",
                        backgroundColor: "rgba(200,0,0,0.2)",
                        borderColor: "#ff0088",
                        data: y_axis
                      }]
                    };

                    var radarChart = new Chart(progress_chart, {
                      type: 'radar',
                      data: progressData,
                      options: {
                            tooltips: {
                                        enabled: true,
                                        callbacks: {
                                            label: function(tooltipItem, data) {
                                                return data.datasets[tooltipItem.datasetIndex].label + ' : ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                            }
                                        }
                                    },
                            responsive: true, // Instruct chart js to respond nicely.
                            maintainAspectRatio: false,
                            elements: {
                              line: {
                                borderWidth: 3
                              }
                            },
                            scale: {
                            animation: false,
                            ticks: {
                                beginAtZero: true,
                                max: 100,
                                min: 0,
                                stepSize: 10
                            }

                            }
                          },
                    });
            })
        }
        if(child_id){
        rpc.query({
            model: 'assessment.assessment',
            method: 'get_speed_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var speed_chart = document.getElementById("speed_canvas").getContext('2d');
                // Define the data
                var speed_x_axis = result.x_axis; // Add data values to array
                var speed_y_axis = result.y_axis;
                var mySpeedChart = new Chart(speed_chart, {
                    type: 'line',
                    data: {
                        labels: speed_x_axis,//x axis
                        datasets: [{
                                label: 'Ball-speed', // Name the series
                                data: speed_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            })
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_score_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var score_chart = document.getElementById("score_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myScoreChart = new Chart(score_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Pace-flow Score', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_legality_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var legality_chart = document.getElementById("legality_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;
                var myLegalityChart = new Chart(legality_chart, {
                    type: 'line',
                    data: {
                        labels: x_axis,//x axis
                        datasets: [{
                                label: 'Legality', // Name the series
                                data: y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_runup_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var runup_chart = document.getElementById("runup_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;
                var myRunupChart = new Chart(runup_chart, {
                    type: 'line',
                    data: {
                        labels: x_axis,//x axis
                        datasets: [{
                                label: 'Momentum', // Name the series
                                data: y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_stride_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var stride_chart = document.getElementById("stride_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;
                var myScoreChart = new Chart(stride_chart, {
                    type: 'line',
                    data: {
                        labels: x_axis,//x axis
                        datasets: [{
                                label: 'Stability', // Name the series
                                data: y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_ffc_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var ffc_chart = document.getElementById("ffc_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;
                var myFFCChart = new Chart(ffc_chart, {
                    type: 'line',
                    data: {
                        labels: x_axis,//x axis
                        datasets: [{
                                label: 'Paceflow', // Name the series
                                data: y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
//            rpc.query({
//            model: 'assessment.assessment',
//            method: 'get_ft_dashboard_data',
//            args: [child_id],
//            })
//            .then(function (result) {
//                var ft_chart = document.getElementById("ft_canvas").getContext('2d');
//                // Define the data
//                var x_axis = result.x_axis; // Add data values to array
//                var y_axis = result.y_axis;
//                var myFTChart = new Chart(ft_chart, {
//                    type: 'line',
//                    data: {
//                        labels: x_axis,//x axis
//                        datasets: [{
//                                label: 'BR-FT', // Name the series
//                                data: y_axis, // Specify the data values array
//                                backgroundColor: '#ff0088',
//                                borderColor: '#ff0088',
//
//                                borderWidth: 2, // Specify bar border width
//                                type: 'line', // Set this data to a line chart
//                                fill: false
//                            }
//                        ]
//                    },
//                    options: {
//                        responsive: true, // Instruct chart js to respond nicely.
//                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
//                        scales: {
//                            animation: false,
//                            yAxes: [{
//                                display: true,
//                                ticks: {
//                                    min: 0,
//                                    max: 100
//                                }
//                            }]
//                        }
//                    }
//                });
//            })
            }
    });
    publicWidget.registry.websiteProgressDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_filter',
        events: {
               //tile filter
               'change #h_date_from': '_onChangeDateFilter',
               'change #h_date_to': '_onChangeDateFilter',
               'change #h_filter_selection': '_onChangeFilter',
               'click #h_clear_dates': '_onClickClear',
    },
    _onClickClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_date_from']").val(null);
         $("input[id='h_date_to']").val(null);
         ajax.jsonRpc('/get_history_filter_clear_data', 'call', {'child_id': child_id})
                .then(function (result) {
                    $('#h_filter_selection option').remove();
                    for (var i=0; i<result.length; i++){
            $('#h_filter_selection').append($('<option>',
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
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_date_from']").val();
         var date_to = $("input[id='h_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_history_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    $('#h_filter_selection option').remove();
                    for (var i=0; i<result.length; i++){
                        $('#h_filter_selection').append($('<option>',
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
         var assessment_id = $("select[id='h_filter_selection']").val();
         rpc.query({
            model: 'assessment.assessment',
            method: 'get_history_dashboard_data',
            args: [assessment_id],
            })
            .then(function (result) {
                var progress_chart = document.getElementById("progress_canvas").getContext('2d');
                // Define the data
                var x_axis = result.x_axis; // Add data values to array
                var y_axis = result.y_axis;

                var progressData = {
                      labels: x_axis,
                      datasets: [{
                        label: "Score",
                        backgroundColor: "rgba(200,0,0,0.2)",
                        borderColor: "#ff0088",
                        data: y_axis
                      }]
                    };
                var radarChart = new Chart(progress_chart, {
                      type: 'radar',
                      data: progressData,
                      options: {
                            tooltips: {
                                        enabled: true,
                                        callbacks: {
                                            label: function(tooltipItem, data) {
                                                return data.datasets[tooltipItem.datasetIndex].label + ' : ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                            }
                                        }
                                    },
                            responsive: true, // Instruct chart js to respond nicely.
                            maintainAspectRatio: false,
                            elements: {
                              line: {
                                borderWidth: 3
                              }
                            },
                            scale: {
                            animation: false,
                            ticks: {
                                beginAtZero: true,
                                max: 100,
                                min: 0,
                                stepSize: 10
                            }

                            }
                          },
                    });
            })

         },
    });

    publicWidget.registry.websiteSpeedDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_speed_filter',
        events: {
               //tile filter
               'change #h_speed_date_from': '_onChangeSpeedDateFilter',
               'change #h_speed_date_to': '_onChangeSpeedDateFilter',
               'click #h_speed_clear_dates': '_onClickSpeedClear',
    },
    _onClickSpeedClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_speed_date_from']").val(null);
         $("input[id='h_speed_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_speed_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var speed_chart = document.getElementById("speed_canvas").getContext('2d');
                // Define the data
                var speed_x_axis = result.x_axis; // Add data values to array
                var speed_y_axis = result.y_axis;
                var mySpeedChart = new Chart(speed_chart, {
                    type: 'line',
                    data: {
                        labels: speed_x_axis,//x axis
                        datasets: [{
                                label: 'Ball-speed', // Name the series
                                data: speed_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });

            })
         },
         _onChangeSpeedDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_speed_date_from']").val();
         var date_to = $("input[id='h_speed_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_speed_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var speed_chart = document.getElementById("speed_canvas").getContext('2d');
                // Define the data
                var speed_x_axis = result.x_axis; // Add data values to array
                var speed_y_axis = result.y_axis;
                var mySpeedChart = new Chart(speed_chart, {
                    type: 'line',
                    data: {
                        labels: speed_x_axis,//x axis
                        datasets: [{
                                label: 'Ball-speed', // Name the series
                                data: speed_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteScoreDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_score_filter',
        events: {
               //tile filter
               'change #h_score_date_from': '_onChangeScoreDateFilter',
               'change #h_score_date_to': '_onChangeScoreDateFilter',
               'click #h_score_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_score_date_from']").val(null);
         $("input[id='h_score_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_score_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var score_chart = document.getElementById("score_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myScoreChart = new Chart(score_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Pace-flow Score', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_score_date_from']").val();
         var date_to = $("input[id='h_score_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_score_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var score_chart = document.getElementById("score_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myScoreChart = new Chart(score_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Pace-flow Score', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteLegalityDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_legality_filter',
        events: {
               //tile filter
               'change #h_legality_date_from': '_onChangeScoreDateFilter',
               'change #h_legality_date_to': '_onChangeScoreDateFilter',
               'click #h_legality_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_legality_date_from']").val(null);
         $("input[id='h_legality_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_legality_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var legality_chart = document.getElementById("legality_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myLegalityChart = new Chart(legality_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Legality', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_legality_date_from']").val();
         var date_to = $("input[id='h_legality_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_legality_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var legality_chart = document.getElementById("legality_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myLegalityChart = new Chart(legality_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Run-up', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteRunUpDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_runup_filter',
        events: {
               //tile filter
               'change #h_runup_date_from': '_onChangeScoreDateFilter',
               'change #h_runup_date_to': '_onChangeScoreDateFilter',
               'click #h_runup_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_runup_date_from']").val(null);
         $("input[id='h_runup_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_runup_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var runup_chart = document.getElementById("runup_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myRunUpChart = new Chart(runup_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Run-up', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_runup_date_from']").val();
         var date_to = $("input[id='h_runup_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_runup_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var runup_chart = document.getElementById("runup_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myRunUpChart = new Chart(runup_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Run-up', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteStrideDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_stride_filter',
        events: {
               //tile filter
               'change #h_stride_date_from': '_onChangeScoreDateFilter',
               'change #h_stride_date_to': '_onChangeScoreDateFilter',
               'click #h_stride_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_stride_date_from']").val(null);
         $("input[id='h_stride_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_stride_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var stride_chart = document.getElementById("stride_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myStrideChart = new Chart(stride_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Stride', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_stride_date_from']").val();
         var date_to = $("input[id='h_stride_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_stride_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var stride_chart = document.getElementById("stride_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myStrideChart = new Chart(stride_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'Stride', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteFFCDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_ffc_filter',
        events: {
               //tile filter
               'change #h_ffc_date_from': '_onChangeScoreDateFilter',
               'change #h_ffc_date_to': '_onChangeScoreDateFilter',
               'click #h_ffc_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_ffc_date_from']").val(null);
         $("input[id='h_ffc_date_to']").val(null);
            rpc.query({
            model: 'assessment.assessment',
            method: 'get_ffc_dashboard_data',
            args: [child_id],
            })
            .then(function (result) {
                var ffc_chart = document.getElementById("ffc_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myFFCChart = new Chart(ffc_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'FFC-BR', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_ffc_date_from']").val();
         var date_to = $("input[id='h_ffc_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_ffc_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var ffc_chart = document.getElementById("ffc_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myFFCChart = new Chart(ffc_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'FFC-BR', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

    publicWidget.registry.websiteFTDashboardAssessments = publicWidget.Widget.extend({
        selector: '#h_ft_filter',
        events: {
               //tile filter
               'change #h_ft_date_from': '_onChangeScoreDateFilter',
               'change #h_ft_date_to': '_onChangeScoreDateFilter',
               'click #h_ft_clear_dates': '_onClickScoreClear',
    },
    _onClickScoreClear: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         $("input[id='h_ft_date_from']").val(null);
         $("input[id='h_ft_date_to']").val(null);
//            rpc.query({
//            model: 'assessment.assessment',
//            method: 'get_ft_dashboard_data',
//            args: [child_id],
//            })
//            .then(function (result) {
//                var ft_chart = document.getElementById("ft_canvas").getContext('2d');
//                // Define the data
//                var score_x_axis = result.x_axis; // Add data values to array
//                var score_y_axis = result.y_axis;
//                var myFTChart = new Chart(ft_chart, {
//                    type: 'line',
//                    data: {
//                        labels: score_x_axis,//x axis
//                        datasets: [{
//                                label: 'BR-FT', // Name the series
//                                data: score_y_axis, // Specify the data values array
//                                backgroundColor: '#ff0088',
//                                borderColor: '#ff0088',
//
//                                borderWidth: 2, // Specify bar border width
//                                type: 'line', // Set this data to a line chart
//                                fill: false
//                            }
//                        ]
//                    },
//                    options: {
//                        responsive: true, // Instruct chart js to respond nicely.
//                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
//                        scales: {
//                            animation: false,
//                            yAxes: [{
//                                display: true,
//                                ticks: {
//                                    min: 0,
//                                    max: 100
//                                }
//                            }]
//                        }
//                    }
//                });
//            })
         },
         _onChangeScoreDateFilter: function (ev) {
         ev.preventDefault();
         var self = this
         var child_id = $("input[id='h_child_id']").val();
         var date_from = $("input[id='h_ft_date_from']").val();
         var date_to = $("input[id='h_ft_date_to']").val();
         if(date_to && date_from){
                ajax.jsonRpc('/get_ft_filter_data', 'call', {'date_from': date_from, 'date_to': date_to, 'child_id': child_id})
                .then(function (result) {
                    var ft_chart = document.getElementById("ft_canvas").getContext('2d');
                // Define the data
                var score_x_axis = result.x_axis; // Add data values to array
                var score_y_axis = result.y_axis;
                var myFTChart = new Chart(ft_chart, {
                    type: 'line',
                    data: {
                        labels: score_x_axis,//x axis
                        datasets: [{
                                label: 'BR-FT', // Name the series
                                data: score_y_axis, // Specify the data values array
                                backgroundColor: '#ff0088',
                                borderColor: '#ff0088',

                                borderWidth: 2, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                        scales: {
                            animation: false,
                            yAxes: [{
                                display: true,
                                ticks: {
                                    min: 0,
                                    max: 100
                                }
                            }]
                        }
                    }
                });
                });
            }
         },
    });

});