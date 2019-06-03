from intrscan import FileScan
import wx
from pythongui import MainWindow

if __name__ == "__main__":
    fs = FileScan()
    result = fs.scan()
    print(result)
    if  result:
        app = wx.App(False)
        frame = MainWindow(None, 'Intrusion Detection System')
        frame.onStartUpScan(result)
        app.MainLoop()
