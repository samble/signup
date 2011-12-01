#!/usr/local/bin/python2.6
""" module doc string
"""
import sqlite3
import traceback

from urlparse import parse_qs
from exceptions import Exception
import sys

from _include import *
from _data import (HISTORY_FIELDS, INCOMING_FIELDS,
                   QUERY_INSERT_HISTORY, QUERY_INSERT_INCOMING)

print SQLITE_DB_PATH

def handle(environ, start_response):
    """ docstring """
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

    return [str(fields)]

def insertPaypalTransaction(fieldDict):
    """ docstring """
    try:
        _fieldDict = fieldDict.copy()

        con = sqlite3.connect(SQLITE_DB_PATH)

        historyParams = dict((field, _fieldDict[field][0] if field in _fieldDict else '') for field in HISTORY_FIELDS)
        open('output', 'a+').write(str(historyParams))
        con.execute(QUERY_INSERT_HISTORY, historyParams)

        id = con.execute('select last_insert_rowid()').fetchone()[0]
        _fieldDict['history_id'] = id

        incomingParams = dict((field, _fieldDict[field][0] if field in _fieldDict else '') for field in INCOMING_FIELDS)
        con.execute(QUERY_INSERT_INCOMING, incomingParams)

        con.commit()
        con.close()

    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)

def main():
    """ docstring """
    from flup.server.fcgi import WSGIServer
    WSGIServer(handle).run()

if __name__ == '__main__':
    main()
