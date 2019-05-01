

import wx
import time
from Filehash import *
from intrscan import FileScan
from processlist import Processhandle

class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title,size=(700, 500))
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

           sqlops = Sqlops()
           result = sqlops.sqlAppSelect()
           apps = result.fetchall()

           for app in apps:
               index = self.listbox.InsertItem(0, app[1])
               status = self.getStatus(app[4])
               self.listbox.SetItem(index, 1, status)



           btn1 = wx.Button(self.pnl, label='Add application', pos=(10, 350), size=(120, -1))
           btn2 = wx.Button(self.pnl, label=' application', pos=(200, 350), size=(120, -1))
           btn4 = wx.Button(self.pnl, label=' Scan', pos=(550, 50), size=(120, -1))

           btn5 = wx.Button(self.pnl, label='Reset Database', pos=(550, 150), size=(120, -1))

           btn1.Bind(wx.EVT_BUTTON, self.onFileopen)
           btn4.Bind(wx.EVT_BUTTON,self.onScan)
           btn5.Bind(wx.EVT_BUTTON,self.onResetDb)


    def reloadListBox(self):
        self.listbox.DeleteAllItems()
        sqlops = Sqlops()
        result = sqlops.sqlAppSelect()
        apps = result.fetchall()
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
        dialog = wx.MessageDialog(self, message="Reset Database", caption="Confirm Reset Database",
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING)
        result = dialog.ShowModal()
        if result == wx.ID_CANCEL:
            print("cancelled")
            return
        else:
            sqlobj = Sqlops()
            sqlobj.resetDbs()
            dialog = wx.MessageDialog(self, message="Success", caption="Successfully Reset Database",
                                      style=wx.OK |wx.ICON_INFORMATION)
            dialog.ShowModal()
            self.listbox.DeleteAllItems()


    def onScan(self,e):

        fs = FileScan()
        result = fs.scan()
        
        if result != 1:
            sql = Sqlops()
            appid = result[5]
            appname = sql.getAppName(result[5])

            dialog = wx.MessageDialog(self, message="This file Changed Location "+result[2]+"Appname =="+appname, caption="File Changed",
                                      style=wx.OK | wx.ICON_ERROR)
            dialog.ShowModal()

            dialog = wx.MessageDialog(self, message="Stop Application "+appname, caption="Confirm Stop",
                                      style=wx.OK | wx.CANCEL | wx.ICON_WARNING)                                               
            result = dialog.ShowModal()
            if result == wx.ID_CANCEL:
                print("caneled")
            else:
                ps = Processhandle()
                result = ps.stopapp(appname)
                if result == 1:
                    sql.changeAppStatus(appid)
                    self.reloadListBox()
                    print("success")
                else:
                    print("error")

            print(result)
        else:
            print("okk")


        #
        # count = 0
        # max = 80
        # progress_dialog = wx.ProgressDialog(title="Scanning", message="Scanning Files",
        #                                    maximum=max, parent=self,style=wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME|wx.PD_APP_MODAL)
        #
        # keepGoing = True
        # count = 0
        #
        # while keepGoing and count < max:
        #     count += 1
        #     wx.MilliSleep(250)
        #
        #     if count >= max / 2:
        #         (keepGoing, skip) = progress_dialog.Update(count, "Half-time!")
        #     else:
        #         (keepGoing, skip) = progress_dialog.Update(count)
        # progress_dialog.Destroy()




        
    def onFileopen(self,e):
        with wx.DirDialog (None, "Choose App Folder", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                 print("cancelled")
                 return     # the user changed their mind
                    # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print(pathname)
            sqlops = Sqlops()
            if sqlops.checkAppExists(pathname):
                print("duplicate")
                dialog = wx.MessageDialog(self, message="Error", caption="Application Already exists",
                                          style=wx.OK | wx.ICON_ERROR)
                dialog.ShowModal()
                return

            filestr = FileHash()

            appname = os.path.basename(pathname)
            index = self.listbox.InsertItem(0, appname)
            status = self.getStatus(0)
            self.listbox.SetItem(index, 1, status)
            appid = sqlops.setAppData(path=pathname)
            filestr.checkfoldersave(pathname,calltype='save',appid=appid)
            # wx.Gauge(pnl,)

            dialog = wx.MessageDialog(self, message="Success", caption="Successfully Added Application",
                                      style=wx.OK | wx.ICON_INFORMATION)
            dialog.ShowModal()


            
            
app = wx.App(False)
frame = MainWindow(None, 'Sample application')
app.MainLoop()
