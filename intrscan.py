from Filehash import FileHash
from sqlops import Sqlops
from processlist import Processhandle




class FileScan():

    infectedApps = []
    def __init__(self):
        pass


    def scan(self):
        sql = Sqlops()
        apps = sql.sqlAppSelect()
        applist = apps.fetchall()
        result = self.filescan(applist)
        if result == 0:
            print("safe")
        else:
            print("change")
            ps = Processhandle()
            for apps in FileScan.infectedApps:
                ps.stopapp(apps)

    def filescan(self,applist):

        filerror = 0
        for apps in applist:
            file = FileHash()
            path = apps[2]
            id   = apps[0]
            file.checkfoldersave(folder=path,calltype="scan",appid=id)
            filedict = file.fileDict
            sql = Sqlops()
            fileresult = sql.sqlsignSelect(appid=id)

            for rows in fileresult:

                if filerror == 1:
                    break

                for x, y in filedict.items():
                    if(rows[2] == y):
                        if(rows[4] == x):

                            print("no change")

                        else:

                            print("File changed")
                            print(rows[2])
                            filerror = 1
                            appid = rows[5]
                            FileScan.infectedApps.append(appid)
                            break
            else:
                print("breked")
        else:
            return 0




fs = FileScan()
fs.scan()
print(FileScan.infectedApps)









# file = FileHash()
# file.checkfoldersave('testdir',calltype="scan",appid=1)
# print(FileHash.fileDict)
# dict = FileHash.fileDict
# print(len(FileHash.fileDict))
#
# db = Sqlops()
# result = db.sqlsignSelect()
# for rows in result:
#     for x, y in dict.items():
#         if(rows[2] == y):
#             if(rows[4] == x):
#                 print("no change")
#             else:
#                 print("File changed")
#                 print(rows[2])
#                 break




