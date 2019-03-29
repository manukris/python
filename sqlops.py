import sqlite3 #sqlite library of python
import time #time library of python
import os




class Sqlops:


    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.sqlCursor = self.conn.cursor()
        self.createDbs()

    def createDbs(self):
        sql = """CREATE TABLE IF NOT EXISTS signature
                                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                     filename text, 
                                     filepath text, 
                                     filetime text, 
                                     signature text, 
                                     appid INTEGER);"""

        self.sqlCursor.execute(sql)
        self.conn.commit()

        sql = """CREATE TABLE IF NOT EXISTS application
                                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                             name text, 
                                             path text, 
                                             time  text, 
                                             status INTEGER DEFAULT 0
                                             );"""
        self.sqlCursor.execute(sql)
        self.conn.commit()



    def setAppData(self,**kwargs):
        kwargs['time'] = str(time.time())
        kwargs['appname'] = os.path.basename(kwargs['path'])
        sql = "INSERT INTO application (name,path,time) VALUES ('" +kwargs['appname']+ "','" +kwargs['path'] + "','" +kwargs['time'] + "')"
        print(sql)
        # execute sql
        self.sqlCursor.execute(sql)
        # save values ro db
        self.conn.commit()
        appid = self.sqlCursor.lastrowid
        return appid


    def setData(self,filename,filepath,sign,appid):
        self.filename = filename
        self.filepath = filepath
        self.filetime = str(time.time())
        self.sign = sign
        self.appid = appid


    def resetDbs(self):
        sql = "DROP TABLE application"
        self.sqlCursor.execute(sql)
        self.conn.commit()
        sql = "DROP TABLE signature"
        self.sqlCursor.execute(sql)
        self.conn.commit()
        self.createDbs()



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

        # insert query
        sql = "INSERT INTO signature (filename,filepath,filetime,signature,appid) VALUES ('"+self.filename+"','"+self.filepath+"','"+self.filetime+"','"+self.sign+"',"+str(self.appid)+")"
        print(sql)
        #execute sql
        self.sqlCursor.execute(sql)
        #save values ro db
        self.conn.commit()

    def sqlsignSelect(self,appid):
        sql = "SELECT * FROM signature where appid="+str(appid);
        print(sql)
        result =  self.sqlCursor.execute(sql)
        return result

    def sqlAppSelect(self):
        sql = "SELECT * FROM application where status = 0";
        print(sql)
        result = self.sqlCursor.execute(sql)
        return result

    def getAppName(self,appid):
        sql = "SELECT name FROM application where id="+str(appid);
        print(sql)
        result = self.sqlCursor.execute(sql)
        result = result.fetchone()
        return result[0]


if __name__ == "__main__":
    sql = Sqlops()
    appname = sql.getAppName(1)
    print(appname)








