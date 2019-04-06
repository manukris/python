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

           pnl = wx.Panel(self)

           listbox = wx.ListBox(pnl,pos=(10, 10),size=(500, 300))

           btn1 = wx.Button(pnl, label='Add application', pos=(10, 350), size=(120, -1))

           btn2 = wx.Button(pnl, label=' application', pos=(200, 350), size=(120, -1))


           btn4 = wx.Button(pnl, label=' label', pos=(550, 50), size=(120, -1))

           btn5 = wx.Button(pnl, label=' label', pos=(550, 150), size=(120, -1))


           

           # btn = wx.Button(pnl, label='Scan', pos=(90, 185), size=(60, -1))

           # btn.Bind(wx.EVT_BUTTON, self.onFileopen)
           
    def onFileopen(self,e):
        with wx.DirDialog (None, "Choose input directory", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                 print("cancelled")
                 return     # the user changed their mind
                    # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print(pathname)
app = wx.App(False)
frame = MainWindow(None, 'Sample application')
app.MainLoop()







