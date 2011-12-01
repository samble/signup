#!/usr/local/bin/python2.6
import sqlite3
import traceback
from time import strftime
from urlparse import parse_qs
from exceptions import Exception

from _include import *
print SQLITE_DB_PATH

HISTORY_FIELDS = ['last_name',
'txn_id',
'receiver_email',
'payment_status',
'reason_code',
'tax',
'payer_status',
'residence_country',
'invoice',
'address_state',
'item_name1',
'txn_type',
'address_street',
'quantity1',
'payment_date',
'first_name',
'mc_shipping',
'item_name',
'item_number1',
'charset',
'parent_txn_id',
'custom',
'notify_version',
'address_name',
'for_auction',
'mc_gross_1',
'test_ipn',
'item_number',
'receiver_id',
'pending_reason',
'business',
'payer_id',
'mc_handling1',
'auction_closing_date',
'mc_handling',
'auction_buyer_id',
'address_zip',
'address_city',
'receipt_ID',
'mc_fee',
'mc_currency',
'shipping',
'verify_sign',
'payer_email',
'payment_type',
'mc_gross',
'mc_shipping1',
'quantity']

INCOMING_FIELDS = HISTORY_FIELDS + ['post_body','history_id']

QUERY_INSERT_HISTORY = 'INSERT INTO IncomingPaypalHistory (' + ','.join(HISTORY_FIELDS) + ') VALUES (' + ','.join([':' + field for field in HISTORY_FIELDS]) + ')'
QUERY_INSERT_INCOMING = 'INSERT INTO IncomingPaypal (' + ','.join(INCOMING_FIELDS) + ') VALUES (' + ','.join([':' + field for field in INCOMING_FIELDS]) + ')'

def handle(environ, start_response):
    try:

        start_response('200 OK', [('Content-Type', 'text/plain')])
        formbody = environ['wsgi.input'].read()
        fields = parse_qs(formbody)

        # Save entire post body for postback verification
        fields['post_body'] = formbody

        # If it's not a test, mark it so manually
        if not 'test_ipn' in fields:
            fields['test_ip'] = 0

        insertPaypalTransaction(fields)

    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

    return []

def insertPaypalTransaction(fieldDict):
    try:
        _fieldDict = fieldDict.copy()

        con = sqlite3.connect(SQLITE_DB_PATH)

        historyParams = dict((field, _fieldDict[field]) for field in HISTORY_FIELDS)
        con.execute(QUERY_INSERT_HISTORY, historyParams)

        id = con.execute('select last_insert_rowid()').fetchone()[0]
        _fieldDict['history_id'] = id

        incomingParams = dict((field, _fieldDict[field]) for field in INCOMING_FIELDS)
        con.execute(QUERY_INSERT_INCOMING, incomingParams)

        con.commit()
        con.close()

    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer
    WSGIServer(handle).run()

