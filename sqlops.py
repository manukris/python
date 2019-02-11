import sqlite3
import time



# def sqliteCreate():

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





def sqlSignInsert(filename,filepath,sign,appId):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    filetime = str(time.time())
    sql = "INSERT INTO signature (filename,filepath,filetime,signature,appid) VALUES ('"+filename+"','"+filepath+"','"+filetime+"','"+sign+"',"+str(appId)+")"
    print(sql)
    c.execute(sql)

    #
    #     # Save (commit) the changes
    conn.commit()
    #
    #     # We can also close the connection if we are done with it.
    #     # Just be sure any changes have been committed or they will be lost.
    conn.close()


