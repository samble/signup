#!/usr/local/bin/python2.6
""" module doc string """
import sqlite3
import traceback
import pdb

from urllib2 import urlopen

from _include import SQLITE_DB_PATH, logException
from _data import (SD_RECEIVER_EMAIL,
                   PAYPAL_VERIFY_URL,
                   QUERY_GET_PAYPAL_INCOMING,
                   QUERY_DELETE_PAYPAL_INCOMING,
                   QUERY_INSERT_PAYPAL_STATUS,
                   QUERY_GET_PREVIOUS_TRANSACTIONID_COUNT,
                   QUERY_INSERT_SIGNUP_HISTORY,
                   QUERY_INSERT_SIGNUP_INCOMING,
                   QUERY_UPDATE_PAYPAL_STATUS,
                   QUERY_INSERT_RESET_HISTORY,
                   QUERY_INSERT_RESET_INCOMING)

def getIncomingRow():
    """docstring"""
    incomingRow = None

    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('begin exclusive transaction')
        cur.execute(QUERY_GET_PAYPAL_INCOMING)
        incomingRow = cur.fetchone()
        cur.execute(QUERY_INSERT_PAYPAL_STATUS, 
            {'history_id': incomingRow['history_id'], 
             'status': 'initial'})
        cur.execute(QUERY_DELETE_PAYPAL_INCOMING, (incomingRow['id'],))
        con.commit()
        con.close()

    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

    else:
        return incomingRow

def main():
    """docstring"""
    try:
        incomingRow = getIncomingRow()

        post_body = incomingRow['post_body']
        history_id = incomingRow['history_id']
        receiver_email = incomingRow['receiver_email']
        payment_status = incomingRow['payment_status']
        item_name = incomingRow['item_name']
        txn_type = incomingRow['txn_type']
        txn_id = incomingRow['txn_id']
        test_ipn = incomingRow['test_ipn']
        option_name1 = incomingRow['option_name1']


        if not paypalVerifyPost(post_body):
            updateStatus(history_id, 'verification failed')

        elif receiver_email != SD_RECEIVER_EMAIL:
            updateStatus(history_id, 'incorrect reciever email')

        elif payment_status != 'Completed':
            updateStatus(history_id, 'incomplete payment')

        elif item_name not in ('Shell Account', 'Donation'):
            updateStatus(history_id, 'unknown item_name')

        elif txn_type not in ('subscr_signup','web_accept'):
            updateStatus(history_id, 'inactionable txn_type')

        elif isDuplicateTransaction(history_id, txn_id):
            updateStatus(history_id, 'duplicate transaction id')

        elif test_ipn == 1:
            updateStatus(history_id, 'test IPN')

        else:
            if item_name == 'Shell Account':
                if option_name1 == 'username':

                    username = incomingRow['option_selection1']
                    email = incomingRow['payer_email']
                    payer_id = incomingRow['payer_id']

                    insertSignup(username, email, payer_id)
                    updateStatus(history_id, 'signup inserted')

                elif option_name1 == 'reset':

                    username = incomingRow['option_selection1']
                    email = incomingRow['payer_email']

                    insertPasswordReset(username, email, payer_id)
                    updateStatus(history_id, 'password reset inserted')

                else:
                    updateStatus(history_id, 'unknown option_name1')

            else: # item_name == 'Donation'
                insertDonation()
                updateStatus(history_id, 'donation')

    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

def naim():
    incomingRow = getIncomingRow()
    pdb.set_trace()
    paypalVerifyPost(incomingRow['post_body'])

def updateStatus(history_id, status):
    pdb.set_trace()
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.execute(QUERY_UPDATE_PAYPAL_STATUS, 
                    {'history_id': history_id, 'status': status})
        con.commit()
        con.close()
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

def paypalVerifyPost(post_body):
    try:
        url = PAYPAL_VERIFY_URL
        if 'test_ipn=1' in post_body:
            url = PAYPAL_TEST_VERIFY_URL
        response = urlopen(PAYPAL_VERIFY_URL, 
                           'cmd=_notify-validate&' + post_body)
        if response.code == 200 and response.read() == 'VERIFIED':
            return True
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)
    return False

def isDuplicateTransaction(history_id, txn_id):
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        cur = con.execute(QUERY_GET_PREVIOUS_TRANSACTIONID_COUNT, 
                          {'history_id': history_id, 'txn_id': txn_id})
        count = cur.fetchone()[0]
        if count > 0:
            return True
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)    
    return False

def insertSignup(payer_id, username, email):
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.execute(QUERY_INSERT_SIGNUP_HISTORY, 
                   {'source': 'paypal', 'source_id': payer_id,
                     'username': username, 'email': email})
        history_id = con.execute('select last_insert_rowid()').fetchone()[0]
        con.execute(QUERY_INSERT_SIGNUP_INCOMING, 
                          {'source': 'paypal', 'source_id': payer_id, 
                           'username': username, 'email': email, 
                           'history_id': history_id})
        con.commit()
        con.close()
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

def insertPasswordReset(payer_id, username):
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.execute(QUERY_INSERT_RESET_HISTORY, 
                    {'source': 'paypal', 
                     'source_id': payer_id, 'username': username})
        history_id = con.execute('select last_insert_rowid()').fetchone()[0]
        con.execute(QUERY_INSERT_RESET_INCOMING,
                    {'source': 'paypal',
                     'source_id': payer_id,
                     'username': username,
                     'history_id': history_id})
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)
  
def insertDonation():
    pass

if __name__ == '__main__':
   main()
