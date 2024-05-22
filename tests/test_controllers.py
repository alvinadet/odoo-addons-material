import json
from urllib.request import Request, urlopen
from odoo.tests.common import HttpCase


class TestMaterialController(HttpCase):

    def test_delete_material(self):
        # Create a material
        material = self.env['material.material'].create({
            'name': 'Test Material',
            'material_type': 'Fabric',
            'buy_price': 150,
            'supplier_id': 1,
            'code': 'TEST001'
        })

        # Send a DELETE request to delete the material
        
        
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/material/' + str(material.id)
        req = Request(method='DELETE', url=url, data=json.dumps({}).encode(), headers={'Content-Type': 'application/json'})
        response = urlopen(req)

        res = json.loads(response.read().decode('utf-8'))
        
        self.assertEqual(res.get('result'), {'code': 200, 'message': 'Material deleted successfully'})
        # Check the response

    def test_update_material(self):
        # Create a material
        material = self.env['material.material'].create({
            'name': 'FOO Material',
            'material_type': 'Fabric',
            'buy_price': 150,
            'supplier_id': 1,
            'code': 'TEST001'
        })

        # Send a PUT request to update the material
        data = {
            'name': 'Updated Material',
            'material_type': 'Jeans',
            'buy_price': 200,
            'supplier_id': 1,
            'code': 'TEST002'
        }
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/material/' + str(material.id)

        req = Request(method='PUT', url=url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
        response = urlopen(req)

        res = json.loads(response.read().decode('utf-8'))

        # Check the response
        self.assertEqual(res.get('result'), {"code": 201, "message": "Material updated successfully"})

        # Check if the material is updated in the database
        updated_material = self.env['material.material'].browse(material.id)
        self.assertEqual(updated_material.name, 'Updated Material')
        self.assertEqual(updated_material.material_type, 'Jeans')
        self.assertEqual(updated_material.buy_price, 200)
        self.assertEqual(updated_material.supplier_id, 2)
        self.assertEqual(updated_material.code, 'TEST002')

    def test_get_materials(self):
        # Create some materials
        material1 = self.env['material.material'].create({
            'name': 'Material 1',
            'material_type': 'Fabric',
            'buy_price': 150,
            'supplier_id': 1,
            'code': 'TEST001'
        })
        material2 = self.env['material.material'].create({
            'name': 'Material 2',
            'material_type': 'Jeans',
            'buy_price': 200,
            'supplier_id': 2,
            'code': 'TEST002'
        })

        # Send a GET request to get the materials
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/material'
        req = Request(method='GET', url=url)
        response = urlopen(req)
        res = json.loads(response.read().decode('utf-8'))


        # Check the response
        self.assertEqual(len(res), 2)

    def test_create_material(self):
        # Send a POST request to create a material
        data = {
            'name': 'New Material',
            'material_type': 'Cotton',
            'buy_price': 180,
            'supplier_id': 3,
            'code': 'TEST003'
        }
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/api/material'

        req = Request(method='POST', url=url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
        response = urlopen(req)


        res = json.loads(response.read().decode('utf-8'))
        
        # Check the response
        self.assertEqual(res.get('result'), {"code": 201, "message": "Material created successfully"})

        # Check if the material is created in the database
        created_material = self.env['material.material'].search([('name', '=', 'New Material')])
        self.assertEqual(len(created_material), 1)
        self.assertEqual(created_material.name, 'New Material')
        self.assertEqual(created_material.material_type, 'Cotton')
        self.assertEqual(created_material.buy_price, 180)
        self.assertEqual(created_material.supplier_id.id, 3)
        self.assertEqual(created_material.code, 'TEST003')