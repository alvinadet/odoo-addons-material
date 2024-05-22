# -*- coding: utf-8 -*-

from odoo import models, fields, api


class material(models.Model):
    _name = 'material.material'
    _description = 'material.material'
    

    code = fields.Char()
    name = fields.Char()
    material_type = fields.Selection([
        ('Fabric', 'Fabric'),
        ('Jeans', 'Jeans'),
        ('Cotton', 'Cotton'),
    ], default='Fabric')
    buy_price = fields.Float()
    supplier_id = fields.Many2one('res.partner')



    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.buy_price = float(record.buy_price) / 100
            record.code = record.code
            record.name = record.name
            record.type = record.type
            record.supplier_id = record.supplier_id
    
    def _list_material(self, material_type=None):
        domain = []
        if material_type:
            domain.append(('material_type', '=', material_type))
        materials = self.env['material.material'].search(domain)
        
        data = []
        for material in materials:
            supplier = None
        
            if material.supplier_id:
                supplier = {
                    'id': material.supplier_id.id,
                    'name': material.supplier_id.name,
                    'email': material.supplier_id.email,
                    'phone': material.supplier_id.phone,
                }
           
            data.append({
                'id': material.id,
                'name': material.name,
                'material_type': material.material_type,
                'buy_price': material.buy_price,
                'code': material.code,
                'supplier': supplier 
            })
        return data
