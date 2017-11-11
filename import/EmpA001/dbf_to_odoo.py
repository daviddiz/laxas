#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTACION DE CLIENTES DESDE SubCta.dbf en 2013/EmpAF

import dbf
# import vatnumber
import os
# import csv

#ruta_contaplus = os.path.abspath('/home/ddiz/workspace/Laxas/import/EmpA001')

file_SubctaA001 = os.path.abspath('/home/ddiz/workspace/Laxas/import/EmpA001/Subcta.dbf')

#print dbf.code_pages

table_SubctaA001 = dbf.Table(file_SubctaA001, codepage='cp437')
#print table_SubctaA001
#print table_SubctaA001.codepage
table_SubctaA001.open()
#print table_SubctaA001
#print table_SubctaA001.codepage
#print dir(table_SubctaA001)
fields = table_SubctaA001.field_names
for field in fields:
    print field
#dbf.export(table_SubctaA001, r'sdv.csv', header = True)
#dbf.export(table_SubctaA001, header = True)
#print "fin"

#cl = 0

for record in table_SubctaA001:
    #dbf.export(table, dbf_file)
    print record
#      tipo_cuenta = str(record['COD'])[:3]
#     if tipo_cuenta == "430":
#         cl = _import_record_clientes(tipo_cuenta, cl, record)
#
# table_SubctaA001.close()
