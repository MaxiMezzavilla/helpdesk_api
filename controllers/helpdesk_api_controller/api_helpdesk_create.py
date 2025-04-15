from odoo import http
from odoo.http import request
import json

class HelpdeskApiController(http.Controller):
    @http.route('/api/ticket/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_ticket(self, **kwargs):
        try:
            # Verificamos que todos los parámetros necesarios estén presentes
            if not kwargs.get('name') or not kwargs.get('description') or not kwargs.get('team_id') or not kwargs.get('partner_id'):
                return {"error": "Faltan parámetros obligatorios"}

            # Creamos el ticket con los datos enviados
            ticket_vals = {
                'name': kwargs.get('name'),
                'description': kwargs.get('description'),
                'partner_id': kwargs.get('partner_id')
            }
            ticket = request.env['helpdesk.ticket'].sudo().create(ticket_vals)

            # Retornamos el ID del ticket creado
            return {'ticket_id': ticket.id}

        except Exception as e:
            # En caso de error, retornamos un mensaje de error
            return {'error': str(e)}
