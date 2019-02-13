import sqlite3 #sqlite library of python
import time #time library of python




class Sqlops:


    def __init__(self,filename,filepath,sign,appid):

        self.conn = sqlite3.connect('test.db')
        self.sqlCursor = self.conn.cursor()
        self.filename = filename
        self.filepath = filepath
        self.filetime = str(time.time())
        self.sign     = sign
        self.appid    = appid

    # def sqliteCreate():
    #
    #
    #     # Create table
    #     c.execute('''CREATE TABLE signature
    #                                  (id INTEGER PRIMARY KEY AUTOINCREMENT, filename text, filepath text, filetime text, signature text, appid INTEGER)''')
    #
    #     # Insert a row of data
    #     # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    #
    #     # Save (commit) the changes
    #     conn.commit()
    #
    #     # We can also close the connection if we are done with it.
    #     # Just be sure any changes have been committed or they will be lost.
    #     conn.close()
    # sqliteCreate()


    def sqlSignInsert(self):

        sql = "INSERT INTO signature (filename,filepath,filetime,signature,appid) VALUES ('"+self.filename+"','"+self.filepath+"','"+self.filetime+"','"+self.sign+"',"+str(self.appId)+")"
        print(sql)

        self.sqlCursor.execute(sql)

        self.conn.commit()

    # def sqlsignSelect(self):
    #     sql = ""



