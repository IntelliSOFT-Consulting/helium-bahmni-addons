# In your_custom_module/controllers/api_controller.py

from odoo import http
from odoo.http import request
import json


class ApiController(http.Controller):

    @http.route('/api/wallet/info', type='http', auth="public", methods=['GET'], website=True)
    def get_info(self, **kwargs):
        try:
            patient_id = kwargs.get('patient')
            if patient_id:
                customer = request.env['res.partner'].search(
                    [('ref', '=', patient_id)], limit=1)
                if not customer:
                    return json.dumps({'error': 'Not found'})
                wallet_id = None
                if len(customer.wallet) > 0:
                    wallet_id = customer.wallet[0]
                # if not wallet create it
                if not wallet_id:
                    wallet_id = request.env['customer.wallet'].create({
                        "customer": customer.id,
                        "balance": 0
                    })
                return json.dumps({"balance": wallet_id.balance})
            return json.dumps({'error': 'Not found'})
        except Exception as e:
            return json.dumps({'error': str(e)})
