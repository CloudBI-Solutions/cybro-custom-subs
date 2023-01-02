odoo.define('survey_extension.surveyForm', function (require) {
    "use strict";
    var ajax = require('web.ajax');
//    const { Component, QWeb } = owl;
    console.log("oooooooooooooo")
    var rpc = require('web.rpc');
    var UserMenu = require('survey.form');
        console.log("QWEB", require('survey.form'))

    var time = require('web.time');
    var click = false;

    UserMenu.include({
        events: {
            'change .o_survey_form_choice_item': '_onChangeChoiceItem',
            'click .o_survey_matrix_btn': '_onMatrixBtnClick',
            'click button[type="submit"]': '_onSubmit',
            'change .singleFile':'_onChangeFile',
            'click .addfiles':'testing',
        },

         start: function () {
            var res = this._super.apply(this, arguments);
            console.log("jjjjj")
            var self = this;
            self.answer = [];
            self.onchange_id = [];
            self.$("input[data-question-type='calculated_metric']").each(function () {
                console.log(self, "self")
                if($(this).data('questionType') == 'calculated_metric'){
                    var question_id = $(this).prop('name');
                     ajax.jsonRpc("/survey/used_in_computation", 'call', {
                            'question_id': question_id,
                        }).then(function (result) {
                            console.log(result)
                            for(var i=0;i<result.length;i++){
                                 if(!self.onchange_id.includes(result[i]['id'])){
                                    self.onchange_id.push(result[i]['id'])
                                    if(result[i]['type'] == 'text_box'){
                                        console.log("Hiiiiiiiiiiii11111111111")
                                        $("textarea[name='"+result[i]['id']+"']").on('change', self._onCalculatedMatrixOperands.bind(self));
                                    }
                                    else if(result[i]['type'] == 'date' || result[i]['type'] == 'datetime'){
                                          self.$('div.o_survey_form_date').each(function () {
                                              if($(this).find('input[type="text"]')[0].name == result[i]['id']){
                                                  $(this).on('change.datetimepicker', self._onCalculatedMatrixOperandsTest.bind(self));
                                              }
                                          });
                                          console.log("Hiiiiiiiiiiii")
                                    }
                                     else{
                                        console.log("Hiiiiiiiiiiii87655544445", result[i])
                                        $("input[name='"+result[i]['id']+"']").on('change', self._onCalculatedMatrixOperands.bind(self));
                                     }
                                }
                            }
                        });
                    }
                });
//            this._toggleConditionalDisplay()
            self.load_default();
//            window.addEventListener("load", this._toggleConditionalDisplay)
         },

         load_default: function(){
            var btns = this.$el.find('input[default-load="True"]');
            for(var btn of btns){
                btn = this.$(btn)
                this._toggleConditionalDisplay(btn);
//                console.log('________', btn)
//                var def_val = btn[0]['defaultChecked']
//                if(! def_val) {
//                    var nodeValue = btn[0]['attributes'][9]['nodeValue'].slice(1,-1)
//                    console.log('VAAAAR', nodeValue)
//                    var obj = JSON.parse(nodeValue);
//                    var array = nodeValue.split('');
//                    console.log('____', array)
//                    this._toggleConditionalDisplay(btn);
//                    var val = 353;
//                    console.log('/////////', this.options)
//                    let dictionary = Object.assign({}, ...nodeValue.map((x) => ({[x.id]: x.value})));
//                    console.log("Objjj", dictionary)
//                }
            }
         },


         testing : function(ev){
            ev.preventDefault();
            ev.stopPropagation();
            $('.singleFile').click();
         },

         _toggleConditionalDisplay: function($target){
            var $choiceItemGroup = $target.closest('.o_survey_form_choice');
            console.log('____vals_____', $target.attr('vals'))
            var vals = eval($target.attr('vals'))
            var toggle_id = false
            var opposite_toggle_id = false
            for(var val of vals){
//                console.log('___val', val)
                   if($target.is(":checked")){
                       if(val.value == 'Yes'){
                            toggle_id = val.id.toString();
                       } else{
                        opposite_toggle_id = val.id.toString();
                       }
                   } else {
                        if(val.value == 'No'){
                            toggle_id = val.id.toString();
                       } else{
                        opposite_toggle_id = val.id.toString();
                       }
                   }
                }
//            console.log('TOGGLEEWE', toggle_id)
//            console.log('OPPOOOOSSS', )
//            console.log("vAAALLS", vals)

            if (this.options.questionsLayout !== "page_per_question"){
//                console.log("HERRRREEE")
//                console.log('toggle_id', toggle_id)
                if (click == true){
                    if (Object.keys(this.options.triggeredQuestionsByAnswer).includes(toggle_id)){
                        this.options.triggeredQuestionsByAnswer[toggle_id].forEach(function (question) {
                            var dependingQuestion = $('.js_question-wrapper#' +question);
                            console.log('depending', dependingQuestion)
                            dependingQuestion.toggleClass('d-none', false);
                        });
                     }
                     console.log('opposite_toggle_id', opposite_toggle_id)

                    if (Object.keys(this.options.triggeredQuestionsByAnswer).includes(opposite_toggle_id)){
//                        console.log("___", this.options.triggeredQuestionsByAnswer)
                        this.options.triggeredQuestionsByAnswer[opposite_toggle_id].forEach(function (question) {
                            console.log("question", question)
                            var dependingQuestion = $('.js_question-wrapper#' +question);
                            console.log('depending', dependingQuestion)

                            dependingQuestion.addClass('d-none', false);
                            });
                        }
                    }

                    //DEFAULT LOAD HEREEE >>>>

                if (click == false) {
                    var self = this;
                    rpc.query({
                        model: 'survey.user_input',
                        method: 'check_work',
                        args: [val['id']],
                    }).then(function (result) {
                        if (result){
                            var dependingQuestion = $('.js_question-wrapper#' +result);
                            dependingQuestion.toggleClass('d-none', false);
                        }
                    })
                   }
              }
         },

         _onChangeChoiceItem: function (event) {
//            var res = this._super.apply(this, arguments);
            console.log('__________here')
            var self = this;
            var $target = $(event.currentTarget);
//            console.log('____target', $target)
            var $choiceItemGroup = $target.closest('.o_survey_form_choice');
//            console.log('choiceItemGroup', $choiceItemGroup)
            var $otherItem = $choiceItemGroup.find('.o_survey_js_form_other_comment');
//            console.log('___other_item', $otherItem)
            var $commentInput = $choiceItemGroup.find('textarea[type="text"]');
//            console.log('comment_input', $commentInput)

            if ($otherItem.prop('checked') || $commentInput.hasClass('o_survey_comment')) {
                $commentInput.enable();
                $commentInput.closest('.o_survey_comment_container').removeClass('d-none');
                if ($otherItem.prop('checked')) {
                    $commentInput.focus();
                }
            } else {
                $commentInput.val('');
                $commentInput.closest('.o_survey_comment_container').addClass('d-none');
                $commentInput.enable(false);
            }

            var $matrixBtn = $target.closest('.o_survey_matrix_btn');

            if ($target.attr('type') === 'radio') {
                var isQuestionComplete = false;
//                console.log('mat_len', $matrixBtn.length)
                if ($matrixBtn.length > 0) {
                    $matrixBtn.closest('tr').find('td').removeClass('o_survey_selected');
                    $matrixBtn.addClass('o_survey_selected');
                    if (this.options.questionsLayout === 'page_per_question') {
                        var subQuestionsIds = $matrixBtn.closest('table').data('subQuestions');
                        var completedQuestions = [];
                        subQuestionsIds.forEach(function (id) {
                            if (self.$('tr#' + id).find('input:checked').length !== 0) {
                                completedQuestions.push(id);
                            }
                        });
                        isQuestionComplete = completedQuestions.length === subQuestionsIds.length;
                    }
                } else {
                    var previouslySelectedAnswer = $choiceItemGroup.find('label.o_survey_selected');
                    previouslySelectedAnswer.removeClass('o_survey_selected');

                    var newlySelectedAnswer = $target.closest('label');
                    if (newlySelectedAnswer.find('input').val() !== previouslySelectedAnswer.find('input').val()) {
                        newlySelectedAnswer.addClass('o_survey_selected');
                        isQuestionComplete = this.options.questionsLayout === 'page_per_question';
                    }

                    // Conditional display
                    if (this.options.questionsLayout !== 'page_per_question') {
                        var treatedQuestionIds = [];  // Needed to avoid show (1st 'if') then immediately hide (2nd 'if') question during conditional propagation cascade
//                        console.log('______previous_____', previouslySelectedAnswer.find('input').val())
                        if (Object.keys(this.options.triggeredQuestionsByAnswer).includes(previouslySelectedAnswer.find('input').val())) {
                            // Hide and clear depending question
                            this.options.triggeredQuestionsByAnswer[previouslySelectedAnswer.find('input').val()].forEach(function (questionId) {
                                var dependingQuestion = $('.js_question-wrapper#' + questionId);

                                dependingQuestion.addClass('d-none');
                                self._clearQuestionInputs(dependingQuestion);

                                treatedQuestionIds.push(questionId);
                            });
                            // Remove answer from selected answer
                            self.selectedAnswers.splice(self.selectedAnswers.indexOf(parseInt($target.val())), 1);
                        }
                        if (Object.keys(this.options.triggeredQuestionsByAnswer).includes($target.val())) {
                            // Display depending question
                            this.options.triggeredQuestionsByAnswer[$target.val()].forEach(function (questionId) {
                                if (!treatedQuestionIds.includes(questionId)) {
                                    var dependingQuestion = $('.js_question-wrapper#' + questionId);
                                    dependingQuestion.removeClass('d-none');
                                }
                            });
                            // Add answer to selected answer
                            this.selectedAnswers.push(parseInt($target.val()));
                        }
                    }
                }
                // Auto Submit Form
                var isLastQuestion = this.$('button[value="finish"]').length !== 0;
                var questionHasComment = $target.closest('.o_survey_form_choice').find('.o_survey_comment').length !== 0
                                            || $target.hasClass('o_survey_js_form_other_comment');
                if (!isLastQuestion && this.options.usersCanGoBack && isQuestionComplete && !questionHasComment) {
                    console.log("HERRRRERRE")
                    this._submitForm({});
                }
            } else {  // $target.attr('type') === 'checkbox'
                if ($matrixBtn.length > 0) {
                    $matrixBtn.toggleClass('o_survey_selected', !$matrixBtn.hasClass('o_survey_selected'));
                } else {

                ///// TOGGLEEE !!!!!!!!!!!!!!!!

                    if($target && $target[0].dataset && $target[0].dataset.questionType == 'toggle'){
//                        console.log('_________toggle', $target[0])
                        click = true;
                        var isQuestionComplete = false;
                        // Conditional display
//                        console.log('this__before', this.options)
                        this._toggleConditionalDisplay($target);
//                        console.log("aftrerr", $target.prop)
                        $target.prop('checked',$target.is(":checked"));
                        var previouslySelectedAnswer = $choiceItemGroup.find('label.o_survey_selected');
//                        console.log('____previouslySwl', previouslySelectedAnswer)

                    }
                    var $label = $target.closest('label');
                    $label.toggleClass('o_survey_selected', !$label.hasClass('o_survey_selected'));

                    // Conditional display
                    if (this.options.questionsLayout !== 'page_per_question' && Object.keys(this.options.triggeredQuestionsByAnswer).includes($target.val())) {
//                    console.log("________Console")
                        var isInputSelected = $label.hasClass('o_survey_selected');
                        // Hide and clear or display depending question
                        this.options.triggeredQuestionsByAnswer[$target.val()].forEach(function (questionId) {
                            var dependingQuestion = $('.js_question-wrapper#' + questionId);
                            dependingQuestion.toggleClass('d-none', !isInputSelected);
                            if (!isInputSelected) {
                                self._clearQuestionInputs(dependingQuestion);
                            }
                        });
                        // Add/remove answer to/from selected answer
                        if (!isInputSelected) {
                            self.selectedAnswers.splice(self.selectedAnswers.indexOf(parseInt($target.val())), 1);
                        } else {
                            self.selectedAnswers.push(parseInt($target.val()));
                        }
                    }
                }
            }
        },

         _onCalculatedMatrixOperandsTest:function(e){
            var self = this;
            console.log("hiiii")
            if($(e.currentTarget).find('input[type="text"]').length !== 0){
                var answer = $(e.currentTarget).find('input[type="text"]').val()
                var question_id = $(e.currentTarget).find('input[type="text"]')[0].name
                if(self.onchange_id.includes(parseInt(question_id))){
                    ajax.jsonRpc("/survey/get_calculated_metric_info_answer", 'call', {
                                'question_id': question_id,
                                'answer':answer,
                                'answer_lst':self.answer,
                            }).then(function (result) {
                                self.answer = result
                                for(var i=0;i<result.length;i++){
                                        $("input[name='"+result[i]['question_id']+"']").val(result[i]['answer'])
                                }
                            });
                }
            }
         },
         _onCalculatedMatrixOperands: function(e){
            var self = this
            console.log(e, "event")
            ajax.jsonRpc("/survey/get_calculated_metric_info_answer", 'call', {
                            'question_id': e.target.name,
                            'answer':e.target.value,
                            'answer_lst':self.answer,
                        }).then(function (result) {
                            self.answer = result
                            for(var i=0;i<result.length;i++){
                                    $("input[name='"+result[i]['question_id']+"']").val(result[i]['answer'])
                            }
                        });
         },
         _onChangeFile: function(ev){
            $.blockUI();
            var $i = $(ev.currentTarget);
            var input = $i[0];
            var file_data = "";
            if (input.files && input.files[0]) {
                var file = input.files[0]; // The file
                var fr = new FileReader(); // FileReader instance
                var filename = file['name']
                if($('#fileLabel').length > 0){
                    $('#fileLabel')[0].innerHTML = filename;
                }
                fr.onload = function () {
                    file_data = fr.result;
                    if (file_data) {
                        $('.image_data').val(file.name+','+file_data.split(",")[1])
                    }
                    $.unblockUI();
                };
                fr.readAsDataURL(file);
            }
            else{
                if($('#fileLabel').length > 0){
                    $('#fileLabel')[0].innerHTML = 'Choose File';
                }
                $.unblockUI();
            }
        },
        _prepareSubmitValues: function (formData, params) {
            var self = this;
            console.log('paraaaamsmms', params)
            console.log("FORM DATA", formData)
            console.log("PARAMS", params)
            formData.forEach(function (value, key) {
                console.log('key.....', key)
                console.log('value......', value)
//                switch (key) {
//                    case 'csrf_token':
//                    case 'token':
//                    case 'page_id':
//                    case 'question_id':
                        params[key] = value;
//                        break;
//                }
                console.log("HHAHHHA", params)
            });

            // Get all question answers by question type
            this.$('[data-question-type]').each(function () {
                    switch ($(this).data('questionType')) {

                        case 'text_box':
                        case 'char_box':
                        case 'numerical_box':
                        case 'progress_bar':
                            params[this.name] = this.value;
                            break;
                        case 'toggle':
                            params[this.name] = $(this).is(":checked");
                            console.log("paraaaamsss", params)
                            break;
                        case 'calculated_metric':
                            params[this.name] = this.value;
                            break;
                        case 'date':
                            params = self._prepareSubmitDates(params, this.name, this.value, false);
                            break;
                        case 'datetime':
                            params = self._prepareSubmitDates(params, this.name, this.value, true);
                            break;
                        case 'simple_choice_radio':
                        case 'multiple_choice':
                            params = self._prepareSubmitChoices(params, $(this), $(this).data('name'));
                            break;
                        case 'matrix':
                            params = self._prepareSubmitAnswersMatrix(params, $(this));
                            break;
                        case 'file':
                            params[this.name] = this.value;
                            break;
                        case 'body_map':
                }
            });
        },
        _prepareSubmitCalculatedMetric: function (params, questionId, value, isDateTime) {
            console.log("test")
            params['question_id'] = questionId
            $.ajax({
                url: '/survey/get_calculated_metric_info',
                type: 'POST',
                data: params,
                async: false,
                cache: false,
                success: function (html) {
                    params[questionId] = html;
                    return params;
                }
            });

        },
        _onNextScreenDone: function (result, options) {
//            var res = this._super.apply(this, arguments);
            var self = this;
//            console.log('herrreee___ next screen', this)
            if (!(options && options.isFinish)
                && !this.options.sessionInProgress) {
                this.preventEnterSubmit = false;
            }

            if (result && !result.error) {
                this.$(".o_survey_form_content").empty();
                this.$(".o_survey_form_content").html(result.survey_content);

                if (result.survey_progress && this.$surveyProgress.length !== 0) {
                    this.$surveyProgress.html(result.survey_progress);
                } else if (options.isFinish && this.$surveyProgress.length !== 0) {
                    this.$surveyProgress.remove();
                }
                if ($(result.survey_content).find('.body_map').length !== 0 ) {
                    location.reload();
                }

                if($(result.survey_content).find("input[data-question-type='calculated_metric']").length !== 0){
                    self.$("input[data-question-type='calculated_metric']").each(function () {
                        if($(this).data('questionType') == 'calculated_metric'){
                            var question_id = $(this).prop('name');
                             ajax.jsonRpc("/survey/used_in_computation", 'call', {
                                    'question_id': question_id,
                                }).then(function (result) {

                                    console.log(result, "result")
                                    for(var i=0;i<result.length;i++){
                                         if(!self.onchange_id.includes(result[i]['id'])){
                                            self.onchange_id.push(result[i]['id'])
                                            if(result[i]['type'] == 'text_box'){
                                            console.log("Hlooooo", "234567")
                                                $("textarea[name='"+result[i]['id']+"']").on('change', self._onCalculatedMatrixOperands.bind(self));
                                            }
                                            else if(result[i]['type'] == 'date' || result[i]['type'] == 'datetime'){
                                                 self.$('div.o_survey_form_date').each(function () {
                                                      if($(this).find('input[type="text"]')[0].name == result[i]['id']){
                                                          $(this).on('change.datetimepicker', self._onCalculatedMatrixOperandsTest.bind(self));
                                                      }
                                                  });
                                                  console.log("Hlooooo")
                                            }
                                             else{
                                             console.log("Hlooooo", "jjjj")
                                                $("input[name='"+result[i]['id']+"']").on('change', self._onCalculatedMatrixOperands.bind(self));

                                             }
                                        }
                                    }
                                });
                        }
                    });
                }

                if (result.survey_navigation && this.$surveyNavigation.length !== 0) {
                    this.$surveyNavigation.html(result.survey_navigation);
                    this.$surveyNavigation.find('.o_survey_navigation_submit').on('click', self._onSubmit.bind(self));
                }

                // Hide timer if end screen (if page_per_question in case of conditional questions)
                if (self.options.questionsLayout === 'page_per_question' && this.$('.o_survey_finished').length > 0) {
                    options.isFinish = true;
                }

                this.$('div.o_survey_form_date').each(function () {
                    self._initDateTimePicker($(this));
                });
                if (this.options.isStartScreen || (options && options.initTimer)) {
                    this._initTimer();
                    this.options.isStartScreen = false;
                } else {
                    if (this.options.sessionInProgress && this.surveyTimerWidget) {
                        this.surveyTimerWidget.destroy();
                    }
                }
                if (options && options.isFinish) {
                    this._initResultWidget();
                    if (this.surveyBreadcrumbWidget) {
                        this.$('.o_survey_breadcrumb_container').addClass('d-none');
                        this.surveyBreadcrumbWidget.destroy();
                    }
                    if (this.surveyTimerWidget) {
                        this.surveyTimerWidget.destroy();
                    }
                } else {
                    this._updateBreadcrumb();
                }
                self._initChoiceItems();
                self._initTextArea();

                if (this.options.sessionInProgress && this.$('.o_survey_form_content_data').data('isPageDescription')) {
                    // prevent enter submit if we're on a page description (there is nothing to submit)
                    this.preventEnterSubmit = true;
                }

                this.$('.o_survey_form_content').fadeIn(this.fadeInOutDelay);
                $("html, body").animate({ scrollTop: 0 }, this.fadeInOutDelay);
                self._focusOnFirstInput();
            }
            else if (result && result.fields && result.error === 'validation') {
                this.$('.o_survey_form_content').fadeIn(0);
                this._showErrors(result.fields);
            } else {
                var $errorTarget = this.$('.o_survey_error');
                $errorTarget.removeClass("d-none");
                this._scrollToError($errorTarget);
            }
        },
    });

});
