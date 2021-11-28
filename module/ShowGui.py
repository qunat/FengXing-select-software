# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Extend.DataExchange import read_iges_file
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QCursor,QKeySequence as QKSec
from GUI.Icons import get_icon
from GUI.RibbonButton import RibbonButton
from GUI.RibbonTextbox import RibbonTextbox
from GUI.RibbonWidget import RibbonWidget

from ui import MainGui,Vision
from module.QSS import *
import os
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView,
                             QComboBox, QPushButton, QDockWidget, QListWidget)
from PyQt5.QtCore import QSettings, QDateTime, Qt, QUrl
from functools import partial
from graphics import GraphicsView, GraphicsPixmapItem
from PyQt5.QtCore import  Qt
from GUI.RibbonWidget import *
from module.FuctionModule import *




class Ui_MainWindow(MainGui.Ui_MainWindow):
    def __init__(self):
        self.setupUi(self)
        self.canva = qtViewer3d(self.tab_7)  # 链接3D模块
        self.pushButton = {}  # 按件字典
        self.label_ = {}  # 标签字典
        self.serise_path = {}
        self.page = {}
        self.tabWidget_ = {}
        self.tab = {}
        self.widget = {}
        self.scroll = {}
        self.vbox = {}
        self.layoutWidget = {}
        self.gridLayout = {}
        self.new_vison = Vision()

        # -------------      actions       -----------------
        self._open_action = self.add_action("打开", "open", "打开", True, self.on_open_file, QKSec.Open)
        self._exit_action = self.add_action("退出", "exit", "退出", True,partial(Quit_,self))
        self._copy_action = self.add_action("Copy", "copy", "Copy selection", True, self.on_copy, QKSec.Copy)
        self._paste_action = self.add_action("Paste", "paste", "Paste from clipboard", True, self.on_paste, QKSec.Paste)
        self._zoom_action = self.add_action("Zoom", "zoom", "Zoom in on document", True, self.on_zoom)
        self._about_action = self.add_action("About", "about", "About QupyRibbon", True, self.on_about)
        self._license_action = self.add_action("License", "license", "Licence for this software", True, self.on_license)
        self.actionView_Right= self.add_action("右视图","view-right","右视图",True,self.View_Right)
        self.actionView_Left= self.add_action("左视图","view-left","左视图",True,self.View_Left)
        self.actionView_Top= self.add_action("上视图","view-top","上视图",True,self.View_Top)
        self.actionView_Bottom= self.add_action("下视图","view-bottom","下视图",True,self.View_Bottom)
        self.actionView_Front= self.add_action("主视图","view-front","主视图",True,self.View_Front)
        self.actionView_Rear = self.add_action("后视图", "view-rear", "后视图", True, self.View_Rear)
        self.actionView_Iso= self.add_action("轴测图","view-isometric","轴测图",True,self.View_Iso)
        self.action_Fitall= self.add_action("全显","zoom-all","全显",True,self.View_fitall)
        self.action_Export_STP = self.add_action("导出STP", "Std_Export", "导出STP", True,partial(Output_stp_data,self=self))
        self.action_Export_IGES = self.add_action("导出IGES", "Std_Export", "导出IGES", True, partial(Output_iges_data,self=self))
        self.action_Export_STL = self.add_action("导出STL", "Std_Export", "导出STL", True,partial(Output_stl_data,self=self))
        self.action_Measure_distance_tool = self.add_action("距离测量", "view-measurement", "距离测量", True, partial(Measure_distance_fun,self=self))
        self.action_Measure_diameter_tool = self.add_action("孔径测量", "view-measurement", "孔径测量", True, partial(Measure_diameter_fun,self=self))
        self.action_download = self.add_action("下载更新", "download", "下载更新", True, partial(UP_date_software,self))
        self.action_purchase = self.add_action("采购下单", "purchase", "采购下单", True, partial(Put_order_fun,self))
        self.action_about_software = self.add_action("版本信息", "about", "版本信息", True, self.Vision)
        # -------------      textboxes       -----------------

        self._text_box1 = RibbonTextbox("Text 1", self.on_text_box1_changed, 80)
        self._text_box2 = RibbonTextbox("Text 2", self.on_text_box1_changed, 80)
        self._text_box3 = RibbonTextbox("Text 3", self.on_text_box1_changed, 80)

        # Ribbon

        self._ribbon = RibbonWidget(self)
        self.addToolBar(self._ribbon)
        self.init_ribbon()
        ribbin_offset_X=self._ribbon.width()
        ribbin_offset_Y=76#减去ribbonde高度


        all_kinds_path = os.listdir("./Pic")
        self.tabWidget_5.tabBar().setTabTextColor(0,QtGui.QColor(0,0,0))#tabwidget字体颜色设置
        self.tabWidget_5.tabBar().setTabTextColor(1, QtGui.QColor(0, 0, 0))#tabwidget字体颜色设置
        self.tabWidget_5.tabBar().setTabTextColor(2, QtGui.QColor(0, 0, 0))#tabwidget字体颜色设置
        self.tabWidget_5.tabBar().setTabTextColor(3, QtGui.QColor(0, 0, 0))  # tabwidget字体颜色设置

        self.tabWidget_4.tabBar().setTabTextColor(0, QtGui.QColor(0, 0, 0))  # tabwidget字体颜色设置
        self.tabWidget_4.tabBar().setTabTextColor(1, QtGui.QColor(0, 0, 0))  # tabwidget字体颜色设置



        #初始屏幕大小
        origin_height=self.geometry().height()
        origin_width=self.geometry().width()
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        # 将窗口放置在中央小控件的右侧
        self.screenRect = self.desktop.availableGeometry()
        self.height1 = self.screenRect.height()
        self.width1 = self.screenRect.width()
        self.height_scal=self.height1/origin_height#缩放比例
        self.width_scal=self.width1/origin_width#缩放比例
        X=self.width_scal
        Y=self.height_scal
        #自动调整大小
        self.canva.setGeometry(QtCore.QRect(0, 0, 468 * X, (581-ribbin_offset_Y) * Y))

        x=self.stackedWidget.geometry().x()*X
        y=self.stackedWidget.geometry().y()*Y
        width=self.stackedWidget.geometry().width()*X
        height=self.stackedWidget.geometry().height()*Y-ribbin_offset_Y*Y
        self.stackedWidget.setGeometry(QtCore.QRect(x, y, width, height))

        x = self.tabWidget.geometry().x() * X
        y = self.tabWidget.geometry().y() * Y
        width = self.tabWidget.geometry().width() * X
        height = self.tabWidget.geometry().height() * Y-ribbin_offset_Y*Y
        self.tabWidget.setGeometry(QtCore.QRect(x, y, width, height))

        x = self.tabWidget_4.geometry().x() * X
        y = self.tabWidget_4.geometry().y() * Y
        width = self.tabWidget_4.geometry().width() * X
        height = self.tabWidget_4.geometry().height() * Y-ribbin_offset_Y*Y
        self.tabWidget_4.setGeometry(QtCore.QRect(x, y, width, height))

        x = self.tableWidget_2.geometry().x() * X
        y = self.tableWidget_2.geometry().y() * Y
        width = self.tableWidget_2.geometry().width() * X
        height = self.tableWidget_2.geometry().height() * Y-ribbin_offset_Y*Y
        self.tableWidget_2.setGeometry(QtCore.QRect(x, y, width, height))

        x = self.tableWidget.geometry().x() * X
        y = self.tableWidget.geometry().y() * Y
        width = self.tableWidget.geometry().width() * X
        height = self.tableWidget.geometry().height() * Y-ribbin_offset_Y*Y
        self.tableWidget.setGeometry(QtCore.QRect(x, y, width, height))

        x = self.tabWidget_5.geometry().x() * X
        y = self.tabWidget_5.geometry().y() * Y
        width = self.tabWidget_5.geometry().width() * X
        height = self.tabWidget_5.geometry().height() * Y-ribbin_offset_Y*Y
        self.tabWidget_5.setGeometry(QtCore.QRect(x, y, width, height))
        self.tab_3.setStyleSheet("background-color: rgb(176, 176, 176)")
        self.tab_4.setStyleSheet("background-color: rgb(176, 176, 176)")
        self.tab_8.setStyleSheet("background-color: rgb(176, 176, 176)")
        #self.tableWidget_2.setStyleSheet("background-color: rgb(240, 240, 240)")

        #x = self.menubar.geometry().x() * X
        #y = self.menubar.geometry().y() * Y
        #width = self.menubar.geometry().width() * X
        #height = self.menubar.geometry().height() * Y-ribbin_offset_Y*Y
        #self.menubar.setGeometry(QtCore.QRect(x, y, width, height))



        #表格平均分配
        blank_size = self.tableWidget_2.geometry().width() / 3
        self.tableWidget_2.setColumnWidth(1, blank_size)  # 手动设置列宽
        self.tableWidget_2.setColumnWidth(0, blank_size)  # 手动设置列宽
        self.tableWidget_2.setColumnWidth(2, blank_size)  # 手动设置列宽

        for j in all_kinds_path:
            try:
                if "." in j:
                    continue
                self.page[j] =QtWidgets.QWidget()
                self.tabWidget_[j] =QtWidgets.QTabWidget(self.page[j])
                self.tab[j] = QtWidgets.QWidget()
                self.widget[j] =QtWidgets.QWidget(self.tab[j])
                self.scroll[j] =QtWidgets.QScrollArea()
                self.vbox[j] =QtWidgets.QVBoxLayout()
                self.layoutWidget[j] = QtWidgets.QWidget(self.widget[j])
                self.gridLayout[j] = QtWidgets.QGridLayout(self.layoutWidget[j])
                self.stackedWidget.addWidget(self.page[j])

            except:
                pass
                print("ERROR")

        self.CreateTree()#零件树
        self.Create_page()#page

        self.items = QDockWidget('零件目录', self)#新建QDockWidget
        self.items2 = QDockWidget('功能区', self)#新建QDockWidget
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)#在主显示区域右侧显示
        self.addDockWidget(Qt.LeftDockWidgetArea, self.items2)#在主显示区域左侧显示
        self.items.setMaximumWidth(self.width1-self.stackedWidget.geometry().width())#设置最小大小


        #界面布局
        self.items.setWidget(self.widget_Tree)
        self.setCentralWidget(self.stackedWidget)
        self.items2.setWidget(self.stackedWidget)

        #自动生成界面-1
        try:
            pass
            all_kinds_path = os.listdir("./Pic")
            ls_all_kinds_path = []  # 临时变量 存储all_kinds_path
            for i in all_kinds_path:
                if "." in i:
                    continue
                ls_all_kinds_path.append(i)  # 剔除非文件夹文件

            all_kinds_path = ls_all_kinds_path  # 复制

            for i in all_kinds_path:
                index = all_kinds_path.index(i) + 1
                # print(i,index)
                self.pushButton[i].clicked.connect(partial(self.Show_gui, index))  # 实时传递数值
                kinds_path = os.listdir("./Pic/" + i)
                for j in kinds_path:
                    if "系列" in i and False:
                        pass
                        ls_str = j.split(".")
                        dic = ls_str[2] + ls_str[3]
                        self.pushButton[j].clicked.connect(partial(self.Create_ProcessBar, dic))  # 实时传递数值 程序运行入口
                        # self.pushButton[j].setCursor(QCursor(Qt.PointingHandCursor))
                    else:
                        pass
                        ls_str = j.split(".")
                        dic = ls_str[0]
                        self.pushButton[j].clicked.connect(partial(self.Create_ProcessBar, dic))  # 实时传递数值 程序运行入口
                        # self.pushButton[j].setCursor(QCursor(Qt.PointingHandCursor))
        except:
            pass

        # ------------------------------------------------------------尺寸数据显示设置
        try:
            pass
            self.pix = QPixmap('Pic/FX.png')
            self.graphicsView = GraphicsView(self.pix, self.tab_8)
            self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461 * self.width_scal, 581 * self.height_scal))
            self.graphicsView.setObjectName("graphicsView")
            self.graphicsView.scale(1, 1)  # 显示比例
            self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
            self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例22
            self.scene.addItem(self.item)
        except:
            pass



    def Create_meau(self,
                    index=0,
                    Number_columns=7,
                    picture_width=150,
                    picture_interval=16,
                    picture_height=156,
                    pic_label_interval=10,
                    icon_widrh=130,
                    icom_height=130,
                    serie_path=None,
                    page=None,
                    tabWidget=None,
                    tab=None,
                    widget=None,
                    scroll=None,
                    vbox = None,
                    layoutWidget=None,
                    gridLayout=None
                    ):

        X = self.width_scal
        Y = self.height_scal
        fun=lambda x, y: x if x > y else y
        # 循环建立菜单图片+文字描述
        # ---第一步获取对应文件夹里的内容 确定button数量
        file_path_list = []
        file_path_list = os.listdir(serie_path)
        #--------------------------自动计算一排最多有多少个picture--------------------------------------------------
        width=781*X

        for i in [5,6,7,8]:
            try:
                if (i*picture_width+(i+1)*picture_interval)<width and ((i+1)*picture_width+(i+2)*picture_interval)>width:
                    Number_columns=i

                if len(file_path_list)<Number_columns:
                    Number_columns=len(file_path_list)
                break
            except:
                pass
        #确定行数
        #print(Number_columns)
        if len(file_path_list)<=Number_columns:
            ls_column=1
            x_lengh = ls_column * (picture_height+picture_interval)#原值166
        elif len(file_path_list)%Number_columns==0:
            ls_column = int(len(file_path_list) / Number_columns)
            x_lengh=ls_column*(picture_width+picture_interval)#原值166
        else:
            x_lengh = (int(len(file_path_list) / Number_columns) + 1) *(picture_width+picture_interval)#166QRect长度

        y = 0  # QRect宽度
        # 设置图片路径
        QPixmap_path = serie_path
        # 循环建立控件
        row = 0
        column = 0

        #tabWidget = QtWidgets.QTabWidget(page)
        tabWidget.setGeometry(QtCore.QRect(10, 10, 781*X, 631*Y))
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(12)

        tabWidget.setFont(font)
        tabWidget.setStyleSheet("")
        tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        tabWidget.setObjectName("tabWidget")

        #tab = QtWidgets.QWidget()
        tab.setObjectName("tab")

        #widget = QtWidgets.QWidget(tab)
        widget.setGeometry(QtCore.QRect(0, 0, 781*X, fun(800,x_lengh)*Y))
        widget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        widget.setStyleSheet("background-color: rgb(216, 216, 216);")
        widget.setObjectName("widget")
        # 判断是否需要有滑条
        # ------------------------------------------------------------滚动条1.0
        widget.setMinimumSize(0, x_lengh+100)  # 设置滚动范围
        #scroll = QtWidgets.QScrollArea()  # 创建滚动类
        scroll.setWidget(widget)  # 设置滚动区域为self.widget
        #vbox = QtWidgets.QVBoxLayout()  # 创建布局
        vbox.addWidget(scroll)  # 增加布局内容
        tab.setLayout(vbox)  #
        # ------------------------------------------------------------滚动条1.0



        #layoutWidget = QtWidgets.QWidget(widget)
        if len(file_path_list)<=Number_columns:
            layoutWidget_x=len(file_path_list)*(picture_width+picture_interval)
            x_lengh=(picture_width+picture_interval)*1
            layoutWidget.setGeometry(QtCore.QRect(10, 10, layoutWidget_x, x_lengh))

        else:
            layoutWidget.setGeometry(QtCore.QRect(10, 10, 750*X, x_lengh))


        layoutWidget.setObjectName("layoutWidget")
        #gridLayout = QtWidgets.QGridLayout(layoutWidget)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setObjectName("gridLayout")
        pbstyle='''
                background-color: rgb(255, 255, 255);\n
                border:1px solid gray;\n
                        width:300px;\n
                        border-radius:10px;\n
                        padding:2px 4px;\n
                border-color: rgb(61, 61, 61);
                
                '''


        for i in range(len(file_path_list)):
            self.pushButton[file_path_list[i]]=QtWidgets.QPushButton(layoutWidget)
            self.pushButton[file_path_list[i]].setMaximumSize(QtCore.QSize(picture_width, picture_height))
            self.pushButton[file_path_list[i]].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.pushButton[file_path_list[i]].setStyleSheet(pbstyle)
            self.pushButton[file_path_list[i]].setText("")
            self.pushButton[file_path_list[i]].setCursor(QCursor(Qt.PointingHandCursor))
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(QPixmap_path,file_path_list[i])),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton[file_path_list[i]].setIcon(icon)
            self.pushButton[file_path_list[i]].setIconSize(QtCore.QSize(icon_widrh, icom_height))
            self.pushButton[file_path_list[i]].setObjectName(file_path_list[i])
            if i%Number_columns==0 and i>=Number_columns:
                row+=2
                column=0
            gridLayout.addWidget(self.pushButton[file_path_list[i]], row, column, 1, 1)
            font = QtGui.QFont()
            font.setFamily("微软雅黑")
            font.setPointSize(9)
            font.setBold(False)
            font.setItalic(False)
            font.setWeight(50)
            if file_path_list[i].endswith("png"):
                pass
                label_name="型号："+file_path_list[i].strip(".png")
            elif file_path_list[i].endswith("jpg"):
                pass
                label_name = "型号：" + file_path_list[i].strip(".jpg")
            self.label_[file_path_list[i]] = QtWidgets.QLabel(layoutWidget)
            self.label_[file_path_list[i]].setFont(font)
            self.label_[file_path_list[i]].setLayoutDirection(QtCore.Qt.RightToLeft)
            self.label_[file_path_list[i]].setAlignment(QtCore.Qt.AlignCenter)
            self.label_[file_path_list[i]].setObjectName(file_path_list[i])
            self.label_[file_path_list[i]].setText(label_name)
            gridLayout.addWidget(self.label_[file_path_list[i]], row+1, column, 1, 1)

            column += 1


        tabWidget.addTab(tab, "图表")
        font.setPointSize(12)
        tabWidget.setFont(font)
        #self.retranslateUi(page)
        QtCore.QMetaObject.connectSlotsByName(page)
        tabWidget.setCurrentIndex(0)

    def Create_page(self):
        all_kinds_path=os.listdir("./Pic")
        for j in all_kinds_path:
            pass
            if "." in j:
                continue
            path="./Pic/"+j
            self.Create_meau(index=all_kinds_path.index(j),serie_path=path,page=self.page[j],tabWidget=self.tabWidget_[j],tab=self.tab[j], widget=self.widget[j],
                             scroll=self.scroll[j], vbox=self.vbox[j], layoutWidget=self.layoutWidget[j],gridLayout=self.gridLayout[j])


    def CreateTree(self):
        pass
        X=self.width_scal
        Y=self.height_scal
        x1=self.width1-self.stackedWidget.geometry().width()*1.027
        y1=self.stackedWidget.geometry().height()
        self.widget_Tree = QtWidgets.QWidget(self.centralwidget)
        #self.widget_Tree.setGeometry(QtCore.QRect((810+5)*X, (130-7)*Y, (211)*X, (800)*Y))
        self.widget_Tree.setMinimumHeight(y1)
        self.widget_Tree.setObjectName("widget_Tree")
        self.widget_Tree_2 = QtWidgets.QWidget(self.widget_Tree)
        self.widget_Tree_2.setGeometry(QtCore.QRect(0, 0, x1, y1))
        self.widget_Tree_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_Tree_2.setAutoFillBackground(False)
        self.widget_Tree_2.setObjectName("widget_Tree_2")
        self.formLayoutWidget_Tree_2 = QtWidgets.QWidget(self.widget_Tree_2)
        self.formLayoutWidget_Tree_2.setGeometry(QtCore.QRect(0, 0, x1, y1))
        self.formLayoutWidget_Tree_2.setObjectName("formLayoutWidget_Tree_2")
        self.formLayout_Tree_2 = QtWidgets.QFormLayout(self.formLayoutWidget_Tree_2)
        self.formLayout_Tree_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_Tree_2.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout_Tree_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_Tree_2.setSpacing(0)
        self.formLayout_Tree_2.setObjectName("formLayout_Tree_2")

        #建立pubuttton树
        # ---第一步获取对应文件夹里的内容 确定button数量
        file_path_list = []
        file_path_list = os.listdir("./Pic")

        # -------------------------------------------------------------------------设置滚动条
        self.widget_Tree_2.setMinimumSize(0, len(file_path_list)*35)  # 设置滚动范围
        self.scroll_Tree_2 = QtWidgets.QScrollArea()  # 创建滚动类
        self.scroll_Tree_2.setWidget(self.widget_Tree_2)  # 设置滚动区域为self.widget

        self.vbox2_Tree_2 = QtWidgets.QVBoxLayout()  # 创建布局
        self.vbox2_Tree_2.addWidget(self.scroll_Tree_2)  # 增加布局内容
        self.widget_Tree.setLayout(self.vbox2_Tree_2)  #
        #---------------------------------------------------
        #设置butthon字体
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(12)
        #循环建立pubutton
        for i in range(len(file_path_list)):
            if "." in file_path_list[i]:
                continue
            #print(file_path_list[i])
            self.pushButton[file_path_list[i]] = QtWidgets.QPushButton(self.formLayoutWidget_Tree_2)
            self.pushButton[file_path_list[i]].setMinimumSize(QtCore.QSize(90, 30))
            self.pushButton[file_path_list[i]].setFont(font)
            self.pushButton[file_path_list[i]].setStyleSheet(
                "border:none;background-color: qlineargradient(spread:pad, x1:0.336, y1:1, x2:0.54, y2:0, stop:0 rgba(155, 155, 155, 255), stop:1 rgba(255, 255, 255, 255));\n"
                "")
            self.pushButton[file_path_list[i]].setObjectName(file_path_list[i])
            self.formLayout_Tree_2.setWidget(i, QtWidgets.QFormLayout.FieldRole, self.pushButton[file_path_list[i]])
            self.pushButton[file_path_list[i]].setText(file_path_list[i])
            self.pushButton[file_path_list[i]].setStyleSheet(butstyle)



    def Vision(self):
        pass
        self.new_vison.show()

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
    def View_Rear(self):
        pass
        self.canva._display.View_Rear()

    def View_fitall(self):
        pass
        self.canva._display.FitAll()

    #ribbom function
    def closeEvent(self, close_event):
        pass

    def on_open_file(self):
        Open_file(self=self)
    def on_save_to_excel(self):
        pass

    def on_save(self):
        pass

    def on_text_box1_changed(self):
        pass

    def on_text_box2_changed(self):
        pass

    def on_text_box3_changed(self):
        pass

    def on_copy(self):
        pass

    def on_paste(self):
        pass

    def on_zoom(self):
        pass

    def on_about(self):
        text = "QupyRibbon\n"
        text += "This program was made by Magnus Jørgensen.\n"
        text += "Copyright © 2016 Magnus Jørgensen"
        QMessageBox().about(self, "About QupyRibbon", text)

    def on_license(self):
        file = open('LICENSE', 'r')
        lic = file.read()
        QMessageBox().information(self, "License", lic)

    def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
        action = QAction(get_icon(icon_name), caption, self)
        action.setStatusTip(status_tip)
        action.triggered.connect(connection)
        action.setIconVisibleInMenu(icon_visible)
        if shortcut is not None:
            action.setShortcuts(shortcut)
        self.addAction(action)
        return action

    def init_ribbon(self):
        #------文件选项----------------------------------
        home_tab = self._ribbon.add_ribbon_tab("文件")#table 选项
        file_pane = home_tab.add_ribbon_pane("文件")#选项下的菜单
        file_pane.add_ribbon_widget(RibbonButton(self, self._open_action, True))
        file_pane.add_ribbon_widget(RibbonButton(self, self._exit_action, True))

        down_load_panel = home_tab.add_ribbon_pane("更新")#选项下的菜单
        down_load_panel.add_ribbon_widget(RibbonButton(self, self.action_download, True))

        Purchase_order = home_tab.add_ribbon_pane("下单")  # 选项下的菜单
        Purchase_order.add_ribbon_widget(RibbonButton(self, self.action_purchase, True))

        about_software = home_tab.add_ribbon_pane("关于软件")  # 选项下的菜单
        about_software.add_ribbon_widget(RibbonButton(self, self.action_about_software, True))

        #grid = edit_panel.add_grid_widget(200)#选项下的菜单
        #grid.addWidget(QLabel("Text box 1"), 1, 1)
        #grid.addWidget(QLabel("Text box 2"), 2, 1)
        #grid.addWidget(QLabel("Text box 3"), 3, 1)
        #grid.addWidget(self._text_box1, 1, 2)
        #grid.addWidget(self._text_box2, 2, 2)
        #grid.addWidget(self._text_box3, 3, 2)

        # ------View选项----------------------------------
        #view_panel = home_tab.add_ribbon_pane("View")#选项下的菜单
        #view_panel.add_ribbon_widget(RibbonButton(self, self._zoom_action, True))
        #home_tab.add_spacer()

        # ------视图----------------------------------
        tool_tab = self._ribbon.add_ribbon_tab("视图")
        view_panel = tool_tab.add_ribbon_pane("视图")
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Left, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Right, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Front, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Rear, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Top, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Bottom, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.actionView_Iso, True))
        view_panel.add_ribbon_widget(RibbonButton(self, self.action_Fitall, True))

        # ------导出数据----------------------------------
        fix_tab = self._ribbon.add_ribbon_tab("导出数据")
        fix_panel = fix_tab.add_ribbon_pane("导出数据")
        fix_panel.add_ribbon_widget(RibbonButton(self, self.action_Export_STP, True))
        fix_panel.add_ribbon_widget(RibbonButton(self, self.action_Export_IGES, True))
        fix_panel.add_ribbon_widget(RibbonButton(self, self.action_Export_STL, True))


        # ------工具----------------------------------
        about_tab = self._ribbon.add_ribbon_tab("工具")
        tool_panel = about_tab.add_ribbon_pane("工具")
        tool_panel.add_ribbon_widget(RibbonButton(self, self.action_Measure_distance_tool, True))
        tool_panel.add_ribbon_widget(RibbonButton(self, self.action_Measure_diameter_tool, True))

class Vision(QtWidgets.QMainWindow, Vision.Ui_Form):
    def __init__(self, parent=None):
        super(Vision, self).__init__(parent)
        self.setupUi(self)
        self.label_6.setText("<A href='https://www.aliyuncad.com/'>软件下载：https://www.aliyuncad.com/</a>")
        self.label_6.setOpenExternalLinks(True)