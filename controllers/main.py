import json

from odoo import http
from odoo.http import request


class HelpdeskApiController(http.Controller):
    @http.route('/api/helpdesk/create_ticket', type='http', auth='public', methods=['POST'], csrf=False)
    def create_helpdesk_ticket(self):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            name = data.get('name')
            description = data.get('description')
            team_id = data.get('team_id')  # Opcional: ID del equipo de Helpdesk
            partner_id = data.get('partner_id') # Opcional: ID del cliente

            if not name or not description:
                return request.make_response(json.dumps({'error': 'Faltan los campos obligatorios: name y description'}), headers=[('Content-Type', 'application/json')])

            ticket_data = {
                'name': name,
                'description': description,
            }
            if team_id:
                ticket_data['team_id'] = team_id
            if partner_id:
                ticket_data['partner_id'] = partner_id

            new_ticket = request.env['helpdesk.ticket'].sudo().create(ticket_data)

            return request.make_response(json.dumps({'success': True, 'ticket_id': new_ticket.id}), headers=[('Content-Type', 'application/json')])

        except json.JSONDecodeError:
            return request.make_response(json.dumps({'error': 'Datos JSON inválidos'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'error': str(e)}), headers=[('Content-Type', 'application/json')])
