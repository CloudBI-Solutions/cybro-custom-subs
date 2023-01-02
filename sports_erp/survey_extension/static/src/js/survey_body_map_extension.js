odoo.define('survey_extension.survey_body_map_extension', function(require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;
    var Qweb = core.qweb;
    var rpc = require('web.rpc');

//    require("survey.form");

//    console.log("KKKKKKKK")

     publicWidget.registry.bodyMapReviw = publicWidget.Widget.extend({
        selector: '.body_map_review',
         events:{
           'click .newcircle': 'onClickCircle',
           'click #btnDanger': 'onBtnDanger',
        },
        start: function () {
            var answer_id = false;
            if($('#answer').val() != ''){
                answer_id = $('#answer').val()
            }
            console.log(">..............>>",answer_id)

            var self = this;
            var res = this._super.apply(this, arguments);
            var NS = 'http://www.w3.org/2000/svg'
//            debugger;
//            $('#humanInner').on('click',self.onHumanInner.bind(this));
//            return res
            rpc.query({
                    model: 'survey.body.map.value',
                    method: 'get_body_map_value_data',
                    args: [[],parseInt(answer_id)],
                }).then(function (res){
                    if(res.length>0){
                        for(var i=0;i<res.length;i++){
                             var x_value = res[i].x_value
                            var y_value =res[i].y_value
                            var newCircIdParam = "newcircle" + x_value + '-' + y_value
                            var circle = document.createElementNS(NS, 'circle');
                            circle.setAttributeNS(null, 'cx', x_value);
                            circle.setAttributeNS(null, 'cy', y_value);
                            circle.setAttributeNS(null, 'r', 10);
                            circle.setAttributeNS(null, 'class', "newcircle");
                            circle.setAttributeNS(null, 'id', newCircIdParam);
                            circle.setAttributeNS(null, 'data-x', x_value);
                            circle.setAttributeNS(null, 'data-y', y_value);
                            $(self.el).find('#humanInner').after(circle)
                        }
                    }
                });
        },
        onClickCircle(e){
            var pinForm = $(this.el).find('#pinForm');
            rpc.query({
                        model: 'survey.body.map.value',
                        method: 'search_read',
                        args: [[['x_value','=',$(e.target).data('x')],['y_value','=',$(e.target).data('y')]]],
                    }).then(function (res){
                        if(res[0]['pain_level']){
                            $('#pain_level').val(res[0]['pain_level']);
                        }
                        if(res[0]['comment']){
                            $('#Comment').val(res[0]['comment']);
                        }
                        pinForm.show();
                    });
        },
        onBtnDanger(e){
            var pinForm = $(this.el).find('#pinForm');
            pinForm.hide();
        },
    });
//
    publicWidget.registry.bodyMap = publicWidget.Widget.extend({
        selector: '.body_map',
        events:{
           'click #btnSuccess': 'onBtnSuccess',
           'click #humanInner': '_onHumanInner',
           'click #btnConfirmTrue': 'onBtnConfirmTrue',
           'click #btnDanger': 'onBtnDanger',
           'click #pinConfirmSucces': 'onPinConfirmSucces',
           'click .newcircle': 'onClickCircle',
           'click #btnConfirmCancel': 'onBtnConfirmCancel',
        },
        start: function () {
            var answer_id = false;
            if($('#answer').val() != ''){
                answer_id = $('#answer').val()
            }
            var self = this;
            var res = this._super.apply(this, arguments);
            var NS = 'http://www.w3.org/2000/svg'
//            debugger;
//            $('#humanInner').on('click',self.onHumanInner.bind(this));
//            return res
            rpc.query({
                    model: 'survey.body.map.value',
                    method: 'get_body_map_value_data',
                    args: [[],parseInt(answer_id)],
                }).then(function (res){
                    if(res.length>0){
                        for(var i=0;i<res.length;i++){
                             var x_value = res[i].x_value
                            var y_value =res[i].y_value
                            var newCircIdParam = "newcircle" + x_value + '-' + y_value
                            var circle = document.createElementNS(NS, 'circle');
                            circle.setAttributeNS(null, 'cx', x_value);
                            circle.setAttributeNS(null, 'cy', y_value);
                            circle.setAttributeNS(null, 'r', 10);
                            circle.setAttributeNS(null, 'class', "newcircle");
                            circle.setAttributeNS(null, 'id', newCircIdParam);
                            circle.setAttributeNS(null, 'data-x', x_value);
                            circle.setAttributeNS(null, 'data-y', y_value);
                            $(self.el).find('#humanInner').after(circle)
                        }
                    }
                });
        },
        onBtnSuccess: function(e){
             $('#pinForm').hide();
            var Comment = $('#Comment').val();
//            var mark_area = $('#mark_area').val();
            var pain_level = $('#pain_level').val();
//            var name = $('#name').val();
            var answer = $('#answer').val();
            var question = $('#question').val();
            var x_value = $('#x_value').val();
            var y_value = $('#y_value').val();
            rpc.query({
                    model: 'survey.body.map.value',
                    method: 'create_data',
                    args: [[],{'comment':Comment,'pain_level':pain_level,'answer':parseInt(answer),'question':parseInt(question),'x_value':x_value,'y_value':y_value}],
                }).then(function (res){
                });

            $('#Comment').val('');
            $('#pain_level').val(0);
            $('#x_value').val('');
            $('#y_value').val('');
//          pinConfirmSucces.show();
        },
        _onHumanInner: function(e){
            var NS = 'http://www.w3.org/2000/svg';
            $('#Comment').val('');
            $('#pain_level').val(0);
            var t = e.target,
                x = e.clientX,
                y = e.clientY,
                target = (t == document.getElementById('humanAnatomy') ? document.getElementById('humanAnatomy') : t.parentNode),
                pin = this.pinCenter(target, x, y),
                newCircIdParam = "newcircle" + Math.round(pin.x) + '-' + Math.round(pin.y),
                circle = document.createElementNS(NS, 'circle');
            circle.setAttributeNS(null, 'cx', Math.round(pin.x));
            circle.setAttributeNS(null, 'cy', Math.round(pin.y));
            circle.setAttributeNS(null, 'r', 10);
            circle.setAttributeNS(null, 'class', "newcircle");
            circle.setAttributeNS(null, 'id', newCircIdParam);
            circle.setAttributeNS(null, 'data-x', Math.round(pin.x));
            circle.setAttributeNS(null, 'data-y', Math.round(pin.y));
            target.after(circle);

            $('#x_value').val(Math.round(pin.x));
            $('#y_value').val(Math.round(pin.y));

            $('#pinConfirm').show();
            $('#pinConfirmBtns').css({
                "left": (x ) + 'px',
                "top": (y) + 'px'
            });
        },
        pinCenter: function(element, x, y) {
            var pt = document.getElementById('humanAnatomy').createSVGPoint();
            pt.x = x;
            pt.y = y;
            return pt.matrixTransform(element.getScreenCTM().inverse());
        },
        onBtnConfirmTrue: function(e){
            $('#pinConfirm').hide();
            $('#pinForm').show();
        },
        onBtnDanger: function(e){
            $('#pinForm').hide();
            $('#pinConfirm').show();
            $('#Comment').val('');
            $('#pain_level').val(0);
            $('#x_value').val('');
            $('#y_value').val('');
        },
        onPinConfirmSucces: function(e){
            $('#pinConfirmSucces').hide();
        },
        onClickCircle: function(e){
             rpc.query({
                    model: 'survey.body.map.value',
                    method: 'search_read',
                    args: [[['x_value','=',$(e.target).data('x')],['y_value','=',$(e.target).data("y")]]],
                }).then(function (res){
                    if(res.length >0){
                        if(res[0]['pain_level']){
                            $('#pain_level').val(res[0]['pain_level']);
                        }
                        if(res[0]['comment']){
                            $('#Comment').val(res[0]['comment']);
                        }
                     }
                         $('#x_value').val($(e.target).data('x'));
                         $('#y_value').val($(e.target).data("y"));
                        $('#pinForm').show();


                });
        },
        onBtnConfirmCancel: function(e){
             rpc.query({
                    model: 'survey.body.map.value',
                    method: 'delete_body_map_value',
                    args: [[],{'x_value':$("#humanInner + .newcircle").data('x'),'y_value':$("#humanInner + .newcircle").data("y")}],
                }).then(function (res){
                    $("#humanInner + .newcircle").remove();
                    $('#pinConfirm').hide();
                });
        },

    });

    return {bodyMap:publicWidget.registry.bodyMap,bodyMapReviw:publicWidget.registry.bodyMapReviw}

});
