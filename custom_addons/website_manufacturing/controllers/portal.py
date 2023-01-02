from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager


class CustomerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        manufacturing_order = request.env['mrp.production'].search_count([
            ('partner_id', '=', partner.id),
            ('state', '!=', 'cancel')
        ])
        # print("mfo", manufacturing_order)
        if 'mo_count' in counters:
            values['mo_count'] = manufacturing_order
        return values

    def _prepare_mos_domain(self, partner):
        return [
            ('partner_id', '=', partner.id),
            ('state', 'in',
             ['draft', 'confirmed', 'progress', 'to_close', 'done'])
        ]

    # MO Orders

    def _get_mos_searchbar_sortings(self):
        return {
            'date': {'label': _('Order Date'),
                     'order': 'date_planned_start desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

    @http.route('/my/mos', type='http', auth="public", website=True)
    def portal_my_mos(self, page=1, date_begin=None, date_end=None,
                      sortby=None, **kw):

        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        manufacturing_order = request.env['mrp.production'].search([
            ('partner_id', '=', partner.id)
        ])

        domain = self._prepare_mos_domain(partner)

        searchbar_sortings = self._get_mos_searchbar_sortings()

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('date_planned_start', '>', date_begin),
                       ('date_planned_start', '<=', date_end)]

        # count for pager
        mo_count = manufacturing_order.search_count([
            ('partner_id', '=', partner.id)
        ])
        # print("heree", mo_count)
        # make pager
        pager = portal_pager(
            url="/my/mos",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby},
            total=mo_count,
            page=page,
            step=self._items_per_page
        )
        mos = manufacturing_order.search(domain, order=sort_order,
                                         limit=self._items_per_page,
                                         offset=pager['offset'])
        request.session['my_mo_history'] = mos.ids[:100]

        values.update({
            'date': date_begin,
            'mos': mos.sudo(),
            'page_name': 'mo',
            'pager': pager,
            'default_url': '/my/mos',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("website_manufacturing.portal_my_mo", values)

    @http.route('/remove/<id>', type='http', auth="public", website=True)
    def button_remove(self, **kw):
        mo_id = kw.get('id')
        print(mo_id)
        print(kw)
        manufacturing_order = request.env['mrp.production'].search([
            ('id', '=', mo_id)])
        manufacturing_order.state = 'cancel'
        return request.redirect('/my/mos')
