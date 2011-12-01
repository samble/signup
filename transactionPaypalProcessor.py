#!/usr/local/bin/python2.6
""" module doc string """
from sys import exit
import sqlite3

from _include import *
from _data import (QUERY_GET_INCOMING,
                   QUERY_DELETE_INCOMING,
                   QUERY_INSERT_STATUS)

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
