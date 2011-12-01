""" module doc string """
from time import strftime

import sqlite3

SQLITE_DB_PATH = '/var/wwws/cgi-bin/transactions.db'
LAST_RESORT = '/var/wwws/cgi-bin/last-resort.txt'

def this_is_prod():
    """ prod environment predicate """
    return False

def this_is_dev():
    """ dev is environment predicate """
    return not this_is_prod()

def logException(ex, traceString):
    """ docstring """
    if this_is_dev():
        raise
    else:
        try:
            con = sqlite3.connect(SQLITE_DB_PATH)
            con.execute('INSERT INTO Exceptions (type, args, message, trace) ' + \
                        'VALUES (:type, :args, :message, :trace)',
                        {'type': str(type(ex)), 'args': str(ex.args),
                         'message': str(ex.message), 'trace': traceString})
            con.commit()
            con.close()
        except Exception as ex:
            f = open(LAST_RESORT, 'a+')
            f.writelines([strftime("%x %X %Z"),
                          'FATALLY FUCKED UP HANDLING EXCEPTION!',
                          repr(ex), traceString])
            f.close()
