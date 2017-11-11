# -*- coding: utf-8 -*-

import vatnumber
import os
import csv
import xmlrpclib

url = 'http://localhost:8069'
db = 'laxas_dev'
username = 'admin'
password = 'Milonga_25'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

csv_path = './'
csv.register_dialect('coma_dialecto', delimiter=',')


def check_vat(vat):
    if vat[:2] == "PT":
        vat_format = vat
        country_id = 185
    elif vat[:2] == "GB":
        vat_format = vat
        country_id = 233
    elif vat[:2] == "ES":
        vat_format = vat
        country_id = 69
    else:
        vat_format = "ES" + vat
        country_id = 69

    if vatnumber.check_vat(vat_format) == False:
        vat_subjected = False
        comment = "NIF: " + vat_format
        vat_format = ""
    else:
        vat_subjected = True
        comment = ""
    return [vat_format, vat_subjected, comment, country_id]


csv_proveedores = open(os.path.abspath(csv_path + 'INVERSIONES proveedores.csv'), 'rb')
reader_proveedores = csv.reader(csv_proveedores, dialect='coma_dialecto')

proveedor_account_ids = models.execute_kw(db, uid, password, 'account.account', 'search', [[['code', '=', "400000"], ['company_id', '=', 4]]])
acreedor_account_ids = models.execute_kw(db, uid, password, 'account.account', 'search', [[['code', '=', "410000"], ['company_id', '=', 4]]])
proveedor_fiscal_position_ids = models.execute_kw(db, uid, password, 'account.fiscal.position', 'search', [[['name','=',"Régimen Nacional"],['company_id','=',4]]])
proveedor_fiscal_position_id = proveedor_fiscal_position_ids[0]

c = 0
for linea_proveedores in reader_proveedores:
    c += 1
    print "INVERSIONES proveedor linea: ", c
    cuenta = linea_proveedores[0]
    nombre = linea_proveedores[1]
    direccion = linea_proveedores[2]
    cp = linea_proveedores[3]
    ciudad = linea_proveedores[4]
    provincia = linea_proveedores[5]
    cif = linea_proveedores[6]
    telefono = linea_proveedores[7]

    proveedor_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['name', '=', nombre], ['company_id', '=', 4]]])
    if proveedor_ids:
        continue

    if cuenta[:2] == "40":
        acc_id = proveedor_account_ids[0]
    elif cuenta[:2] == "41":
        acc_id = acreedor_account_ids[0]

    vat = check_vat(cif)

    proveedor_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
                        'name': nombre,
                        'company_id': 4,
                        'vat_subjected': vat[1],
                        'vat': vat[0],
                        'street': direccion,
                        'city': ciudad,
                        'zip': cp,
                        'phone': telefono,
                        'country_id': vat[3],
                        'supplier': True,
                        'customer': False,
                        'is_company': True,
                        'tz': "Europe/Madrid",
                        'comment': vat[2],
                        }])

    partner_res_id = "res.partner," + str(proveedor_id)
    account_payable_field = "account.account," + str(acc_id)
    models.execute_kw(db, uid, password,\
            'ir.property', 'create', [{
                'name': "property_account_payable",
                'type': "many2one",
                'company_id': 4,
                'fields_id': 2470,
                'value_reference': account_payable_field,
                'res_id': partner_res_id,
                }])
    account_position_field = "account.fiscal.position," + str(proveedor_fiscal_position_id)
    models.execute_kw(db, uid, password,\
            'ir.property', 'create', [{
                'name': "property_account_position",
                'type': "many2one",
                'company_id': 4,
                'fields_id': 2466,
                'value_reference': account_position_field,
                'res_id': partner_res_id,
                }])
