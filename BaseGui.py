# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging
import time
from functools import partial
from OCC.Display.OCCViewer import OffscreenRenderer
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5 import QtCore, QtWidgets
from module import  Process_message_word,SelectModule,FuctionModule
from module.CreateParameter import *
from PyQt5.QtCore import pyqtSignal
from ui import MainGui

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
from PyQt5.QtGui import QIcon
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from PyQt5.QtWidgets import QApplication
import sys
from  module import Upyun_Update, AboutDownload,ShowGui,ProcessBar


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
        self.process_message = SelectModule.Process_message()
        self.process_message_word = Process_message_word()

        self.new_AboutDownload = AboutDownload()
        self.centerOnScreen()
        # ----------------------------------------------------------------------------------
        self.sinal = 0
        self.tabWidget_5.currentChanged['int'].connect(self.Refresh)  # 切换时刷新

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
        self.Measure_distance.triggered.connect(partial(FuctionModule.Measure_distance_fun,self))
        self.Measure_diameter.triggered.connect(partial(FuctionModule.Measure_diameter_fun,self))
        # --------------------------------------------------------------------------------------显示软件版本
        self.AboutVision.triggered.connect(self.Vision)
        self.AboutDownload.triggered.connect(self.AboutDownload_)



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
        '''
        SelectModule.Ceate_combox_table(self=self,ButtonId=ButtonId)
    def show_parameter(self, filepath=None):  # 切换到参数画面
        self.stackedWidget.setCurrentIndex(0)
        self.tab_7.show()
        QApplication.processEvents()
        self.canva._display.Repaint()

    def Create_ProcessBar(self, ButtonId=None):  # 过程处理函数 获取数据生成所需的界面
        SelectModule.Create_ProcessBar(self=self,ButtonId=ButtonId)

    def Show3D(self, mode=0, file=None, aCompound=None):  # 生成3D mode控制显示模式
        SelectModule.Show3D(self=self,mode=0, file=None, aCompound=None)

    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)


    def line_clicked(self, shp, *kwargs):
        """ This function is called whenever
        """

        FuctionModule.Measure_funtion(self=self,shp=shp)
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

                self.actionreboot.triggered.connect(partial(FuctionModule.Measure_distance_fun,self))
                self.actionreboot_1.triggered.connect(partial(FuctionModule.Measure_diameter_fun,self))

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




    def AboutDownload_(self):
        self.new_AboutDownload.show()





class AboutDownload(QtWidgets.QMainWindow, AboutDownload.Ui_Form):
    def __init__(self, parent=None):
        super(AboutDownload, self).__init__(parent)
        self.setupUi(self)





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
