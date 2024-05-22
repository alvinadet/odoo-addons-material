# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo.http import request,Response
from werkzeug.exceptions import NotFound, BadRequest

ENDPOINT = '/api/material'


class Material(http.Controller):

    @http.route('/api/material/<int:id>', auth='public', methods=['DELETE'], csrf=False,type='json')
    def delete_material(self, id):
        material = request.env['material.material'].sudo().browse(id)
        if not material:
            return {'code': 404, 'message': 'Material not found'}
        material.unlink()
        return {'code': 200, 'message': 'Material deleted successfully'}



    @http.route(ENDPOINT + '/<int:id>', auth='public', methods=['PUT'], csrf=False, type='json')
    def update_material(self, id):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            material_type = data.get('material_type')
            buy_price = data.get('buy_price')
            supplier_id = data.get('supplier_id')
            code = data.get('code')

          

            # Validate required fields
            if not name or not material_type or not buy_price or not supplier_id or not code:
                raise BadRequest('Missing required fields')

            if material_type not in ['Fabric', 'Jeans', 'Cotton']:
                raise BadRequest('Invalid material type')

            material = request.env['material.material'].sudo().browse(id)
            
            if not material:
                raise NotFound('Material not found')

            if buy_price < 100 :
                raise BadRequest('Buy price less than 100')

            material.write({
                'name': name,
                'material_type': material_type,
                'buy_price': buy_price,
                'supplier_id': supplier_id,
                'code': code
            })

            

            res = {"code": 201, "message": "Material updated successfully" }
            return res

        except ValueError:
            return Response(json.dumps({'error': 'Invalid JSON body'}), status=400, content_type='application/json')


    @http.route(ENDPOINT, auth='public', methods=['GET'], csrf=False,type='http')
    def get_materials(self, material_type=None, **kwargs):
        materials = http.request.env['material.material'].sudo()._list_material(material_type=material_type)
        return Response(json.dumps(materials), content_type='application/json')

    @http.route(ENDPOINT + '/supplier', auth='public', methods=['GET'], csrf=False)
    def get_suppliers(self, **kwargs):
        suppliers = http.request.env['res.partner'].sudo().search([])
        data = []
        for supplier in suppliers:
            data.append({
                'id': supplier.id,
                'name': supplier.name,
                'email': supplier.email,
                'phone': supplier.phone,
                # Add more fields as needed
            })
        return Response(json.dumps(data), content_type='application/json')

    @http.route(ENDPOINT, auth='public', methods=['POST'], csrf=False, type='json')
    def create_material(self):
        try:
            data = json.loads(request.httprequest.data)
            name = data.get('name')
            material_type = data.get('material_type')
            buy_price = data.get('buy_price')
            supplier_id = data.get('supplier_id')
            code = data.get('code')

            

            # Validate required fields
            if not name or not material_type or not buy_price or not supplier_id or not code:
                raise BadRequest('Missing required fields')

            if material_type not in ['Fabric', 'Jeans', 'Cotton']:
                raise BadRequest ('Invalid material type')

            if buy_price < 100 :
                raise BadRequest('buy price less than 100')
           
            request.env['material.material'].sudo().create({
                'name': name,
                'material_type': material_type,
                'buy_price': buy_price,
                'supplier_id': supplier_id,
                'code': code
            })

            return {'code': 201, 'message': 'Material created successfully'}

        
        except ValueError:
            
            return Response(json.dumps({'error': 'Invalid JSON body'}), status=400, content_type='application/json')
