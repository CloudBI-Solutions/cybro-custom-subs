odoo.define('dashboard_extension.custom', function(require) {
    'use strict';
    var ks_website_dashboard = require('ks_website_dashboard_ninja.ks_website_dashboard');
    var ajax = require('web.ajax');

    ks_website_dashboard.include({
        start: function(dashboard_id, data_selection, ks_self_received) {
            var ks_self = this;
            if (dashboard_id == undefined) {
                if($('#dashboard_id').length > 0){
                    dashboard_id = parseInt($('#dashboard_id').val());
                }
                else{
                    dashboard_id = 0;
                }
            }
            if (data_selection == undefined) {
                ks_self.data_selection = 'user_data';
            } else {
                ks_self.data_selection = data_selection;
            }
            if (ks_self_received !== undefined) {
                ks_self.ks_self_received = ks_self_received;
                ks_self.$el = ks_self_received.$el;
                ks_self.$target = ks_self_received.$target;
                ks_self.$target.attr('data-id', dashboard_id);
                ks_self.$target.attr('data-selection', data_selection);
                ks_self.$overlay = ks_self_received.$overlay;
                ks_self.data = ks_self_received.data;
                this.$el = ks_self_received.$target;
                this.$target = ks_self_received.$target;
                this.$overlay = ks_self_received.$overlay;
            }
            Chart.plugins.unregister(ChartDataLabels);
            ks_self.ks_set_default_chart_view();
            if($('#dashboard_id').length > 0){
                var dashboard_id = parseInt($('#dashboard_id').val());
            }
            else{
                var dashboard_id = 0;
            }
            $.when(ks_self.ks_fetch_data()).then(function(result) {
                if(result){
                    $.when(ks_self.ks_fetch_items_data()).then(function(result) {
                        var $target = ks_self.$target;
                        ks_self.ks_set_update_interval();
                        ks_self.ksRenderDashboard($target, dashboard_id);
                    });
                }
            });
        },
        ks_fetch_data: function() {
            var ks_self = this;
            if($('#dashboard_id').length > 0){
                ks_self.dashboard_id = parseInt($('#dashboard_id').val());
            }
            else{
                ks_self.dashboard_id = ks_self.$target.attr('data-id');;
            }
            return ajax.jsonRpc('/dashboard/data', 'call', {
                model: 'ks_dashboard_ninja.items',
                method: 'ks_dashboard_data_handler',
                args: [],
                kwargs: {
                    'id': Number(ks_self.dashboard_id),
                    'type': ks_self.data_selection,
                },
                context: ks_self.getContext(),
            }).then(function(data) {
                if (data !== "missingerror") {
                    if(! data.login){
                        ks_self.$el = ks_self.$target.empty();
                        if(data.type === 'user_data') {
                            $(QWeb.render('ksWebsiteNoItemNoUserView')).appendTo(ks_self.$el);
                            $('.ks_dashboard_header').addClass('ks_hide');
                            return false;
                        }
                        else if(data.type === 'all_data') {
                            ks_self.config = data;
                            return true;
                        }
                    }
                    else {
                        ks_self.config = data;
                        return true;
                    }
                }
            }.bind(ks_self));
        },

    });
});