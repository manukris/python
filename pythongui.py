

import wx
import time
from Filehash import *
from intrscan import FileScan
from processlist import Processhandle

class MainWindow(wx.Frame):

    def __init__(self, parent, title):


        self.sqlops   = Sqlops()
        self.filehash = FileHash()
        self.filescan = FileScan()
        self.ps       = Processhandle()

        wx.Frame.__init__(self, parent, title=title, size=(700, 500))
        self.Centre()
        self.gui()
        self.Show()

    def gui(self):
           # A Statusbar in the bottom of the window                            
           self.CreateStatusBar()                                               
                                                                                
           # Setting up the menu                                                
           file_menu = wx.Menu()                                                
                                                                                
           # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided               
           # by wxWidgets.                                                      
           file_menu.Append(wx.ID_ABOUT, '&About',                              
                            'Information about this application')               
           file_menu.Append(wx.ID_NEW, '&New')                                  
           file_menu.Append(wx.ID_OPEN, '&Open')                                
           file_menu.Append(wx.ID_SAVE, '&Save')                                
           file_menu.AppendSeparator()                                          
           file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit the application')        
                                                                                
           # Creating the menubar                                               
           menu_bar = wx.MenuBar()                                              
                                                                                
           # Adding the 'file_menu' to the menu bar                             
           menu_bar.Append(file_menu, '&File')                                  
                                                                                
           # Adding the menu bar to the frame content                           
           self.SetMenuBar(menu_bar)

           self.pnl = wx.Panel(self)

           self.listbox = wx.ListCtrl(self.pnl,pos=(10, 10),size=(500, 300),style=wx.LC_REPORT)

           self.listbox.InsertColumn(0,"Application",width=420)
           self.listbox.InsertColumn(1,'Status')

           result = self.sqlops.sqlAppSelectAll()
           apps = result.fetchall()

           for app in apps:
               index = self.listbox.InsertItem(0, app[1])
               status = self.getStatus(app[4])
               self.listbox.SetItem(index, 1, status)



           btn1 = wx.Button(self.pnl, label='Add Application', pos=(10, 350), size=(120, -1))
           btn2 = wx.Button(self.pnl, label='Add Exception', pos=(200, 350), size=(120, -1))
           btn3 = wx.Button(self.pnl, label='Update Files', pos=(400, 350), size=(120, -1))
           btn4 = wx.Button(self.pnl, label='Scan', pos=(550, 50), size=(120, -1))

           btn5 = wx.Button(self.pnl, label='Reset Database', pos=(550, 150), size=(120, -1))

           btn1.Bind(wx.EVT_BUTTON, self.onFileopen)
           btn4.Bind(wx.EVT_BUTTON,self.onScan)
           btn5.Bind(wx.EVT_BUTTON,self.onResetDb)
           btn2.Bind(wx.EVT_BUTTON, self.onExcept)
           btn3.Bind(wx.EVT_BUTTON, self.onUpdate)



    def messageDialog(self,message,caption):

        dialog = wx.MessageDialog(self, message=message, caption=caption,
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING)
        result = dialog.ShowModal()
        if result == wx.ID_CANCEL:
            return False
        return True



    def onExcept(self,event):
        count = self.listbox.SelectedItemCount
        if count == 0:
            self.messageDialog(message="No app Selected to Add exception", caption="Error")
            return  False
        if not self.messageDialog(message="Add Exception",caption="Confirm delete Signatiures"):
            return False
        else:
                apps = self.listbox.GetFirstSelected()
                while (apps != -1):

                    appname = self.listbox.GetItemText(item=apps,col=0)

                    if(self.sqlops.getAppStatus(appname) == 0):
                        appid   = self.sqlops.getAppId(appname)
                        self.sqlops.changeAppStatus(appid,2)
                        self.sqlops.deleteExptAppFile(appid)
                    apps = self.listbox.GetNextSelected(apps)
                self.reloadListBox()


    def onUpdate(self,event):

        if not self.messageDialog(message = "Update File Signature",caption= "Confirm Update Signatiures" ):
            return False
        else:
            count = self.listbox.SelectedItemCount
            if count == 0:
                print("Select an App")
            else:
                apps = self.listbox.GetFirstSelected()
                while (apps != -1):
                    appname  = self.listbox.GetItemText(item=apps,col=0)
                    pathname = self.sqlops.getAppPath(appname)
                    appid    = self.sqlops.getAppId(appname)
                    self.sqlops.changeAppStatus(appid,0)
                    filestr = FileHash()
                    print(pathname)
                    filestr.checkfoldersave(pathname,calltype='save',appid=appid)
                    apps = self.listbox.GetNextSelected(apps)
                self.reloadListBox()


    def reloadListBox(self):
        self.listbox.DeleteAllItems()
        result = self.sqlops.sqlAppSelectAll()
        apps   = result.fetchall()
        for app in apps:
            index = self.listbox.InsertItem(0, app[1])
            status = self.getStatus(app[4])
            self.listbox.SetItem(index, 1, status)


    def getStatus(self,status):
        if status == 0:
            return "Added"
        elif status == 1:
            return "Blocked"
        elif status == 2:
            return "Excepmted"

    def onResetDb(self,e):

        if not self.messageDialog(message="Reset Database",caption="Confirm Reset Database"):
            return False
        else:
            self.sqlops.resetDbs()
            self.listbox.DeleteAllItems()
            self.messageDialog(message="Success", caption="Successfully Reset Database")


    def onScan(self,e):

        result = self.filescan.scan()

        if  not result:
            self.messageDialog(message="No Application to scan",caption="Error")
            return  False

        if result != 1:
            appid = result[5]
            appname = self.sqlops.getAppName(result[5])

            self.messageDialog(message="This file Changed Location "+result[2]+"Appname =="+appname,caption="File Changed")

            if not self.messageDialog(message="Stop Application "+appname, caption="Confirm Stop"):
                print("caneled")
                return False
            else:

                result = self.ps.stopapp(appname)
                if result == 1:
                    self.sqlops.changeAppStatus(appid,status=1)
                    self.reloadListBox()
                else:
                    self.messageDialog(message="Unable to stop Application it is not running currently" ,caption="Unable to stop")

        else:
            self.messageDialog(message="No file Changed",caption=" No Intrusion")

    def onFileopen(self,e):
        with wx.DirDialog (None, "Choose App Folder", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                 print("cancelled")
                 return     # the user changed their mind
                    # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            if self.sqlops.checkAppExists(pathname):
                self.messageDialog(message="Error", caption="Application Already exists")
                return False


            appname = os.path.basename(pathname)
            index = self.listbox.InsertItem(0, appname)
            status = self.getStatus(0)
            self.listbox.SetItem(index, 1, status)
            appid = self.sqlops.setAppData(path=pathname)
            self.filehash.checkfoldersave(pathname,calltype='save',appid=appid)
            # wx.Gauge(pnl,)

            self.messageDialog(message="Success", caption="Successfully Added Application")


            
app = wx.App(False)
frame = MainWindow(None, 'Intrusion Detection System')
app.MainLoop()


