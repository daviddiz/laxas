# -*- coding: utf-8 -*-
##############################################################################
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# from openerp import models, fields, api, _
# from openerp.exceptions import RedirectWarning
# 
# 
# class AccountInvoice(models.Model):
#     _inherit = "account.invoice"
# 
#     @api.onchange('supplier_invoice_number')
#     def onchange_supplier_invoice_number(self):
#         if self.type == 'in_invoice' and self.partner_id and \
#             self.supplier_invoice_number:
#             same_inv_num_sup_c = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('type', '=', 'in_invoice'),
#                 ('supplier_invoice_number', '=ilike', \
#                     self.supplier_invoice_number)
#                 ])
#             id_original = [self._origin.id]
#             same_inv_num_sup_c_ids = [c.id for c in same_inv_num_sup_c]
#             if same_inv_num_sup_c and same_inv_num_sup_c_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message':
#         _('Ya existe una factura con igual referencia para este proveedor.')
#                     }
#                 }
#                 return res
# 
#     @api.onchange('partner_id')
#     @api.depends('type', 'date_invoice', 'payment_term', 'partner_bank_id', 'company_id')
#     def onchange_partner_id(self):
#         orig_result = super(AccountInvoice, self).onchange_partner_id(self.type,
#             self.partner_id.id,
#             self.date_invoice or False,
#             self.payment_term.id or False,
#             self.partner_bank_id.id or False,
#             self.company_id.id or False)
# 
#         if type(orig_result) is dict and orig_result.has_key('value'):
#             for field, value in orig_result.get('value').items():
#                 if hasattr(self, field):
#                     setattr(self, field, value)
# 
#         if self.supplier_invoice_number and self.partner_id:
#             same_inv_num_sup_c = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('type', '=', 'in_invoice'),
#                 ('supplier_invoice_number', '=ilike', \
#                     self.supplier_invoice_number)
#                 ])
#             id_original = [self._origin.id]
#             same_inv_num_sup_c_ids = [c.id for c in same_inv_num_sup_c]
#             if same_inv_num_sup_c and same_inv_num_sup_c_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message': _('''Ya existe una factura con igual referencia
#                                  para este proveedor.''')
#                     }
#                 }
#                 return res
# 
# 
# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"
# 
#     @api.onchange('partner_id')
#     def onchange_partner_id(self):
#         orig_result = super(PurchaseOrder, self).onchange_partner_id(self.partner_id.id)
# 
#         if type(orig_result) is dict and orig_result.has_key('value'):
#             for field, value in orig_result.get('value').items():
#                 if hasattr(self, field):
#                     setattr(self, field, value)
# 
#         if self.partner_ref and self.partner_id:
#             same_purchase_order_num = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('partner_ref', '=ilike', self.partner_ref)
#                 ])
#             id_original = [self._origin.id]
#             same_purchase_order_num_ids = \
#                 [c.id for c in same_purchase_order_num]
#             if same_purchase_order_num and \
#                 same_purchase_order_num_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message': _('''Ya existe un pedido con igual
#                             referencia para este proveedor.''')
#                     }
#                 }
#                 return res
# 
#     @api.onchange('partner_ref')
#     def onchange_partner_ref(self):
#         if self.partner_ref and self.partner_id:
#             same_purchase_order_num = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('partner_ref', '=ilike', self.partner_ref)
#                 ])
#             id_original = [self._origin.id]
#             same_purchase_order_num_ids = \
#                 [c.id for c in same_purchase_order_num]
#             if same_purchase_order_num and \
#                 same_purchase_order_num_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message': _('''Ya existe un pedido con igual referencia
#                                  para este proveedor.''')
#                     }
#                 }
#                 return res
# 
# 
# class StockPicking(models.Model):
#     _inherit = "stock.picking"
# 
#     @api.model
#     def _default_client_order_ref(self):
#         if self.group_id:
#             sale_obj = self.env['sale.order']
#             self.client_order_ref = ''
#             cond = [('procurement_group_id', '=', self.group_id.id)]
#             sale = sale_obj.search(cond, limit=1)
#             self.client_order_ref = sale.client_order_ref
# 
#     @api.onchange('partner_id')
#     def onchange_partner_id(self):
#         if self.client_order_ref and self.partner_id:
#             same_picking_num = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('client_order_ref', '=ilike', self.client_order_ref)
#                 ])
#             id_original = [self._origin.id]
#             same_picking_num_ids = \
#                 [c.id for c in same_picking_num]
#             if same_picking_num and \
#                 same_picking_num_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message': _('''Ya existe un albarán con igual referencia
#                                  para este proveedor.''')
#                     }
#                 }
#                 return res
# 
#     @api.onchange('client_order_ref')
#     def onchange_client_order_ref(self):
#         if self.client_order_ref and self.partner_id:
#             same_picking_num = self.search([
#                 ('partner_id', '=', self.partner_id.id),
#                 ('client_order_ref', '=ilike', self.client_order_ref)
#                 ])
#             id_original = [self._origin.id]
#             same_picking_num_ids = \
#                 [c.id for c in same_picking_num]
#             if same_picking_num and \
#                 same_picking_num_ids != id_original:
#                 res = {'warning': {
#                     'title': _('Warning'),
#                     'message': _('''Ya existe un albarán con igual referencia
#                                  para este proveedor.''')
#                     }
#                 }
#                 return res
# 
#     client_order_ref = fields.Char(
#         string="Sale Reference/Description",
#         default=_default_client_order_ref)
