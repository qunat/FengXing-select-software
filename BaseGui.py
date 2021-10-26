# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import time
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Circle
from OCC.Display.OCCViewer import OffscreenRenderer
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5 import QtCore, QtWidgets, Qt
from graphics import GraphicsView, GraphicsPixmapItem
from module import Process_message, Process_message_word,SelectModule
from module.CreateParameter import *
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
import re,copy
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication, QUrl
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension, AIS_AngleDimension, AIS_LengthDimension
from OCC.Core.TopAbs import (TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX,
                             TopAbs_SHELL, TopAbs_SOLID)

# ------------------------------------------------------------开始初始化环境
log = logging.getLogger(__name__)


def check_callable(_callable):
    if not callable(_callable):
        raise AssertionError("The function supplied is not callable")


backend_str = None
size = [850, 873]
display_triedron = True
background_gradient_color1 = [212, 212, 212]
background_gradient_color2 = [128, 128, 128]
if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER") == "1":
    # create the offscreen renderer
    offscreen_renderer = OffscreenRenderer()
    def do_nothing(*kargs, **kwargs):
        """ takes as many parameters as you want,
        ans does nothing
        """
        pass
    def call_function(s, func):
        """ A function that calls another function.
        Helpfull to bypass add_function_to_menu. s should be a string
        """
        check_callable(func)
        log.info("Execute %s :: %s menu fonction" % (s, func.__name__))
        func()
        log.info("done")
    # returns empty classes and functions
used_backend = load_backend(backend_str)
log.info("GUI backend set to: %s", used_backend)
# ------------------------------------------------------------初始化结束
from OCC.Display.qtDisplay import qtViewer3d
from PyQt5.QtGui import QPixmap, QFont, QBrush, QMovie, QIcon, QCursor
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Builder, TopoDS_Compound, topods_CompSolid, TopoDS_Edge, TopoDS_Face,\
TopoDS_Vertex

from OCC.Extend.DataExchange import read_iges_file, read_step_file, read_stl_file, write_step_file, write_stl_file, \
    write_iges_file
from PyQt5.QtWidgets import QComboBox, QPushButton, QHBoxLayout, QMdiArea, QMdiSubWindow, QTextEdit, QApplication, \
    QFileDialog, QProgressBar, QMessageBox, QTableView, QDockWidget, QListWidget
import sys
import webbrowser
from  module import Ftp_Update, Upyun_Update, Vision, AboutDownload,MainGui, ShowGui,ProcessBar
import  threading
import os, shutil
from multiprocessing import Process, Queue

Stylesheet = """
#MainWindow {

    border-radius: 10px;
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
"""


class Mywindown(QtWidgets.QMainWindow, ShowGui.Ui_MainWindow,MainGui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindown, self).__init__(parent)
        # 3D显示设置
        self.setWindowTitle("枫信自动化选型软件测试版")
        self.setFixedSize(self.desktop.width(), self.desktop.height())
        self.vision = "1.0.1"
        self.measure_signale = 0  # 测量类型的型号
        self.process_bar = Process_Bar()
        self.process_message = Process_message()
        self.process_message_word = Process_message_word()
        self.new_vison = Vision()
        self.new_AboutDownload = AboutDownload()
        self.centerOnScreen()
        # ----------------------------------------------------------------------------------
        self.sinal = 0
        self.tabWidget_5.currentChanged['int'].connect(self.Refresh)  # 切换时刷新
        self.Out_put_stp.triggered.connect(self.Output_stp_data)
        self.Out_put_iges.triggered.connect(self.Output_iges_data)
        self.Out_put_stl.triggered.connect(self.Output_stl_data)
        # -----------------------------------------------------------------------------------采购下单
        self.Put_order.triggered.connect(self.Put_order_fun)
        self.Up_data.triggered.connect(self.UP_date_software)
        # -------------------------------------------------------------------------------------视图操作
        self.Quit.triggered.connect(self.Quit_)
        self.actionView_Right.triggered.connect(self.View_Right)
        self.actionView_Left.triggered.connect(self.View_Left)
        self.actionView_Top.triggered.connect(self.View_Top)
        self.actionView_Bottom.triggered.connect(self.View_Bottom)
        self.actionView_Front.triggered.connect(self.View_Front)
        self.actionView_Iso.triggered.connect(self.View_Iso)
        self.action_Fitall.triggered.connect(self.View_fitall)

        #-------------------------------------------------------------------------------------右键单击菜单
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 606*self.width_scal, 26*self.height_scal))
        self.menuBar.setObjectName("menuBar")
        self.canva.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.canva.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)

        # -----------------------------------------------------------------------------------版本更新提示
        try:
            now_vision = self.get_now_vision()
            now_notes = self.get_now_notes()
            if True:
                if self.vision != now_vision:
                    message = "V" + now_vision + "版本可供下载" + "(" + now_notes + ")"
                    self.statusbar.showMessage(message)

        except:
            pass
        # -------------------------------------------------------------------------------------测量菜单
        self.Measure_distance.triggered.connect(self.Measure_distance_fun)
        self.Measure_diameter.triggered.connect(self.Measure_diameter_fun)
        # -------------------------------------------------------------------------------------自定义信号和槽
        Measure_distance_signal = pyqtSignal()
        Measure_diameter_signal = pyqtSignal()
        # --------------------------------------------------------------------------------------显示软件版本
        self.AboutVision.triggered.connect(self.Vision)
        self.AboutDownload.triggered.connect(self.AboutDownload_)

    def View_Bottom(self):
        pass
        self.canva._display.View_Bottom()

    def View_Front(self):
        pass
        self.canva._display.View_Front()

    def View_Iso(self):
        pass
        self.canva._display.View_Iso()

    def View_Left(self):
        pass
        self.canva._display.View_Left()

    def View_Right(self):
        pass
        self.canva._display.View_Right()

    def View_Top(self):
        pass
        self.canva._display.View_Top()

    def View_fitall(self):
        pass
        self.canva._display.FitAll()

    def doubleClickedHandle(self, index):
        text = self.model().item(index.row(), 0).text()
        self.doubleClickedItem.emit(text)

    def outSelect(self, Item=None):
        if Item == None:
            return

    def Refresh(self):
        self.canva._display.Repaint()
        self.graphicsView.show()

    def Show_gui(self, index=0):
        self.stackedWidget.setCurrentIndex(index)
        # self.stackedWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.statusbar.showMessage("状态：软件运行正常")

    def Show_gui_text(self, index=0):
        self.stackedWidget.setCurrentIndex(index)
        self.tabWidget_5.update()

    def Ceate_product_parameter_table_and_show_3d(self, QClor=1, dict={}, start=0, ):  # 生成/更新产品参数表格
        '''
        根据combox选项生成产品参数列表
        '''
        SelectModule.Create_product_parameter_table_and_show_3d(self=self, dict=dict)
    def Ceate_show_3d(self, QClor=1, dict={}, start=0, ):#仅更新3D
        #根据combox选项生成产品参数列表
        SelectModule.Ceate_show_3d(self)


    def Ceate_combox_table(self, ButtonId=None):  # 生成选项卡表格
        '''
        1.建立选型列表名称
        2.获取各个选项的值
        3.
        '''
        SelectModule.Ceate_combox_table(self=self,ButtonId=ButtonId)

    def choose(self):
        if self.stackedWidget.currentIndex() == 1:
            pass

    def show_parameter(self, filepath=None):  # 切换到参数画面
        self.stackedWidget.setCurrentIndex(0)
        self.tab_7.show()
        QApplication.processEvents()
        self.canva._display.Repaint()

    def Create_ProcessBar(self, ButtonId=None):  # 过程处理函数 获取数据生成所需的界面
        try:
            # -----------------清空3D显示界面
            self.statusbar.showMessage("状态：软件运行正常")
            self.canva._display.EraseAll()
            self.canva._display.hide_triedron()
            self.canva._display.display_triedron()
            self.canva._display.Repaint()
            # ------------------------------
            self.message = Process_message()  #
            self.tableWidget_2.clear()  # 清空原来的数据
            self.tableWidget_2.clearSpans()

            self.tableWidget_2.setHorizontalHeaderLabels(['选项', '列表值', '备注'])
            textFont = QFont()
            textFont.setFamily("微软雅黑")
            textFont.setPointSize(11)
            self.tableWidget_2.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑  # 表格不可编辑
            # 选型
            headItem = self.tableWidget_2.horizontalHeaderItem(0)  # 获得水平方向表头的Item对象
            headItem.setFont(textFont)  # 设置字体
            brush = QtGui.QBrush(QtGui.QColor(85, 85, 255))
            headItem.setForeground(brush)  # 设置文字颜色
            # 列表值
            headItem = self.tableWidget_2.horizontalHeaderItem(1)  # 获得水平方向表头的Item对象
            headItem.setFont(textFont)  # 设置字体
            brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
            headItem.setForeground(brush)  # 设置文字颜色
            # 备注
            headItem = self.tableWidget_2.horizontalHeaderItem(2)  # 获得水平方向表头的Item对象
            headItem.setFont(textFont)  # 设置字体
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
            headItem.setForeground(brush)  # 设置文字颜色
            if "KS系列(孔输出) " in ButtonId :
                self.ButtonId = ButtonId
                self.Ceate_combox_table(ButtonId)#建立
                # 将所有的combox 选项和型号槽绑定 只要选项更新就会选项产品参数
                for i in self.combox_list:
                    if self.combox_list.index(i)==7:
                        i.currentTextChanged.connect(self.Ceate_show_3d)#刷新
                        continue
                    i.currentTextChanged.connect(self.Ceate_product_parameter_table_and_show_3d)#刷新
            self.sinal = 1
            self.message.process_message_show()
        except Exception as e:
            print(e)

        if True:
            if self.sinal == 1:
                try:
                    pass
                except:
                    pass
                self.show_parameter()
                self.sinal = 0
                self.message.close()
                # break

    def Show3D(self, mode=0, file=None, aCompound=None):  # 生成3D mode控制显示模式
        try:
            self.canva._display.EraseAll()
            self.canva._display.hide_triedron()
            self.canva._display.display_triedron()
            self.canva._display.Repaint()
            if mode == 0:
                shapes_labels_colors = read_step_file_with_names_colors(file)
                self.statusbar.showMessage("数据生成中请梢后......")
                self.aCompound=shapes_labels_colors
                for shpt_lbl_color in shapes_labels_colors:
                    label, c = shapes_labels_colors[shpt_lbl_color]
                    for e in TopologyExplorer(shpt_lbl_color).solids():
                        pass
                        self.canva._display.DisplayColoredShape(e, color=Quantity_Color(c.Red(),
                                                                                        c.Green(),
                                                                                        c.Blue(),
                                                                                        Quantity_TOC_RGB))
            elif mode == 1:

                self.show = self.canva._display.DisplayColoredShape(aCompound, color="WHITE", update=True)

        except:
            pass
            self.statusbar.showMessage("没有此零件")

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

    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)

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
    def line_clicked(self, shp, *kwargs):
        """ This function is called whenever
        """
        try:
            if self.measure_signale == 1:
                for shape in shp:  # this should be a TopoDS_Edge
                    # print(type(shape))
                    if shape.IsNull():
                        continue
                    elif isinstance(shape,TopoDS_Vertex):
                        point = BRep_Tool.Pnt(shape)
                        self.measure_shape_list.append(point)
                    elif isinstance(shape,TopoDS_Edge):
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
                            if isinstance(self.measure_shape_list[0],gp_Pnt):
                                distance=self.measure_shape_list[0].Distance(self.measure_shape_list[1])
                                measure_result=(distance)

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


            elif self.measure_signale == 2:#测量直径
                for shape in shp:  # this should be a TopoDS_Edge
                    if shape.IsNull():
                        continue
                    else:
                        self.measure_shape_list.append(shape)

                    if len(self.measure_shape_list) == 1:
                        try:
                            if isinstance(self.measure_shape_list,TopoDS_Edge):
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
                            elif isinstance(self.measure_shape_list[0],TopoDS_Face):
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
                                        #ls_point = [loc.X(), loc.Y(), loc.Z(), radius]
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

    def rightMenuShow(self):
        try:
            if True :
                rightMenu = QtWidgets.QMenu(self.menuBar)
                self.actionreboot = QtWidgets.QAction(self.canva)
                self.actionreboot.setObjectName("actionreboot")
                self.actionreboot.setText(QtCore.QCoreApplication.translate("MainWindow", "距离测量"))


                self.actionreboot_1 = QtWidgets.QAction(self.canva)
                self.actionreboot_1.setObjectName("actionreboot_1")
                self.actionreboot_1.setText(QtCore.QCoreApplication.translate("MainWindow", "孔径测量"))


                rightMenu.addAction(self.actionreboot)
                rightMenu.addAction(self.actionreboot_1)

                self.actionreboot.triggered.connect(self.Measure_distance_fun)
                self.actionreboot_1.triggered.connect(self.Measure_diameter_fun)

                rightMenu.exec_(QtGui.QCursor.pos())


        except Exception as e:
            print(e)
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

    def get_now_vision(self):
        ftp_serve = Upyun_Update.Ftp_Update()
        ftp_serve.Down_load_file("serve/serve.ini")
        with open("./serve/serve.ini", "r") as f:
            words = f.readlines()
            self.now_vision = words[0].replace("vision=", "").strip("\n")
            f.close()

        return self.now_vision

    def get_now_notes(self):
        # ftp_serve = Upyun_Update.Ftp_Update()
        # ftp_serve.Down_load_file("serve/serve.ini")
        with open("./serve/serve.ini", "r") as f:
            words = f.readlines()
            self.notes = words[-1].replace("notes=", "").strip("\n")
            f.close()

        return self.notes

    def Process_message(self):
        self.process_message = Process_message()
        self.process_message.show()
        QApplication.processEvents()

    def Quit_(self):  # 退出
        self.close()

    def Vision(self):
        pass
        self.new_vison.show()

    def AboutDownload_(self):
        self.new_AboutDownload.show()


class Vision(QtWidgets.QMainWindow, Vision.Ui_Form):
    def __init__(self, parent=None):
        super(Vision, self).__init__(parent)
        self.setupUi(self)
        self.label_6.setText("<A href='https://www.aliyuncad.com/'>软件下载：https://www.aliyuncad.com/</a>")
        self.label_6.setOpenExternalLinks(True)


class AboutDownload(QtWidgets.QMainWindow, AboutDownload.Ui_Form):
    def __init__(self, parent=None):
        super(AboutDownload, self).__init__(parent)
        self.setupUi(self)


class Process_message(QtWidgets.QMainWindow, Process_message.Ui_Form):  # 零件加载过程界面
    def __init__(self, parent=None):
        super(Process_message, self).__init__(parent)
        self.setupUi(self)
        # self.pushButton=QtWidgets.QPushButton()
        # self.pushButton.setGeometry(0,0,10,10)

    def process_message_show(self):
        pass
        self.label.setObjectName("label")
        self.gif = QMovie(':/picture/icons/loading.gif')
        self.label.setMovie(self.gif)
        self.gif.start()
        self.show()


class Process_message_word(QtWidgets.QMainWindow, Process_message_word.Ui_Form):  # 零件加载过程界面
    def __init__(self, parent=None):
        super(Process_message_word, self).__init__(parent)
        self.setupUi(self)
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setGeometry(0, 0, 10, 10)


class Process_Bar(QtWidgets.QMainWindow, ProcessBar.Ui_Form):  # 下载处理进度条
    def __init__(self, parent=None):
        super(Process_Bar, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("下载")
        self.setWindowIcon(QIcon(':/picture/icons/download.ico'))

    def process_bar_show(self, complete_downloadt_list, all_document_num, speed_list):
        while True:
            try:

                percent = len(complete_downloadt_list) / all_document_num * 100
                if percent > 0:
                    self.label_5.setText("链接成功，正在下载")
                self.progressBar.setValue(int(percent))
                speed = speed_list[-1]

                if speed < 1:
                    ls_speed = speed * 1024
                    speed = "{:.2f}".format(ls_speed)
                    speed = str(speed) + "KB/s"
                else:
                    speed = "{:.2f}".format(speed_list[-1])
                    speed = str(speed) + "M/s"

                self.label_3.setText(speed)
                if int(percent) == 99:
                    self.progressBar.setValue(int(100))
                    self.label_5.setText("下载完成！")
                    time.sleep(3)
                    break
            except:
                pass
        '''

        '''
        self.close()
        sys.exit()


def line_clicked(shp, *kwargs):
    """ This function is called whenever a line is selected
    """


# following couple of lines is a tweak to enable ipython --gui='qt'
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    # 启动界面
    try:
        splash = QtWidgets.QSplashScreen(QtGui.QPixmap(":/picture/Pic/setup_pic.jpg"))  # 启动图片设置
        splash.show()
        splash.showMessage("软件启动中......")
    except:
        pass
    # --------------------
    win = Mywindown()
    win.show()
    win.centerOnScreen()
    win.canva.InitDriver()
    win.resize(size[0], size[1])
    win.canva.qApp = app

    display = win.canva._display
    display.display_triedron()
    display.register_select_callback(win.line_clicked)
    if background_gradient_color1 and background_gradient_color2:
        # background gradient
        display.set_bg_gradient_color(background_gradient_color1, background_gradient_color2)
    win.raise_()  # make the application float to the top
    win.showMaximized()

    try:
        splash.finish(win)
    except:
        pass
    app.exec_()
