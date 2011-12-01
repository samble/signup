#!/usr/local/bin/python2.6
""" module doc string """
import sqlite3

from _include import SQLITE_DB_PATH
from _data import (QUERY_GET_INCOMING,
                   QUERY_DELETE_INCOMING,
                   QUERY_INSERT_STATUS)

def process():
    """ NOTE: ``a`` is undefined currently.. """
    con = sqlite3.connect(SQLITE_DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute('begin exclusive transaction')

    cur.execute(QUERY_GET_INCOMING)
    incomingRow = cur.fetchone()
    cur.execute(QUERY_INSERT_STATUS, a)
    cur.execute(QUERY_DELETE_INCOMING, (incomingRow['id']))

    cur.commit()
