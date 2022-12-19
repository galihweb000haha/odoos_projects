# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        # return http.request.render('academy.index', {
        #     'contacts': ["Galih", "Khaepah", "Lester Vaughn"],
        # })
        Contacts = http.request.env['academy.contacts']

        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(request.env['ir.config_parameter'].sudo().get_param('web.base.url'))

        return http.request.render('academy.index', {
            'base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            'contacts': Contacts.search([])
        })

    
    @http.route('/academy/detail/<id>', auth='public', website=True)
    def detail(self, id):
      
        print("?>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>2")
        return request.render('academy.detail', {
            'base_url': request.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            'contacts': request.env['academy.contacts'].search([('id', '=', id)]),
        })

    @http.route('/academy/langsung', auth='public', website=True)
    def langsung(self):
        return {
            'ng': 'ngek',
            'ngo': 'ngok'
        }