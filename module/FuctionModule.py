#coding=utf-8
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopoDS import TopoDS_Builder, TopoDS_Compound
from OCC.Extend.DataExchange import write_step_file, write_iges_file, write_stl_file
from PyQt5.QtWidgets import QFileDialog
import re


def Translation_Assemble(self):  # 转换为装配体
    pass
    try:
        self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
        self.New_Compound = TopoDS_Compound()  # 定义一个复合体
        self.new_build.MakeCompound(self.New_Compound)  # 生成一个复合体DopoDS_shape
        for shape in self.aCompound:
            self.new_build.Add(self.New_Compound, shape)
        self.aCompound = self.New_Compound
    except:
        pass


def Assemble_Rename(self):
    try:
        Part_NO = 0
        with open(self.save_part_path, "r") as f:
            words = f.read()
            f.close()
        p = re.compile(r"Open CASCADE STEP translator 7.4 1.\d{1,2}")  # h获取子装配体名称
        assemble_part_name_list = p.findall(words)
        for i in range(0, (len(assemble_part_name_list)), 2):
            pass
            new_name = self.filename + "-" + str(Part_NO)
            words = words.replace(assemble_part_name_list[i], new_name)
            Part_NO += 1
        with open(self.save_part_path, "w+") as f:  # 重新写入stp
            f.write(words)
            f.close()
            # print("succeed")


    except:
        pass


def Output_stp_data(self):  # 将数据转换成stp并导出
    try:
        pass
        self.Translation_Assemble()
        path = "../" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.step)")
        write_step_file(self.aCompound, fileName)
        self.save_part_path = fileName
        self.Assemble_Rename()
        self.statusbar.showMessage("零件导出成功")

    except:
        pass
        self.statusbar.showMessage("错误：没用模型可以导出")


def Output_iges_data(self):  # 将数据转换成iges并导出
    try:
        pass
        self.Translation_Assemble()
        path = "./" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.iges)")
        write_iges_file(self.aCompound, fileName)
        self.save_part_path = fileName
        self.statusbar.showMessage("零件导出成功")

    except:
        pass
        self.statusBar.showMessage('错误：没用模型可以导出')


def Output_stl_data(self):  # stl
    try:
        pass
        self.Translation_Assemble()
        path = "./" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.iges)")
        write_stl_file(self.aCompound, fileName)
        self.save_part_path = fileName
        self.statusbar.showMessage("零件导出成功")

    except:
        pass
        self.statusBar.showMessage('错误：没用模型可以导出')

def Measure_distance_fun(self):
        pass
        self.measure_signale = 1  # 测量长度
        self.measure_shape_list = []
        self.canva._display.SetSelectionModeNeutral()
        self.canva._display.SetSelectionMode(TopAbs_FACE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_EDGE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_VERTEX) # 设置选择模式
        self.statusbar.showMessage("请选择要测量距离的两个面或者两条边")
def Measure_diameter_fun(self):
        pass
        self.measure_signale = 2  # 测量直径
        self.measure_shape_list = []
        self.canva._display.SetSelectionModeNeutral()
        self.canva._display.SetSelectionMode(TopAbs_FACE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_EDGE)  # 设置选择模式
        self.statusbar.showMessage("请选择圆弧或者圆弧面")
        # print("选择面")