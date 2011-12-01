#!/usr/local/bin/python2.6
""" module doc string
"""
import urllib
import traceback
from urlparse import parse_qs
import sys

import pdb
import sqlite3

from _include import (logException, SQLITE_DB_PATH, this_is_prod)
from _data import (HISTORY_FIELDS, INCOMING_FIELDS,
                   QUERY_INSERT_HISTORY, QUERY_INSERT_INCOMING)

def mutate_fields(fields, original_qs=''):
    """ currently this actually mutates the fields in place.
        we'll still return them anyway, just in case that part
        of the implementation changes.
    """

    # Values don't need to be 1 element lists
    fields = dict((i, fields[i][0]) for i in fields)

    # Save entire post body for postback verification
    fields['post_body'] = original_qs

    # If it's not a test, mark it so manually
    if 'test_ipn' not in fields:
        fields['test_ip'] = 0

    return fields

def handle_fields(fields):
    """ docstring """
    insertPaypalTransaction(fields)

def handle(environ, start_response):
    """ boiler plate for wsgi stuff """
    try:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        formbody = environ['wsgi.input'].read()
        fields = parse_qs(formbody)
        fields = mutate_fields(fields, original_qs=formbody)
        handle_fields(fields)
    except Exception as ex:
        exInfo = traceback.format_exc()
        logException(ex, exInfo)
    else:
        return [str(fields)]

def insertPaypalTransaction(fieldDict):
    """ docstring """
    try:
        _fieldDict = fieldDict.copy()

        con = sqlite3.connect(SQLITE_DB_PATH)
        historyParams = dict((field, _fieldDict[field] if field in _fieldDict else '') for field in HISTORY_FIELDS)
        open('output', 'a+').write(str(historyParams))
        con.execute(QUERY_INSERT_HISTORY, historyParams)

        id = con.execute('select last_insert_rowid()').fetchone()[0]
        _fieldDict['history_id'] = id

        incomingParams = dict((field, _fieldDict[field] if field in _fieldDict else '') for field in INCOMING_FIELDS)
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

def niam():
    """ alternative main """
    from flask import Flask, request
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def handle():

        # originally..
        #formbody = environ['wsgi.input'].read()
        #fields = parse_qs(formbody)

        # new..
        formbody = urllib.urlencode(request.form)
        fields = dict(request.form)
        fields = mutate_fields(fields, original_qs=formbody)
        handle_fields(fields)

        return '\n'+str(dict(request.form))+'\n\n'

    app.run(debug=True,host='0.0.0.0',port=8080)

if __name__ == '__main__':
    if this_is_prod():
        main()
    else:
        niam()
