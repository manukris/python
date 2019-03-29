from psutil import *


class Processhandle:

    appname = ""

    def stopapp(self,appname):
        for proc in process_iter():
           try:
               pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           except NoSuchProcess:
              print("exception")
           else:
              print(pinfo)
              if pinfo['name'] == appname or pinfo['name'] == appname+".exe":
                  proc.kill()
    def getCurrentProcessList(self):
        for proc in process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            except NoSuchProcess:
                print("exception")
            print(pinfo)


if __name__ == "__main__":
    ps = Processhandle()
    ps.getCurrentProcessList()
    ps.stopapp('postgres')
    ps.getCurrentProcessList()


