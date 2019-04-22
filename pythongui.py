# import wx
#
#
# class MyTarget(wx.TextDropTarget):
#     def __init__(self, object):
#         wx.TextDropTarget.__init__(self)
#         self.object = object
#
#     def OnDropText(self, x, y, data):
#         self.object.InsertStringItem(0, data)
#
#
# class Mywin(wx.Frame):
#
#     def __init__(self, parent, title):
#         super(Mywin, self).__init__(parent, title=title, size=(-1, 300))
#         panel = wx.Panel(self)
#         box = wx.BoxSizer(wx.HORIZONTAL)
#         languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript',
#                      'PHP', 'VB.NET', 'C#']
#
#         self.lst1 = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
#         self.lst2 = wx.ListCtrl(panel, -1, style=wx.LC_LIST)
#         for lang in languages:
#             self.lst1.InsertStringItem(0, lang)
#
#         dt = MyTarget(self.lst2)
#         self.lst2.SetDropTarget(dt)
#         wx.EVT_LIST_BEGIN_DRAG(self, self.lst1.GetId(), self.OnDragInit)
#
#         box.Add(self.lst1, 0, wx.EXPAND)
#         box.Add(self.lst2, 1, wx.EXPAND)
#
#         panel.SetSizer(box)
#         panel.Fit()
#         self.Centre()
#         self.Show(True)
#
#     def OnDragInit(self, event):
#         text = self.lst1.GetItemText(event.GetIndex())
#         tobj = wx.PyTextDataObject(text)
#         src = wx.DropSource(self.lst1)
#         src.SetData(tobj)
#         src.DoDragDrop(True)
#         self.lst1.DeleteItem(event.GetIndex())
#
#
# ex = wx.App()
# Mywin(None, 'Drag&Drop Demo')
# ex.MainLoop()


import wx
import time
from Filehash import *

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

           self.listbox = wx.ListBox(self.pnl,pos=(10, 10),size=(500, 300))

           sqlops = Sqlops()
           result = sqlops.sqlAppSelect()
           apps = result.fetchall()
           for app in apps:
                self.listbox.Append(app[1])


           btn1 = wx.Button(self.pnl, label='Add application', pos=(10, 350), size=(120, -1))
           btn2 = wx.Button(self.pnl, label=' application', pos=(200, 350), size=(120, -1))
           btn4 = wx.Button(self.pnl, label=' Scan', pos=(550, 50), size=(120, -1))

           btn5 = wx.Button(self.pnl, label='Reset Database', pos=(550, 150), size=(120, -1))

           btn1.Bind(wx.EVT_BUTTON, self.onFileopen)
           btn4.Bind(wx.EVT_BUTTON,self.onScan)
           btn5.Bind(wx.EVT_BUTTON,self.onResetDb)








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



    def onScan(self,e):

        count = 0
        max = 80
        progress_dialog = wx.ProgressDialog(title="Scanning", message="Scanning Files",
                                           maximum=max, parent=self,style=wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME|wx.PD_APP_MODAL)

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            wx.MilliSleep(250)

            if count >= max / 2:
                (keepGoing, skip) = progress_dialog.Update(count, "Half-time!")
            else:
                (keepGoing, skip) = progress_dialog.Update(count)
        progress_dialog.Destroy()

        
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


            self.listbox.Append(pathname)
            filestr = FileHash()

            appid = sqlops.setAppData(path=pathname)
            filestr.checkfoldersave(pathname,calltype='save',appid=appid)
            # wx.Gauge(pnl,)

            dialog = wx.MessageDialog(self, message="Success", caption="Successfully Added Application",
                                      style=wx.OK | wx.ICON_INFORMATION)
            dialog.ShowModal()


            
            
app = wx.App(False)
frame = MainWindow(None, 'Sample application')
app.MainLoop()





