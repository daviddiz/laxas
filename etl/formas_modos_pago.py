# -*- coding: utf-8 -*-

import vatnumber
import os
import csv
import xmlrpclib
from datetime import datetime

url = 'http://localhost:8069'
db = 'laxas_dev'
username = 'admin'
password = 'Milonga_25'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

# CREAR CUENTAS BANCARIAS DE CADA COMPAÑÍA ANTES DE LANZAR ESTE SCRIPT

#creo los plazos de pago si no existen
if not models.execute_kw(db, uid, password,'account.payment.term', 'search', [[['name','=',"85 DIAS"]]]):
    payment_term_id = models.execute_kw(db, uid, password,'account.payment.term', 'create', [{'name': "85 DIAS",'note': "85 DIAS",'active': True,}])
    payment_term_line_id = models.execute_kw(db, uid, password,'account.payment.term.line', 'create', [{'payment_id': payment_term_id,'days2': 0,'days': 85,'value':"balance"}])

#creo los modos de pago

#PROMOCIONES
cash_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"cash"],['company_id','=',1]]])
bank_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"bank"],['company_id','=',1]]])
res_partner_bank_ids = models.execute_kw(db, uid, password,'res.partner.bank', 'search', [[['company_id','=',1]]])

if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CONTADO"],['company_id','=',1]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CONTADO",'journal': cash_journal_ids[0],'company_id': 1,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"RECIBO"],['company_id','=',1]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "RECIBO",'journal': bank_journal_ids[1],'company_id': 1,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"TR.BANCARI"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "TR.BANCARI",'journal': bank_journal_ids[1],'company_id': 1,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CHEQUE"],['company_id','=',1]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CHEQUE",'journal': bank_journal_ids[1],'company_id': 1,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"PAGARE"],['company_id','=',1]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "PAGARE",'journal': bank_journal_ids[1],'company_id': 1,'bank_id': res_partner_bank_ids[0],'type': 1,}])

#GRUPO
cash_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"cash"],['company_id','=',3]]])
bank_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"bank"],['company_id','=',3]]])
res_partner_bank_ids = models.execute_kw(db, uid, password,'res.partner.bank', 'search', [[['company_id','=',3]]])

if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CONTADO"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CONTADO",'journal': cash_journal_ids[0],'company_id': 3,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"RECIBO"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "RECIBO",'journal': bank_journal_ids[1],'company_id': 3,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"TR.BANCARI"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "TR.BANCARI",'journal': bank_journal_ids[1],'company_id': 3,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CHEQUE"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CHEQUE",'journal': bank_journal_ids[1],'company_id': 3,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"PAGARE"],['company_id','=',3]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "PAGARE",'journal': bank_journal_ids[1],'company_id': 3,'bank_id': res_partner_bank_ids[0],'type': 1,}])

#INVERSIONES
cash_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"cash"],['company_id','=',4]]])
bank_journal_ids = models.execute_kw(db, uid, password,'account.journal', 'search', [[['type','=',"bank"],['company_id','=',4]]])
res_partner_bank_ids = models.execute_kw(db, uid, password,'res.partner.bank', 'search', [[['company_id','=',4]]])

if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CONTADO"],['company_id','=',4]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CONTADO",'journal': cash_journal_ids[0],'company_id': 4,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"RECIBO"],['company_id','=',4]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "RECIBO",'journal': bank_journal_ids[1],'company_id': 4,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"TR.BANCARI"],['company_id','=',4]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "TR.BANCARI",'journal': bank_journal_ids[1],'company_id': 4,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"CHEQUE"],['company_id','=',4]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "CHEQUE",'journal': bank_journal_ids[1],'company_id': 4,'bank_id': res_partner_bank_ids[0],'type': 1,}])
if not models.execute_kw(db, uid, password,'payment.mode', 'search', [[['name','=',"PAGARE"],['company_id','=',4]]]):
    payment_mode_id = models.execute_kw(db, uid, password,'payment.mode', 'create', [{'name': "PAGARE",'journal': bank_journal_ids[1],'company_id': 4,'bank_id': res_partner_bank_ids[0],'type': 1,}])
