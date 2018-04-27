# coding: utf-8
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from openerp.osv import osv, fields


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def onchange_quantity(self, cr, uid, ids, product_id, product_qty, product_uom, product_uos):
        warning = {}

        # Warn if the quantity was increased
        if ids:
            for move in self.read(cr, uid, ids, ['product_qty', 'picking_id', 'purchase_line_id']):

				purchase_product_qty = self.pool.get('purchase.order.line').browse(cr, uid, move['purchase_line_id'], context=context).product_qty

                if (product_qty > move['product_qty']) and (move['picking_id']) and (move['purchase_line_id']) and (product_qty > purchase_product_qty):
                    warning.update({
                        'title': ('Información'),
                        'message': ("No puede recibir más cantidad de la existente en el pedido.")})
                break

		if warning == {}:
			res = super(stock_move, self).onchange_quantity(cr, uid, ids, product_id, product_qty, product_uom, product_uos)
			return res
		else:
	        return {'warning': warning}

