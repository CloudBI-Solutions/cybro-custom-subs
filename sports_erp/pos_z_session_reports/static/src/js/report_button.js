odoo.define('pos_z_session_reports.ReportButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    const { useState, useRef, useContext, useExternalListener } = owl.hooks;


    class ReportButton extends PosComponent {
        constructor() {
            super(...arguments);
            this.state = useState({
                selected_value: ''
            });
            useListener('click', this._onClick);
        }
        async _onClick() {
            var session = this.env.pos.pos_session.id;
            var session_summary = await this.rpc({
				model: 'pos.session',
				method: 'get_order_summary',
				args: [this.env.pos.pos_session.id, session],
				});
            this.showScreen('SessionSummaryReceiptScreen', { session_summary: session_summary});
        }
    }
    ReportButton.template = 'pos_z_session_reports.ReportButton';

    ProductScreen.addControlButton({
        component: ReportButton,
        condition: function () {
            return this.env.pos.config.session_report;
        },
    });

    Registries.Component.add(ReportButton);

    return ReportButton;
});
