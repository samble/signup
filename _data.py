
PAYPAL_FIELDS = ['last_name',
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
'quantity',
'subscr_id',
'option_selection1',
'option_name1']

PAYPAL_HISTORY_FIELDS = PAYPAL_FIELDS
PAYPAL_INCOMING_FIELDS = PAYPAL_HISTORY_FIELDS + ['post_body','history_id']

QUERY_INSERT_PAYPAL_HISTORY = 'INSERT INTO IncomingPaypalHistory (' + \
                       ','.join(PAYPAL_HISTORY_FIELDS) + ') VALUES (' +\
                       ','.join([':' + field for field in PAYPAL_HISTORY_FIELDS]) + ')'

QUERY_INSERT_PAYPAL_INCOMING = 'INSERT INTO IncomingPaypal (' + \
                        ','.join(PAYPAL_INCOMING_FIELDS) + ') VALUES (' + \
                        ','.join([':' + field for field in PAYPAL_INCOMING_FIELDS]) + ')'

QUERY_GET_PAYPAL_INCOMING = '''SELECT
id,
history_id,
txn_id,
receiver_email,
payment_status,
item_name,
test_ipn,
payer_id,
payer_email,
option_selection1,
option_name1,
post_body
FROM IncomingPaypal
WHERE id = (SELECT MIN(id) FROM IncomingPaypal)'''

QUERY_DELETE_PAYPAL_INCOMING = 'DELETE FROM IncomingPaypal WHERE id = ?'

QUERY_INSERT_PAYPAL_STATUS = 'INSERT INTO IncomingPaypalStatus (history_id, status) VALUES (:history_id, :status)' 

QUERY_UPDATE_PAYPAL_STATUS = 'UPDATE IncomingPaypalStatus SET status = :status, update_date = current_timestamp where history_id = :history_id'


PAYPAL_VERIFY_URL = 'http://www.sandbox.paypal.com/cgi-bin/webscr'
