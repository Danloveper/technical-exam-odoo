from odoo import _, api, fields, models

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    def action_create_payments(self):

        super(AccountPaymentRegister, self).action_create_payments()

        return self.partner_id._cron_calculate_payment_behavior()