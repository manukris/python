from psutil import *

class Processhandle:
    appname = ""
    def stopapp(self):
        for proc in process_iter():
           try:
               pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           except NoSuchProcess:
              print("exception")
           else:
              print(pinfo)
              if pinfo['name'] == 'sublime_text':
                  proc.kill()

