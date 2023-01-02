import logging

from odoo import api, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'payfort':
            return tx

        reference = data.get('reference')
        print('refer', reference)
        tx = self.search([('reference', '=', reference), ('provider', '=', 'payfort')])
        print('tx', tx)
        if not tx:
            raise ValidationError(
                "Payfort: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        super()._process_feedback_data(data)
        if self.provider != "payfort":
            return
        self._set_done()
