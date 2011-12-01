from time import strftime

SQLITE_DB_PATH = '/var/wwws/cgi-bin/transactions.db'

def logException(ex, traceString):
    try:
        con = sqlite3.connect(SQLITE_DB_PATH)
        con.execute('INSERT INTO Exceptions (type, args, message, trace) VALUES (:type, :args, :message, :trace)',
            {'type': str(type(ex)), 'args': str(ex.args), 'message': str(e.message), 'trace': traceString})
        con.commit()
        con.close()
    except Exception as ex:
        f = open('/var/wwws/cgi-bin/last-resort.txt', 'a+')
        f.writelines([strftime("%x %X %Z"), 'FATALLY FUCKED UP HANDLING EXCEPTION!', repr(ex), traceString])
        f.close()
