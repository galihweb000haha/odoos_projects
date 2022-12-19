from operator import itemgetter
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo import http, _
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self):
        """
        perpare the values or data to be passing to the portal home
        """
        # get values from old function or parent method
        values = super(CustomerPortal, self)._prepare_home_portal_values()

        # get invoice count with (serach_count: return number of record)
        to_invoice_count = request.env['sale.order'].search_count([('invoice_status', '=', 'to invoice')]) \
            if request.env['sale.order'].check_access_rights(
            'read', raise_exception=False) else 0

        # update the dictionary to add the to_invoice count
        values.update({
            'to_invoice_count': to_invoice_count
        })

        return values

    @http.route(['/my/to_invoice', '/my/to_invoice/page/<int:page>'], type='http', auth="user", website=True)
    def get_orders_to_invoice(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """
        this function will render new template that will contain records of sale order where state is to invoice
        """
        SaleOrder = request.env['sale.order']

        # set the domain (where in sql)
        domain = [
            ('invoice_status', '=', 'to invoice')
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        to_invoice_count = SaleOrder.search_count(domain)

        pager = portal_pager(
            url="my/to_invoice",
            url_args={'date_begin': date_begin, 'date_end':date_end,'sortby':sortby},
            total=to_invoice_count,
            page=page,
            step=self._items_per_page
        )
        
        orders_to_invoice = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values = {
            'to_invoices' : orders_to_invoice,
            'page_name': 'to_invoice',
            'default_url': '/my/to_invoice',
            'sortby' : sortby,
            'searchbar_sortings': searchbar_sortings,
            'pager': pager,
            'date': date_begin,
            'date_end': date_end
        }
        
        return request.render('website_portal.portal_my_orders_to_invoice', values)

    @http.route(['/my/orders', '/my/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None, sortby=None, groupby='partner_id', filterby=None, search=None, search_in='content', **kw):
        """
        Add some search method such as sort by, filter by and group by
        """
        values = super(CustomerPortal, self).portal_my_orders(page=page, date_begin=date_begin, date_end=date_end, sortby=sortby, groupby='partner_id',  filterby=filterby, search=search, search_in='content')
        SaleOrder = request.env['sale.order']
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'partner_id': {'input': 'partner_id', 'label': _('Partner Id')}
        }

        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        sale_order = SaleOrder.search([])
        for so in sale_order:
            searchbar_filters.update({
                str(so.partner_id.id): {'label': so.partner_id.name, 'domain': [('partner_id', '=', so.partner_id.id)]}
            })
        
        sale_order_groups = SaleOrder.read_group([], fields=['partner_id','user_id'], groupby=['partner_id','user_id'],lazy=False)

        for group in sale_order_groups:
            partner_id = group['partner_id'][0] if group['partner_id'] else False
            sale_order_name = group['partner_id'][1] if group['partner_id'] else _('Others')
            searchbar_filters.update({
                str(partner_id): {'label': sale_order_name, 'domain': [('partner_id', '=', partner_id)]}
            })

        if not filterby:
            filterby = 'all'

        domain = searchbar_filters.get(filterby, searchbar_filters.get(str(filterby)))['domain']

        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('name', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain += search_domain
        
        sale_order_count = SaleOrder.search_count(domain)

        pager = portal_pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,'filterby': filterby,'search_in': search_in,'search': search},
            total=sale_order_count,
            page=page,
            step=self._items_per_page
        )

        orders = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_orders_history'] = orders.ids[:100]

        if groupby == 'partner_id':
            grouped_sale_order = [SaleOrder.concat(*g) for k, g in groupbyelem(orders, itemgetter('partner_id'))]
        else:
            grouped_sale_order = [orders]
        
        values.qcontext.update({
            'searchbar_groupby': searchbar_groupby,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs' : searchbar_inputs,
            'pager': pager,
            'orders': orders,
            'grouped_sale_order': grouped_sale_order,
            'groupby': groupby,
            'filterby': filterby,
            'search_in': search_in,
            'sortby': sortby,
        })
    
        return values