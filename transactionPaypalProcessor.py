#!/usr/local/bin/python2.6
""" module doc string """
import sqlite3

from urllib2 import urlopen

from _include import SQLITE_DB_PATH
from _data import (QUERY_GET_PAYPAL_INCOMING,
                   QUERY_DELETE_PAYPAL_INCOMING,
                   QUERY_INSERT_PAYPAL_STATUS)

def process():
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

    cur.commit()
    con.close()

    history_id = incomingRow['history_id']
    post_body = incomingRow['post_body']

    if incomingRow['payment_status'] != 'Completed':
        updateStatus(history_id, 'incomplete payment')
    elif item_name not in ['Shell Account', 'Donation']:
        updateStatus(history_id, 'unknown item_name')
    elif not paypalVerifyPost(post_body):
        updateStatus(history_id, 'verification failed')

def updateStatus(history_id, status):
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.execute(QUERY_UPDATE_PAYPAL_STATUS, {'history_id': history_id, 'status': status})        
        con.close()
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

def paypalVerifyPost(post_body):
    try:
        urlopen(
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)
        return False
    else:
        return True
