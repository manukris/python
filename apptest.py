from Filehash import FileHash
from sqlops import Sqlops

file = FileHash()
#checking folder testdir

sql = Sqlops()

# sql.resetDbs();
path = "/var/www/html/test"
appid = sql.setAppData(path=path)
file.checkfoldersave(folder=path,calltype="save",appid=appid)
print(file.fileDict)