#!/usr/local/bin/python2.6

from _include import *
from sys import exit
import sqlite3

if not __name__ == 'main':
   exit(0) 

QUERY_GET_INCOMING = '''SELECT
id,
last_name,
txn_id,
receiver_email,
payment_status,
reason_code,
tax,
payer_status,
residence_country,
invoice,
address_state,
item_name1,
txn_type,
address_street,
quantity1,
payment_date,
first_name,
mc_shipping,
item_name,
item_number1,
charset,
parent_txn_id,
custom,
notify_version,
address_name,
for_auction,
mc_gross_1,
test_ipn,
item_number,
receiver_id,
pending_reason,
business,
payer_id,
mc_handling1,
auction_closing_date,
mc_handling,
auction_buyer_id,
address_zip,
address_city,
receipt_ID,
mc_fee,
mc_currency,
shipping,
verify_sign,
payer_email,
payment_type,
mc_gross,
mc_shipping1,
quantity
FROM IncomingPaypal
WHERE id = (SELECT MIN(id) FROM IncomingPaypal)
'''

QUERY_DELETE_INCOMING = 'DELETE FROM IncomingPaypal WHERE id = ?'

QUERY_INSERT_STATUS = 'INSERT INTO IncomingPaypalStatus (history_id, status) VALUES (:history_id, :status)'

def process():
    con = sqlite3.connect(SQLITE_DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('begin exclusive transaction')
    cur.execute(QUERY_GET_INCOMING)
    incomingRow = cur.fetchone()
    cur.execute(QUERY_INSERT_STATUS, a)
    cur.execute(QUERY_DELETE_INCOMING, (incomingRow['id']))
    cur.commit()


