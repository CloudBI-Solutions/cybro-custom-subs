odoo.define('survey_question.survey_form', function (require) {
'use strict';

var field_utils = require('web.field_utils');
var publicWidget = require('web.public.widget');
var time = require('web.time');
var core = require('web.core');
var Dialog = require('web.Dialog');
var dom = require('web.dom');
var utils = require('web.utils');
const ajax = require('web.ajax');

var _t = core._t;

publicWidget.registry.DiariesSurvey = publicWidget.Widget.extend({
    selector: '.o_survey_form',
    events: {
        'change .js_question-wrapper': '_onChangeformContent',
//        'click .o_survey_matrix_btn': '_onMatrixBtnClick',
//        'click button[type="submit"]': '_onSubmit',
    },
    _onChangeformContent: function(ev){
//        console.log(ev.target.dataset,"toggle")
//        console.log(ev.currentTarget.is(":checked"), "toggle1234")
        var answer
        if(ev.target.dataset.questionType === 'toggle'){
                    answer = $(ev.target).is(":checked")
                }
               else{
                answer = ev.target.value
               }
               console.log(answer)


         ajax.jsonRpc("/survey/calculated_metric", 'call', {
                        'question_id': ev.currentTarget.id,
                        'answer': answer
                    }).then(function (result) {
//                        self.answer = result
//                        for(var i=0;i<result.length;i++){
//                                $("input[name='"+result[i]['question_id']+"']").val(result[i]['answer'])
//                        }
                    });

    },
    })
    })