#coding=utf-8
from OCC.Core.AIS import AIS_LengthDimension
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Circle
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopoDS import TopoDS_Builder, TopoDS_Compound, TopoDS_Vertex, TopoDS_Edge, TopoDS_Face
from OCC.Core.gp import gp_Pnt
from OCC.Extend.DataExchange import write_step_file, write_iges_file, write_stl_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import re,sys
import  threading
import os, shutil
from multiprocessing import Process, Queue
from module import Upyun_Update,assemble
import webbrowser
from OCC.Extend.DataExchange import read_iges_file


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


def Output_stp_data(self,mode=1):  # 将数据转换成stp并导出
    try:
        pass
        #self.Translation_Assemble(self=self)
        #self.statusbar.showMessage("零件导出中......")
        path = "../" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.step)")
        self.message.process_message_show()
        QApplication.processEvents()
        write_step_file(self.aCompound, fileName)
        self.save_part_path = fileName
        #self.Assemble_Rename()
        self.statusbar.showMessage("零件导出成功")
        self.message.close()

    except:
        pass
        self.statusbar.showMessage("错误：没用模型可以导出")


def Output_iges_data(self):  # 将数据转换成iges并导出
    try:
        pass
        #self.Translation_Assemble(self=self)
        #self.statusbar.showMessage("零件导出中......")
        path = "./" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.iges)")
        self.message.process_message_show()
        QApplication.processEvents()
        self.statusbar.showMessage("数据生成中请稍后......")
        write_iges_file(self.aCompound, fileName)
        self.save_part_path = fileName
        self.statusbar.showMessage("零件导出成功")
        self.message.close()

    except:
        pass
        self.statusBar.showMessage('错误：没用模型可以导出')


def Output_stl_data(self):  # stl
    try:
        pass
        #self.Translation_Assemble(self=self)
        #self.statusbar.showMessage("零件导出中......")
        path = "./" + self.filename
        fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.stl)")
        self.message.process_message_show()
        QApplication.processEvents()
        write_stl_file(self.aCompound, fileName)
        self.save_part_path = fileName
        self.statusbar.showMessage("零件导出成功")
        self.message.close()

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
def Measure_funtion(self,shp,*args):
    try:
        if self.measure_signale == 1:
            for shape in shp:  # this should be a TopoDS_Edge
                # print(type(shape))
                if shape.IsNull():
                    continue
                elif isinstance(shape, TopoDS_Vertex):
                    point = BRep_Tool.Pnt(shape)
                    self.measure_shape_list.append(point)
                elif isinstance(shape, TopoDS_Edge):
                    select = BRep_Tool.Curve(shape)[0]
                    if not Geom_Circle.DownCast(select):
                        pass
                    else:
                        possible_circle = Geom_Circle.DownCast(select)
                        # 从Geom_Curve向下类型转换为Geom_Circle
                        circle_ = possible_circle.Circ()
                        # 得到gp_Circ类型的圆
                        loc = circle_.Location()  # 圆心， gp_Pnt 类型
                        self.measure_shape_list.append(loc)

                else:
                    self.measure_shape_list.append(shape)

                if len(self.measure_shape_list) == 2:
                    try:
                        if isinstance(self.measure_shape_list[0], gp_Pnt):
                            distance = self.measure_shape_list[0].Distance(self.measure_shape_list[1])
                            measure_result = (distance)

                        else:
                            am = AIS_LengthDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                            # self.canva._display.Context.Display(am,True)
                            measure_result = am.GetValue()

                        measure_result = "测量结果:" + "{:2.2f}".format(measure_result) + "mm"
                        reply = QMessageBox.information(self,  # 使用infomation信息框
                                                        "测量结果",
                                                        str(measure_result),
                                                        QMessageBox.Yes)
                    except:
                        self.statusbar.showMessage("必须选择同样的元素")
                    finally:
                        self.measure_shape_list.clear()

                elif len(self.measure_shape_list) > 2:
                    pass
                    self.measure_shape_list.clear()


        elif self.measure_signale == 2:  # 测量直径
            for shape in shp:  # this should be a TopoDS_Edge
                if shape.IsNull():
                    continue
                else:
                    self.measure_shape_list.append(shape)

                if len(self.measure_shape_list) == 1:
                    try:
                        if isinstance(self.measure_shape_list, TopoDS_Edge):
                            select = BRep_Tool.Curve(self.measure_shape_list[0])[0]
                            if not Geom_Circle.DownCast(select):
                                pass
                            else:
                                possible_circle = Geom_Circle.DownCast(select)
                                # 从Geom_Curve向下类型转换为Geom_Circle
                                circle_ = possible_circle.Circ()
                                # 得到gp_Circ类型的圆
                                loc = circle_.Location()  # 圆心， gp_Pnt 类型
                                radius = circle_.Radius()  # 半径
                                measure_result = radius * 2
                            # am = AIS_RadiusDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                        elif isinstance(self.measure_shape_list[0], TopoDS_Face):
                            for e in TopologyExplorer(self.measure_shape_list[0]).edges():
                                select = BRep_Tool.Curve(e)[0]
                                if not Geom_Circle.DownCast(select):
                                    pass
                                else:
                                    possible_circle = Geom_Circle.DownCast(select)  # 从Geom_Curve向下类型转换为Geom_Circle
                                    circle_ = possible_circle.Circ()  # 得到gp_Circ类型的圆
                                    loc = circle_.Location()  # 圆心， gp_Pnt 类型
                                    radius = circle_.Radius()  # 半径
                                    # print(loc.X(), loc.Y(), loc.Z(), radius)
                                    # ls_point = [loc.X(), loc.Y(), loc.Z(), radius]
                                    measure_result = radius * 2

                                    break

                        measure_result = "测量结果:直径" + "{:2.2f}".format(measure_result) + "mm"
                        reply = QMessageBox.information(self,  # 使用infomation信息框
                                                        "测量结果",
                                                        str(measure_result),
                                                        QMessageBox.Yes)
                    except:
                        self.statusbar.showMessage("必须选择同样的元素")
                    finally:
                        self.measure_shape_list.clear()

                elif len(self.measure_shape_list) > 1:
                    pass
                    self.measure_shape_list.clear()
    except:
        pass
def Put_order_fun(self):
        try:
            sys.path.append("libs")
            self.url = 'http://www.fxjiansuji.com/'
            webbrowser.open(self.url)
        except:
            self.statusbar.showMessage("浏览器打开失败")

def UP_date_software(self, mode=1):  # mode=1 为GUI模式下载  mode=2 则为控制台模式下载
        pass
        mode = 1
        if mode == 1:
            self.process_bar.show()
            try:
                ftp_serve = Upyun_Update.Ftp_Update()
                all_document_num = ftp_serve.get_download_document_num()
                ftp_serve.Delete_Document("./debug")  # 清楚所有原先文件
                os.mkdir("./debug")  # 新建debug文件夹
            except Exception as e:
                pass
            try:
                complete_downloadt_list = []  # 已经完成下载的文件列表
                download_speed_list = []
                t1 = threading.Thread(target=ftp_serve.Check_dir, args=(complete_downloadt_list, download_speed_list,))
                t1.start()
                t2 = threading.Thread(target=self.process_bar.process_bar_show,
                                      args=(complete_downloadt_list, all_document_num, download_speed_list,))
                t2.start()

            except:
                pass
                self.statusbar.showMessage("下载错误，请重新下载")
        if mode == 2:
            try:

                p1 = Process(target=os.system, args=("Upyun_Update.exe",))  # 必须加,号
                p1.start()
                pass
            except:
                self.statusbar.showMessage("下载错误，请重新下载")

def Quit_(self):  # 退出
        self.close()


def Open_file(self):
    try:
        self.chose_document = QFileDialog.getOpenFileName(self, '打开文件', './',
                                                          " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
        filepath = self.chose_document[0]  # 获取打开文件夹路径
        # 判断文件类型 选择对应的导入函数
        end_with = str(filepath).lower()
        if end_with.endswith(".step") or end_with.endswith("stp"):
            self.import_shape, assemble_relation_list = assemble.read_step_file_with_names_colors(filepath)
            self.statusbar.showMessage("数据生成中请稍后......")
            for shpt_lbl_color in self.import_shape:
                label, c, property = self.import_shape[shpt_lbl_color]
                # color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
                if isinstance(shpt_lbl_color, TopoDS_Face):  # 排除非solid
                    continue
                return_shape = self.canva._display.DisplayShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
                                                                                                     c.Green(),
                                                                                                     c.Blue(),
                                                                                                     Quantity_TOC_RGB))
                #self.part_maneger_core_dict[label] = return_shape
            self.statusbar.showMessage("状态：打开成功")  ###
            self.statusBar().showMessage('状态：软件运行正常')
            return assemble_relation_list
        elif end_with.endswith(".iges") or end_with.endswith(".igs"):
            self.import_shape = read_iges_file(filepath)
            self.statusbar.showMessage("状态：打开成功")  ###
            self.statusBar().showMessage('状态：软件运行正常')

    except Exception as e:
        print(e)