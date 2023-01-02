odoo.define('odoo11_magento2.magento_dashboard', function (require) {
"use strict";

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var myChart = null;

    var MagentoDashboard = AbstractAction.extend({
        contentTemplate: 'Magento_Dashboard',
        events: {
            'click .my_orders': 'my_orders',
            'click .my_shipments': 'my_shipments',
            'click .my_stores': 'my_stores',
            'click .amount_due': 'invoice',
            'click .total_invoiced': 'invoice',
            'click .credit_note': 'credit_note',
            'click .customers': 'customers',
            'click .products': 'products',
            'change #dependent_values': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="this_year"){
                    this.onclick_this_year($target.val());
                }else if (value=="this_quarter"){
                    this.onclick_this_quarter($target.val());
                }else if (value=="this_month"){
                    this.onclick_this_month($target.val());
                }else if (value=="this_week"){
                    this.onclick_this_week($target.val());
                }
            },
            'change #total_sales': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="sales_today"){
                    this.onclick_sales_today($target.val());
                }else if (value=="sales_7"){
                    this.onclick_sales_7($target.val());
                }
            },
        },

        my_orders: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("My Orders"),
                type: 'ir.actions.act_window',
                res_model: 'sale.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['magento', '=', true]],
                target: 'current',
            }, options)
        },

        my_shipments: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("My Shipments"),
                type: 'ir.actions.act_window',
                res_model: 'shipment.shipment',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                target: 'current',
            }, options)
        },

        my_stores: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("My Stores"),
                type: 'ir.actions.act_window',
                res_model: 'stores.magento',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                target: 'current',
            }, options)
        },

        invoice: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Invoice"),
                type: 'ir.actions.act_window',
                res_model: 'account.move',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['magento', '=', true], ['move_type', '!=', 'out_refund']],
                target: 'current',
            }, options)
        },

        credit_note: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Credit Notes"),
                type: 'ir.actions.act_window',
                res_model: 'account.move',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['magento', '=', true], ['move_type', '=', 'out_refund']],
                target: 'current',
            }, options)
        },

        customers: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Customers"),
                type: 'ir.actions.act_window',
                res_model: 'res.partner',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['magento', '=', true]],
                target: 'current',
            }, options)
        },

        products: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Products"),
                type: 'ir.actions.act_window',
                res_model: 'product.product',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['magento', '=', true]],
                target: 'current',
            }, options)
        },

        onclick_this_year: function(){
            var self = this;
            rpc.query({
                model: 'magento.dashboard',
                method: 'this_year',
                args: [[]],
            }).then(function (result) {

                $('#total_this_month').hide();
                $('#due_this_month').hide();
                $('#shipment_this_month').hide();
                $('#invoiced_this_month').hide();
                $('#credit_note_this_month').hide();

                $('#total_this_quarter').hide();
                $('#due_this_quarter').hide();
                $('#shipment_this_quarter').hide();
                $('#invoiced_this_quarter').hide();
                $('#credit_note_this_quarter').hide();

                $('#total_this_week').hide();
                $('#due_this_week').hide();
                $('#shipment_this_week').hide();
                $('#invoiced_this_week').hide();
                $('#credit_note_this_week').hide();

                $('#total_this_year').show();
                $('#due_this_year').show();
                $('#shipment_this_year').show();
                $('#invoiced_this_year').show();
                $('#credit_note_this_year').show();

                if(!result[0]['sum']){
                    $('#total_this_year').empty().append('No Orders');
                }
                else{
                    $('#total_this_year').empty().append(result[3]['symbol'] + ' ' + result[0]['sum']);
                }
                if(!result[2]['due']){
                    $('#due_this_year').empty().append('No Orders');
                }
                else{
                    $('#due_this_year').empty().append(result[3]['symbol'] + ' ' + result[2]['due']);
                }
                $('#shipment_this_year').empty().append(result[4]['shipment']);
                if(!result[6]['invoiced']){
                    $('#invoiced_this_year').empty().append('No Orders');
                }
                else{
                    $('#invoiced_this_year').empty().append(result[3]['symbol'] + ' ' + result[6]['invoiced']);
                }
                if(!result[7]['credit_note']){
                    $('#credit_note_this_year').empty().append('No Orders');
                }
                else{
                    $('#credit_note_this_year').empty().append(result[3]['symbol'] + ' ' + result[7]['credit_note']);
                }
            })
        },

        onclick_this_quarter: function(){
            var self = this;
            rpc.query({
                model: 'magento.dashboard',
                method: 'this_quarter',
                args: [[]],
            }).then(function (result) {

                $('#total_this_month').hide();
                $('#due_this_month').hide();
                $('#shipment_this_month').hide();
                $('#invoiced_this_month').hide();
                $('#credit_note_this_month').hide();

                $('#total_this_year').hide();
                $('#due_this_year').hide();
                $('#shipment_this_year').hide();
                $('#invoiced_this_year').hide();
                $('#credit_note_this_year').hide();

                $('#total_this_week').hide();
                $('#due_this_week').hide();
                $('#shipment_this_week').hide();
                $('#invoiced_this_week').hide();
                $('#credit_note_this_week').hide();

                $('#total_this_quarter').show();
                $('#due_this_quarter').show();
                $('#shipment_this_quarter').show();
                $('#invoiced_this_quarter').show();
                $('#credit_note_this_quarter').show();

                if(!result[0]['sum']){
                    $('#total_this_quarter').empty().append('No Orders');
                }
                else{
                    $('#total_this_quarter').empty().append(result[3]['symbol'] + ' ' + result[0]['sum']);
                }
                if(!result[2]['due']){
                    $('#due_this_quarter').empty().append('No Orders');
                }
                else{
                    $('#due_this_quarter').empty().append(result[3]['symbol'] + ' ' + result[2]['due']);
                }
                $('#shipment_this_quarter').empty().append(result[4]['shipment']);
                if(!result[6]['invoiced']){
                    $('#invoiced_this_quarter').empty().append('No Orders');
                }
                else{
                    $('#invoiced_this_quarter').empty().append(result[3]['symbol'] + ' ' + result[6]['invoiced'])
                }
                if(!result[7]['credit_note']){
                    $('#credit_note_this_quarter').empty().append('No Orders');
                }
                else{
                    $('#credit_note_this_quarter').empty().append(result[3]['symbol'] + ' ' + result[7]['credit_note'])
                }
            })
        },

        onclick_this_month: function() {
            var self = this;
            rpc.query({
                model: 'magento.dashboard',
                method: 'this_month',
                args: [[]],
            }).then(function (result) {

                $('#total_this_year').hide();
                $('#due_this_year').hide();
                $('#shipment_this_year').hide();
                $('#invoiced_this_year').hide();
                $('#credit_note_this_year').hide();

                $('#total_this_quarter').hide();
                $('#due_this_quarter').hide();
                $('#shipment_this_quarter').hide();
                $('#invoiced_this_quarter').hide();
                $('#credit_note_this_quarter').hide();

                $('#total_this_week').hide();
                $('#due_this_week').hide();
                $('#shipment_this_week').hide();
                $('#invoiced_this_week').hide();
                $('#credit_note_this_week').hide();

                $('#total_this_month').show();
                $('#due_this_month').show();
                $('#shipment_this_month').show();
                $('#invoiced_this_month').show();
                $('#credit_note_this_month').show();

                if(!result[0]['sum']){
                    $('#total_this_month').empty().append('No Orders');
                }
                else{
                    $('#total_this_month').empty().append(result[3]['symbol'] + ' ' + result[0]['sum']);
                }
                if(!result[2]['due']){
                    $('#due_this_month').empty().append('No Orders');
                }
                else{
                    $('#due_this_month').empty().append(result[3]['symbol'] + ' ' + result[2]['due']);
                }
                $('#shipment_this_month').empty().append(result[4]['shipment']);
                $('#store_count').empty().append(result[5]['store']);
                if(!result[6]['invoiced']){
                    $('#invoiced_this_month').empty().append('No Orders');
                }
                else{
                    $('#invoiced_this_month').empty().append(result[3]['symbol'] + ' ' + result[6]['invoiced']);
                }
                if(!result[7]['credit_note']){
                    $('#credit_note_this_month').empty().append('No Orders');
                }
                else{
                    $('#credit_note_this_month').empty().append(result[3]['symbol'] + ' ' + result[7]['credit_note']);
                }
                $('#customers_count').empty().append(result[8]['customers']);
                $('#product_count').empty().append(result[9]['products']);
            })
        },

        onclick_this_week: function(){
            var self = this;
            rpc.query({
                model: 'magento.dashboard',
                method: 'this_week',
                args: [[]],
            }).then(function (result) {

                $('#total_this_year').hide();
                $('#due_this_year').hide();
                $('#shipment_this_year').hide();
                $('#invoiced_this_year').hide();
                $('#credit_note_this_year').hide();

                $('#total_this_quarter').hide();
                $('#due_this_quarter').hide();
                $('#shipment_this_quarter').hide();
                $('#invoiced_this_quarter').hide();
                $('#credit_note_this_quarter').hide();

                $('#total_this_month').hide();
                $('#due_this_month').hide();
                $('#shipment_this_month').hide();
                $('#invoiced_this_month').hide();
                $('#credit_note_this_month').hide();

                $('#total_this_week').show();
                $('#due_this_week').show();
                $('#shipment_this_week').show();
                $('#invoiced_this_week').show();
                $('#credit_note_this_week').show();

                if(!result[0]['sum']){
                     $('#total_this_week').empty().append('No Orders');
                }
                else{
                    $('#total_this_week').empty().append(result[3]['symbol'] + ' ' + result[0]['sum']);
                }
                if(!result[2]['due']){
                    $('#due_this_week').empty().append('No Orders');
                }
                else{
                    $('#due_this_week').empty().append(result[3]['symbol'] + ' ' + result[2]['due']);
                }
                $('#shipment_this_week').empty().append(result[4]['shipment']);
                if(!result[6]['invoiced']){
                    $('#invoiced_this_week').empty().append('No Orders');
                }
                else{
                    $('#invoiced_this_week').empty().append(result[3]['symbol'] + ' ' + result[6]['invoiced'])
                }
                if(!result[7]['credit_note']){
                    $('#credit_note_this_week').empty().append('No Orders');
                }
                else{
                    $('#credit_note_this_week').empty().append(result[3]['symbol'] + ' ' + result[7]['credit_note'])
                }
            })
        },

        start: function() {
            var self = this;
            this.set("title", 'Magento Dashboard');
            return this._super().then(function() {
                self.update_cp();
                self.onclick_this_month();
                self.render_graphs();
                self.$el.parent().addClass('oe_background_grey');
            });
        },

        render_graphs: function() {
            var self = this;
            self.onclick_sales_today();
            self.annual_growth();
            self.product_pi();
            self.product_ship();
        },

    //Graphs Here

        onclick_sales_today: function(ev) {
            var self = this;
            self.initial_render = true;
            rpc.query({
                model: "magento.dashboard",
                method: "sales_today",
                args: [[]]
            }).then(function(result){

                $('#total_days_7').hide();
                $('#total_today').show();
                $('#total_today').empty().append(result['currency'] + ' ' + result['amt_today']);
                var ctx = document.getElementById("canvas").getContext('2d');
                var date = ['Today'];
                var count = result['count_today'];
                var barColors = [
                        "#1e7145", "#7FFF00", "#DC143C", "#F0F8FF", "#8B008B", "#DAA520",
                        "#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#F5F5DC", "#8A2BE2",
                        "#4B0082"];
                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                            labels: date,//x axis
                            datasets: [{
                                label: 'Count', // Name the series
                                data: count, // Specify the data values array
                                backgroundColor: barColors,
                                barPercentage: 1,
                                barThickness: 6,
                                maxBarThickness: 8,
                                minBarLength: 0,
                                borderWidth: 1, // Specify bar border width
                                type: 'bar', // Set this data to a line chart
                                fill: false
                            }]
                        },
                    options: {
                        scales: {
                            yAxes: [{
                            display: true,
                                ticks: {

                                    beginAtZero: true,
                                    steps: 1,
                                    stepValue: 1,
                                }
                            }]
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            });
        },

        onclick_sales_7: function(ev) {
            var self = this;
            self.initial_render = true;
            rpc.query({
                model: "magento.dashboard",
                method: "sales_7",
                args: [[]]
            }).then(function(result){
                $('#total_today').hide();
                $('#total_days_7').show();
                if(!result['amt_7']){
                    $('#total_days_7').empty().append('No Orders');
                }
                else{
                    $('#total_days_7').empty().append(result['currency'] + ' ' + result['amt_7']);
                }
                var ctx = document.getElementById("canvas").getContext('2d');
                var date = result['days_name'];
                var count = result['count'];
                var barColors = [
                        "#DC143C", "#F0F8FF", "#8B008B", "#DAA520",
                        "#b91d47", "#00aba9", "#2b5797", "#e8c3b9",
                        "#F5F5DC", "#8A2BE2", "#1e7145", "#7FFF00",
                        "#4B0082"];
                myChart.destroy();
                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                            labels: date,//x axis
                            datasets: [{
                                label: 'Count', // Name the series
                                data: count, // Specify the data values array
                                backgroundColor: barColors,
                                barPercentage: 1,
                                barThickness: 6,
                                maxBarThickness: 8,
                                minBarLength: 0,
                                borderWidth: 1, // Specify bar border width
                                type: 'bar', // Set this data to a line chart
                                fill: false
                            }]
                        },
                        options: {
                        scales: {
                            yAxes: [{
                            display: true,
                                ticks: {

                                    beginAtZero: true,
                                    steps: 1,
                                    stepValue: 1,
                                }
                            }]
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            });
        },

        annual_growth: function(ev) {
        self.initial_render = true;
        rpc.query({
                model: "magento.dashboard",
                method: "annual_growth",
                args: [[]]
            }).then(function(result){
                if(!result['total_year']){
                     $('#total_year').empty().append('No Orders');
                }
                else{
                    $('#total_year').empty().append(result['currency'] + ' ' + result['total_year']);
                }
                var ctx = document.getElementById("canvas_line").getContext('2d');
                var months = result['months'];
                var orders = result['orders'];
                var barColors = [
                        "#F5F5DC", "#8A2BE2", "#1e7145", "#7FFF00",
                        "#DC143C", "#F0F8FF", "#8B008B", "#DAA520",
                        "#b91d47", "#00aba9", "#2b5797", "#e8c3b9",
                        "#4B0082"];
                var annual_Chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                            labels: months,//x axis
                            datasets: [{
                                label: 'Count', // Name the series
                                data: orders, // Specify the data values array
                                backgroundColor: barColors,
                                lineTension: 0,
                                borderColor: '#424242',
                                borderWidth: 1, // Specify bar border width
                                type: 'line', // Set this data to a line chart
                                fill: false
                            }]
                        },
                        options: {
                        legend: {display: true},
                        scales: {
                            yAxes: [{
                            display: true,
                                ticks: {

                                    beginAtZero: true,
                                    steps: 1,
                                    stepValue: 1,
                                }
                            }]
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            });
        },

        product_pi: function(ev) {
        self.initial_render = true;
        rpc.query({
                model: "magento.dashboard",
                method: "product_pi",
                args: [[]]
                }).then(function(result){
                    console.log(result)
                var ctx = document.getElementById("canvas_pi").getContext('2d');
                var xValues = result['product_name'];
                var yValues = result['product_count'];
                var barColors = [
                            "#b91d47", "#00aba9", "#2b5797", "#e8c3b9",
                            "#F5F5DC", "#8A2BE2", "#1e7145", "#7FFF00",
                            "#DC143C", "#F0F8FF", "#8B008B", "#DAA520",
                            "#4B0082"];
                var pieChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                            labels: xValues,//x axis
                            datasets: [{
                                label: 'Count', // Name the series
                                data: yValues, // Specify the data values array
                                backgroundColor: barColors,
                            }]
                        },
                        options: {
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                });
            });
        },

        product_ship: function(ev) {
            self.initial_render = true;
            rpc.query({
                model: "magento.dashboard",
                method: "product_ship",
                args: [[]]
            }).then(function(result){
                console.log(result)
                var ctx = document.getElementById("canvas_shipment").getContext('2d');
                var xValues = result['product_name'];
                var yValues = result['product_count'];
                var barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9",
                                 "#F5F5DC", "#8A2BE2","#1e7145", "#7FFF00",
                                 "#DC143C", "#F0F8FF", "#8B008B", "#DAA520",
                                 "#4B0082"];
                var shipment_chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: xValues,
                        datasets: [{
                            backgroundColor: barColors,
                            data: yValues,
                            label: 'Count', // Name the series
                            barPercentage: 1,
                            barThickness: 6,
                            maxBarThickness: 8,
                            minBarLength: 0,
                            borderWidth: 1, // Specify bar border width
                            type: 'bar', // Set this data to a line chart
                            fill: false,
                            }]
                        },
                    options: {
                        scales: {
                            yAxes: [{
                            display: true,
                                ticks: {

                                    beginAtZero: true,
                                    steps: 1,
                                    stepValue: 1,
                                }
                            }]
                        },
                        responsive: true, // Instruct chart js to respond nicely.
                        maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
                    }
                })
            });
        },

        update_cp: function() {
            var self = this;
        },
    });

core.action_registry.add('magento_dashboard_tag', MagentoDashboard);

return MagentoDashboard;

});
