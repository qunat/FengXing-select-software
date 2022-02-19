# -*- coding: utf-8 -*-
import win32com.client as win32
import pythoncom
'''
#sw VBA接口引入
swApp = win32.Dispatch("Sldworks.application")            #引入sldworks接口
swApp.Visible = True                                      #是否可视化
arg_Nothing = win32.VARIANT(pythoncom.VT_DISPATCH, None)   #转义VBA中不同变量nothing
#swApp.OpenDoc(r'零件1.SLDPRT',1)     #打开二次开发源文件
#swApp.OpenDoc(r"D:\text6\枫信自动化选型软件\3Dsource\零件1.SLDPRT", 1)
errors=1000
Part = swApp.ActiveDoc
AssemblyTitle = Part.GetTitle#获取当前装配体零件名称
#Part = swApp.ActivateDoc3(AssemblyTitle, True, 0, errors)
print(AssemblyTitle)
swInsertedComponent = Part.AddComponent5(r"D:\text6\枫信自动化选型软件\3Dsource\零件1.SLDPRT", 0, "", False, "", -8.563954162355E-05, 0, 4.51908189234018E-05)
#导入stp
boolstatus = swApp.LoadFile2(r"D:\text6\枫信自动化选型软件\3Dsource\resource\KB\FXKB40斜齿行星减速机\FXKB40-S2-L1.STEP", "r")
'''
class Solidworks_API(object):
    def __init__(self,main_gui=None):
        try:
            # sw VBA接口引入
            self.swApp = win32.Dispatch("Sldworks.application")  # 引入sldworks接口
            self.swApp.Visible = True  # 是否可视化
            self.arg_Nothing = win32.VARIANT(pythoncom.VT_DISPATCH, None)  # 转义VBA中不同变量nothing
            self.Part=self.swApp.ActiveDoc#获取solidworks最高权限
        except:
            pass
    def Open_part(self):
        pass
    def Import_part(self,filepath):#solidworks 打开stp文件
        print("so",filepath)
        AssemblyTitle = self.Part.GetTitle  # 获取当前装配体零件名称
        print(AssemblyTitle)
        boolstatus = self.swApp.LoadFile2(filepath, "r")
