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
    if vat[:2] == "ES":
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

csv_clientes = open(os.path.abspath(csv_path + 'PROMOCIONES clientes_mod.csv'), 'rb')
reader_clientes = csv.reader(csv_clientes, dialect='coma_dialecto')

c = 0
for linea_clientes in reader_clientes:
    c += 1
    print "PROMOCIONES cliente linea: ", c
    cuenta = linea_clientes[0]
    nombre = linea_clientes[1]
    direccion = linea_clientes[2]
    cp = linea_clientes[3]
    ciudad = linea_clientes[4]
    provincia = linea_clientes[5]
    cif = linea_clientes[6]
    telefono = linea_clientes[7]

    cliente_account_ids = models.execute_kw(db, uid, password,'account.account', 'search', [[['code','=',"430000"],['company_id','=',1]]])
    acc_id = cliente_account_ids[0]

    proveedor_fiscal_position_ids = models.execute_kw(db, uid, password, 'account.fiscal.position', 'search', [[['name','=',"Régimen Nacional"],['company_id','=',1]]])
    acc_fiscal_position = proveedor_fiscal_position_ids[0]

    vat = check_vat(linea_clientes[6])

    if linea_clientes[2]:
        direccion = linea_clientes[2]
    else:
        direccion = ""
    if linea_clientes[4]:
        ciudad = linea_clientes[4]
    else:
        ciudad = ""
    if linea_clientes[3]:
        cp = linea_clientes[3]
    else:
        cp = ""

    cliente_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['name','=',linea_clientes[1]],['company_id','=',1]]])
    if cliente_ids:
        cliente_cliente_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['name','=',linea_clientes[1]],['company_id','=',1],['customer','=',True]]])
        if cliente_cliente_ids:
            continue
        cliente_id = cliente_ids[0]
        models.execute_kw(db, uid, password,\
                'res.partner', 'write', [[cliente_id], {
                    'street': direccion,
                    'city': ciudad,
                    'zip': cp,
                    'phone': telefono,
                    'vat': vat[0],
                    'company_id': 1,
                    'country_id': 69,
                    'customer': True,
                    'tz': "Europe/Madrid",
                    'is_company': True,
                    }])
        partner_res_id = "res.partner," + str(cliente_id)
        account_receivable_field = "account.account," + str(acc_id)
        models.execute_kw(db, uid, password,\
                'ir.property', 'create', [{
                    'name': "property_account_receivable",
                    'type': "many2one",
                    'company_id': 1,
                    'fields_id': 2478,
                    'value_reference': account_receivable_field,
                    'res_id': partner_res_id,
                    }])
    else:
        cliente_id = models.execute_kw(db, uid, password,\
                'res.partner', 'create', [{
                    'name': linea_clientes[1],
                    'street': direccion,
                    'city': ciudad,
                    'zip': cp,
                    'phone': telefono,
                    'vat': vat[0],
                    'company_id': 1,
                    'country_id': 69,
                    'customer': True,
                    'tz': "Europe/Madrid",
                    'is_company': True,
                    }])
        partner_res_id = "res.partner," + str(cliente_id)
        account_receivable_field = "account.account," + str(acc_id)
        account_position_field = "account.fiscal.position," + str(acc_fiscal_position)
        models.execute_kw(db, uid, password,\
                'ir.property', 'create', [{
                    'name': "property_account_receivable",
                    'type': "many2one",
                    'company_id': 1,
                    'fields_id': 2478,
                    'value_reference': account_receivable_field,
                    'res_id': partner_res_id,
                    }])
        models.execute_kw(db, uid, password,\
                'ir.property', 'create', [{
                    'name': "property_account_position",
                    'type': "many2one",
                    'company_id': 1,
                    'fields_id': 2466,
                    'value_reference': account_position_field,
                    'res_id': partner_res_id,
                    }])
