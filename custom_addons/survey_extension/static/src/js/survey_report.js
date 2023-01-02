odoo.define('survey_extension.survey_report', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var session = require('web.session');
    var QWeb = core.qweb;
    var rpc = require('web.rpc')
    console.log(">>>>>>>>>>>>>>>>>>>>>>dddddddddddd")
    var survey_report = AbstractAction.extend({
        template: 'survey_report_test',
        events:{
            'click .search_btn': 'onClickSearchButton',
        },
        init: function (parent, action) {
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;
            console.log(">>>>>>>>>>>>>>Tesr")
            rpc.query({
	 	            model: 'res.users',
	 	            method: 'search_read',
	 	            args: [[]],
	 	        }).then(function (users) {
	 	            for(var i=0;i<users.length;i++){
                        $(self.$el).find("#user").append( $("<option>").val(users[i]['id']).html(users[i]['name']));
                    }
                    rpc.query({
                            model: 'survey.survey',
                            method: 'search_read',
                            args: [[]],
                        }).then(function (result) {
                            console.log(">>>>>>>>>",result)
                            for(var i=0;i<result.length;i++){
                                $(self.$el).find("#survey").append( $("<option>").val(result[i]['id']).html(result[i]['title']));
                            }
                            self.set_date_data()
                            self.onClickSearchButton()
                        });

                    });
//            self.set_date_data()
//            self.onClickSearchButton()
        },
        set_date_data: function(){
             var self = this;
             var start_date = false
             var end_date = false
             start_date = $('#start_date').val()
             end_date = $('#end_date').val()
    //         if(start_date == "" || start_date == undefined){
                 var today = new Date();
                 today.setMonth(today.getMonth() - 1);
                  var dd = String(today.getDate()).padStart(2, '0');
                 var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                 var yyyy = today.getFullYear();
                 start_date = yyyy +'-'+mm +'-'+dd;
                 $(self.$el).find('#start_date').val(start_date);
    //         }
    //         if(end_date == "" || end_date == undefined){
                 var today = new Date();
                 var dd = String(today.getDate()).padStart(2, '0');
                 var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                 var yyyy = today.getFullYear();
                 today = yyyy +'-'+mm +'-'+dd;
                 end_date = today
                 $(self.$el).find('#end_date').val(today)
    //         }
        },
        onClickSearchButton: function(){
            var self = this;
            var survey = $(self.$el).find('#survey').val()
            var user = $(self.$el).find('#user').val()
            var start_date = false
            var end_date = false
            start_date = $(self.$el).find('#start_date').val()
            end_date = $(self.$el).find('#end_date').val()
             rpc.query({
	 	            model: 'survey.user_input.line',
	 	            method: 'get_survey_user_input_line_data',
	 	            args: [[],survey,user,start_date,end_date],
	 	        }).then(function (result) {
                    console.log(">>>>>>>>>>>>result",result)
                    $('.Report-content').html(QWeb.render('survey-answer-table', result));
	 	        });
        },
	});

	core.action_registry.add("survey_report", survey_report);


});