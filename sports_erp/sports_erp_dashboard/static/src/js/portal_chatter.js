odoo.define('sports_erp_dashboard.portal.chatter', function (require) {
'use strict';

var core = require('web.core');
var portalChatter = require('portal.chatter');
var utils = require('web.utils');
var time = require('web.time');

var _t = core._t;
var PortalChatter = portalChatter.PortalChatter;
var qweb = core.qweb;

PortalChatter.include({
    xmlDependencies: (PortalChatter.prototype.xmlDependencies || [])
        .concat([
            '/sports_erp_dashboard/static/src/xml/portal_chatter.xml'
                ]),

        });
    });
