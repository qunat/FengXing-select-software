#coding=utf-8
from functools import partial
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Extend.TopologyUtils import TopologyExplorer
from PyQt5.QtWidgets import QApplication, QComboBox, QTableView
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QFont, QBrush, QPixmap, QMovie
from graphics import GraphicsView, GraphicsPixmapItem
from module.CreateParameter import *
from module.CreateParameter import Create_Speed_reducer_kbr_series_1to1
import copy,time,sys
from ui import Process_message
#from module import source
from multiprocessing import  Queue,Manager
from module import FuctionModule


def test(func):
    def inner():
        print('running')
    return inner

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
def Create_ProcessBar(self, ButtonId=None):  # 过程处理函数 获取数据生成所需的界面                步骤1
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
            if ButtonId in ["KS系列(孔输出)","KS系列(孔输出法兰)","KS系列(轴输出)","KS系列(轴输出法兰)"] :
                self.ButtonId = ButtonId
                self.Ceate_combox_table(ButtonId)#建立
                # 将所有的combox 选项和型号槽绑定 只要选项更新就会选项产品参数
                for i in self.combox_list:
                    if self.combox_list.index(i)==7:
                        i.currentTextChanged.connect(self.Ceate_show_3d)#刷新
                        continue
                    if self.combox_list.index(i)==1:
                        i.currentTextChanged.connect(self.show_technical_information)#根据combox内容刷新技术资料
                    i.currentTextChanged.connect(self.Ceate_product_parameter_table_and_show_3d)#刷新
            elif ButtonId in ["KBR系列(1-1)","KBR系列(1-2)","KB系列"] :
                self.ButtonId = ButtonId
                self.Ceate_combox_table(ButtonId)#建立
                # 将所有的combox 选项和型号槽绑定 只要选项更新就会选项产品参数
                for i in self.combox_list:
                    if self.combox_list.index(i)==7:
                        i.currentTextChanged.connect(self.Ceate_show_3d)#刷新
                        continue
                    if self.combox_list.index(i)==2:
                        i.currentTextChanged.connect(self.combox_refresh_function)#根据combox内容刷新combox刷新
                        continue
                    if self.combox_list.index(i)==1:
                        i.currentTextChanged.connect(self.show_technical_information)#根据combox内容刷新技术资料
                    i.currentTextChanged.connect(self.Ceate_product_parameter_table_and_show_3d)#刷新
            elif ButtonId in ["EDA系列"] :
                self.ButtonId = ButtonId
                self.Ceate_combox_table(ButtonId)#建立
                # 将所有的combox 选项和型号槽绑定 只要选项更新就会选项产品参数
                for i in self.combox_list:
                    if self.combox_list.index(i)==7:
                        i.currentTextChanged.connect(self.Ceate_show_3d)#刷新
                        continue
                    if self.combox_list.index(i)==2:
                        i.currentTextChanged.connect(self.combox_refresh_function)#根据combox内容刷新combox刷新
                        continue
                    if self.combox_list.index(i)==1:
                        i.currentTextChanged.connect(self.show_technical_information)#根据combox内容刷新技术资料
                    i.currentTextChanged.connect(self.Ceate_product_parameter_table_and_show_3d)#刷新
                    pass
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
def Ceate_combox_table(self, ButtonId=None):  # 生成选项卡表格   步骤二
        '''
        1.建立选型列表名称
        2.获取各个选项的值
        3.
        '''
        try:

            # ------------------------------------------------------------KS系列
            if ButtonId in ["KS系列(孔输出)"]:
                self.boll_SCcrew = Create_Speed_reducer_ks_hole_output()#建立类
            elif ButtonId in["KS系列(轴输出)"]:
                self.boll_SCcrew = Create_Speed_reducer_ks_axle_output()  # 建立类
            elif ButtonId in["KS系列(孔输出法兰)"]:
                self.boll_SCcrew = Create_Speed_reducer_ks_hole_flank_output()  # 建立类
            elif ButtonId in["KS系列(轴输出法兰)"]:
                self.boll_SCcrew = Create_Speed_reducer_ks_axle_flank_output()  # 建立类

            #---------------------------------------------------------------KBR系列
            if ButtonId in ["KBR系列(1-1)"]:
                self.boll_SCcrew = Create_Speed_reducer_kbr_series_1to1()#建立类
            elif ButtonId in["KBR系列(1-2)"]:
                self.boll_SCcrew = Create_Speed_reducer_kbr_series_1to2()#建立类

            #----------------------------------------------------------------KB系列
            if ButtonId in ["KB系列"]:
                self.boll_SCcrew = Create_Speed_reducer_kb_series()#建立类

            #----------------------------------------------------------------EDA系列
            if ButtonId in ["EDA系列"]:
                self.model_3d_file_list=self.ftp_serve.Get_file_list("EDA/EDA40/3D")
                self.boll_SCcrew = Create_transformer_EDA_series(self.model_3d_file_list)#建立类


            all_combox_list = self.boll_SCcrew.Create_combox_list()
            self.order_code_position = len(all_combox_list) - 1  # 订购码的位置
            self.tableWidget_2.setRowCount(len(all_combox_list))  # 参数表格设置.
            self.combox_list = []
            blank_size=self.tableWidget_2.geometry().width()/3
            self.tableWidget_2.setColumnWidth(1, blank_size)  # 手动设置列宽
            self.tableWidget_2.setColumnWidth(0, blank_size)  # 手动设置列宽
            self.tableWidget_2.setColumnWidth(2, blank_size)  # 手动设置列宽
            # ------------------------------------------------先生成combox选项卡
            for i in all_combox_list:  # 遍历生成所有的选项
                comBox = QComboBox()
                comBox.setFont(QFont("微软雅黑", 9, QFont.Black))
                comBox.setStyleSheet("QComboBox{color:rgb(0,0,0)}")
                self.combox_list.append(comBox)
                # comBox.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                if type(i).__name__ == "dict":  # 如果室字典类型则生成combox
                    for key, value in i.items():
                        newItem = QtWidgets.QTableWidgetItem(str(key))
                        newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
                        newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                        newItem.setFont(QFont("微软雅黑", 9, QFont.Black))  # 设置字体
                        newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
                        self.tableWidget_2.setItem(all_combox_list.index(i), 0, newItem)  # 代码
                        for k in value:
                            self.combox_list[all_combox_list.index(i)].addItem(k)
                    self.tableWidget_2.setCellWidget(all_combox_list.index(i), 1,
                                                     self.combox_list[all_combox_list.index(i)])
                    comBox.destroy()
                else:  # f否则生成普通单元格
                    pass
                    newItem = QtWidgets.QTableWidgetItem(str(i[0]))
                    newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
                    newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                    newItem.setFont(QFont("微软雅黑", 9, QFont.Black))
                    newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
                    self.tableWidget_2.setItem(all_combox_list.index(i), 0, newItem)  # 代码
                    # ------------------------------------------------------------------------
                    newItem = QtWidgets.QTableWidgetItem(str(i[1]))
                    newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
                    newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                    newItem.setFont(QFont("微软雅黑", 9, QFont.Black))
                    newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
                    self.tableWidget_2.setItem(all_combox_list.index(i), 1, newItem)  # 代码
                # 设置备注单元格的颜色
                newItem = QtWidgets.QTableWidgetItem(str(""))
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
                newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                # newItem.setFont(QFont("song", 9,QFont.Black))
                self.tableWidget_2.setItem(all_combox_list.index(i), 2, newItem)  # 代码

            # ----------------------------------------------------生成产品参数的tablewidget

        except:
            pass

def Create_product_parameter_table_and_show_3d(self, QClor=1, dict={}, start=0):  # 生成/更新产品参数表格    #步骤3
    '''
    根据combox选项生成产品参数列表
    '''
    try:
        QApplication.processEvents()
        self.aCompound = TopoDS_Compound()

    except:
        pass
    start = len(self.combox_list)  # 确定起始位置
    self.combox_current_text_list = []
    for i in self.combox_list:
        if i.currentText() == "":
            continue
        self.combox_current_text_list.append(i.currentText())  # 装有combox的列表
    try:
        if self.ButtonId in ["KS系列(孔输出)","KS系列(孔输出法兰)","KS系列(轴输出)","KS系列(轴输出法兰)"]:
            self.combox_list[7].clear()  # 清楚原来的combobox选项
            series ="KS"+self.combox_current_text_list[0]  # 机座号
            additems = self.boll_SCcrew.path_dict["FX" + str(series)]  # 对应机座号的可选模型的
            self.filename_dict = {}
            additem_list = []
            for i in range(len(additems)):
                additem = additems[i].split("\\")[-1].replace(".step", "")
                self.filename_dict[additem] = copy.deepcopy(additems[i])
                additem_list.append(additem)
            self.combox_list[7].addItems(additem_list)  # 根据选项变换combox里的内容
            series_1 = self.combox_current_text_list[1]  # 减速比
            dict = self.boll_SCcrew.series[str(series)]  # 机座号选型列表
            dict["额定承载扭矩T2N(Nm)"] = self.boll_SCcrew.T2N[str(series_1)][series]
            dict["最大承载扭矩T2B(Nm)"] = str(float(self.boll_SCcrew.T2N[str(series_1)][series]) * 1.5)
            dict["背隙"] = self.boll_SCcrew.arcmin[str(series_1)]
            dict["输出轴许可径向力"] = self.boll_SCcrew.output_radial_force[str(series_1)][series]
            dict["制锁"] = self.boll_SCcrew.self_lock[str(series_1)]

        elif self.ButtonId in ["KBR系列(1-1)","KBR系列(1-2)"]:
            self.combox_list[7].clear()  # 清楚原来的combobox选项
            series = "KBR"+self.combox_current_text_list[0]  # 机座号
            additems = self.boll_SCcrew.path_dict["FX"+str(series)]  # 对应机座号的可选模型的
            self.filename_dict = {}
            additem_list = []
            for i in range(len(additems)):
                additem = additems[i].split("\\")[-1].replace(".step", "")
                self.filename_dict[additem] = copy.deepcopy(additems[i])
                additem_list.append(additem)
            self.combox_list[7].addItems(additem_list)  # 根据选项变换combox里的内容

            series_1 = self.combox_current_text_list[1]  # 段数
            series_2=self.combox_current_text_list[2] #减速比
            #series_3 = self.boll_SCcrew.series[str(series)]  # 机座号选型列表
            dict["额定输出扭矩T2N(Nm)"] = self.boll_SCcrew.T2N[series_1][series_2][series]
            dict["最大输出扭矩(Nm)"] = str(float(self.boll_SCcrew.T2N[series_1][series_2][series])*2)
            dict["额定输入转速(rpm)"] = self.boll_SCcrew.n1N[str(series)]
            dict["最大输入转速(rpm)"] = self.boll_SCcrew.n1B[str(series)]
            dict["背隙"] = self.boll_SCcrew.arcmin[self.combox_current_text_list[4]][series_1][series_2]
            dict["容许径向力(N)"] = self.boll_SCcrew.F1[str(series)]
            dict["容许轴向力(N)"] = self.boll_SCcrew.F2[str(series)]
            dict["效率(%)"] = self.boll_SCcrew.power[str(series_1)][series_2]
            dict["噪音(DB)"] = self.boll_SCcrew.dB[str(series)]
            dict["重量(Kg)"] = self.boll_SCcrew.weight[series_1][series]
            dict["减速机转动惯量(kg.cm2)"] = self.boll_SCcrew.Moment_inertia[series_1][series_2][series]


        elif self.ButtonId in ["KB系列"]:
            self.combox_list[7].clear()  # 清楚原来的combobox选项
            series = "KB"+self.combox_current_text_list[0]  # 机座号
            additems = self.boll_SCcrew.path_dict["FX"+str(series)]  # 对应机座号的可选模型的
            self.filename_dict = {}
            additem_list = []
            for i in range(len(additems)):
                additem = additems[i].split("\\")[-1].replace(".step", "")
                self.filename_dict[additem] = copy.deepcopy(additems[i])
                additem_list.append(additem)
            self.combox_list[7].addItems(additem_list)  # 根据选项变换combox里的内容

            series_1 = self.combox_current_text_list[1]  # 段数
            series_2=self.combox_current_text_list[2] #减速比

            #series_3 = self.boll_SCcrew.series[str(series)]  # 机座号选型列表
            dict["额定输出扭矩T2N(Nm)"] = self.boll_SCcrew.T2N[series_1][series_2][series]
            dict["最大输出扭矩(Nm)"] = str(float(self.boll_SCcrew.T2N[series_1][series_2][series])*2)
            dict["额定输入转速(rpm)"] = self.boll_SCcrew.n1N[str(series)]
            dict["最大输入转速(rpm)"] = self.boll_SCcrew.n1B[str(series)]
            dict["背隙"] = self.boll_SCcrew.arcmin[self.combox_current_text_list[4]][series_1][series]
            dict["容许径向力(N)"] = self.boll_SCcrew.F1[str(series)]
            dict["容许轴向力(N)"] = self.boll_SCcrew.F2[str(series)]
            dict["效率(%)"] = self.boll_SCcrew.power[str(series_1)][series]
            dict["噪音(DB)"] = self.boll_SCcrew.dB[str(series)]
            dict["重量(Kg)"] = self.boll_SCcrew.weight[series_1][series]
            dict["减速机转动惯量(kg.cm2)"] = self.boll_SCcrew.Moment_inertia[series_1][series_2][series]

        dict_list = []
        self.tableWidget_2.setRowCount(len(dict) + len(self.combox_list))  # 参数表格设置.

        for key in dict.keys():
            ls_list = []
            ls_list.append(key)
            ls_list.append(dict[key])
            dict_list.append(ls_list)
        RowCount = len(dict)
        for i in range(RowCount):
            # 第一列
            newItem = QtWidgets.QTableWidgetItem(dict_list[i][0])
            self.tableWidget_2.setItem(i + len(self.combox_list), 0, newItem)  # 代码
            newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)  # 文字居中
            newItem.setFont(QFont("微软雅黑", 9, QFont.Black))
            newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))

            # 第二列
            if type(dict_list[i][1]) == list:
                pass
                comBox = QComboBox()  # 选项列表
                for ls_item in dict_list[i][1]:
                    pass
                    comBox.addItem(ls_item)
                self.tableWidget_2.setCellWidget(i + len(self.combox_list), 1, comBox)

            else:
                newItem = QtWidgets.QTableWidgetItem(str(dict_list[i][1]))
                self.tableWidget_2.setItem(i + len(self.combox_list), 1, newItem)  # 代码
                newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)  # 文字居中
                newItem.setFont(QFont("微软雅黑", 9, QFont.Black))
                newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
            # 第三列
            newItem = QtWidgets.QTableWidgetItem("")
            self.tableWidget_2.setItem(i + len(self.combox_list), 2, newItem)  # 代码
            newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)  # 文字居中
            newItem.setFont(QFont("微软雅黑", 9, QFont.Black))
            newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))

    except Exception as e:
        print(e)
        pass
    # 获取combox现在设定的参数
    try:
        # ----------------------------------------------清除原有的模型--------------------------
        try:
            for i in self.show:
                self.canva._display.Context.Remove(i, True)
                self.canva._display.Context.erase()
            self.aCompound.Free()
        except:
            pass

        # -----------------设置订购码------------------------------------------------------
        if self.ButtonId in ["KS系列(孔输出)", "KS系列(孔输出法兰)", "KS系列(轴输出)", "KS系列(轴输出法兰)"]:  # 设置订购码
            try:
                series ="KS"+self.combox_list[1].currentText() + "-"  # 系列号和机座代号
                Deceleration_ratio = self.combox_list[3].currentText() + "-"  # 减速比
                Deceleration_ratio = self.combox_list[2].currentText() + "-"  # 减速比
                Rotating_shaft = self.combox_list[3].currentText()[0:2] + "-"  # 附件轴类型
                Out_Flanges = self.combox_list[4].currentText()[0] + "-"  # 输出安装法兰类型
                Fixt_mode = self.combox_list[5].currentText() + "/"  # 安装方式
                Motor_type = self.combox_list[6].currentText()[0:1]  # 电机类型
                series = series + Deceleration_ratio + Rotating_shaft + Out_Flanges + Fixt_mode + Motor_type
            except Exception as e:
                pass
                print(e)
            newItem = QtWidgets.QTableWidgetItem(series)
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
            newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
            newItem.setFont(QFont("微软雅黑", 8, QFont.Black))
            newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
            #self.tableWidget_2.setSpan(self.order_code_position, 1, 1, 2)#合并单元格
            self.copy_buttom = QtWidgets.QPushButton("复制订购码")
            self.copy_buttom.clicked.connect(partial(order_code_copy, series,self))
            self.tableWidget_2.setCellWidget(self.order_code_position, 2, self.copy_buttom)
            self.tableWidget_2.setItem(self.order_code_position, 1, newItem)  # 设置订购码

        if self.ButtonId in ["KBR系列(1-1)", "KBR系列(1-2)","KB系列"]:  # 设置订购码
            try:
                if self.ButtonId=="KB系列":
                    series = "KB" + self.combox_list[1].currentText() + "-"  # 系列号和机座代号
                else:
                    series = "KBR" + self.combox_list[1].currentText() + "-"  # 系列号和机座代号
                Deceleration_ratio = self.combox_list[3].currentText() + "-"  # 减速比
                Deceleration_ratio = self.combox_list[2].currentText() + "-"  # 段数
                Rotating_shaft = self.combox_list[3].currentText()[0:2] + "-"  # 减速比
                Out_Flanges = self.combox_list[4].currentText()[0:2] + "-"  # 轴型
                Fixt_mode = self.combox_list[5].currentText()[0:2] + "/"  # 背隙
                Motor_type = self.combox_list[6].currentText()[0:1]  # 电机类型
                series = series + Deceleration_ratio + Rotating_shaft + Out_Flanges + Fixt_mode + Motor_type
            except Exception as e:
                pass
                print(e)
            newItem = QtWidgets.QTableWidgetItem(series)
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
            newItem.setBackground(QtGui.QBrush(QtGui.QColor(240, 255, 191)))  # 设置背景颜色
            newItem.setFont(QFont("微软雅黑", 8, QFont.Black))
            newItem.setForeground(QBrush(QtGui.QColor(0, 0, 0)))
            #self.tableWidget_2.setSpan(self.order_code_position, 1, 1, 2)#合并单元格
            self.copy_buttom=QtWidgets.QPushButton("复制订购码")
            self.copy_buttom.clicked.connect(partial(order_code_copy, series,self))
            self.tableWidget_2.setCellWidget(self.order_code_position,2,self.copy_buttom)
            self.tableWidget_2.setItem(self.order_code_position, 1, newItem)  # 设置订购码

            # ----------显示3D-------------------------------------------------------------------
            self.tab_7.repaint()
            try:
                filenam = self.filename_dict[self.combox_list[2].currentText()]
                filenam = filenam.repalce(".step", "")
                self.aCompound = self.boll_SCcrew.Create_shape(filename=filenam)
                self.Show3D(mode=1, aCompound=self.aCompound)
                self.statusbar.showMessage("数据生成成功")
                pass
            except:
                self.statusbar.showMessage("此零件官方未提供3D，生成失败")

    except Exception as e:
        print(e)
        pass

def Ceate_show_3d(self, QClor=1, dict={}, start=0, ):#仅更新3D
        #根据combox选项生成产品参数列表
        if self.combox_list[7].currentText() != "-":
            self.statusbar.showMessage("数据生成中.....")
        try:
            # ----------------------------------------------清除原有的模型--------------------------
            try:
                for i in self.show:
                    self.canva._display.Context.Remove(i, True)
                    self.canva._display.Context.erase()
                self.aCompound.Free()
            except:
                pass
            # ----------显示3D-------------------------------------------------------------------
            self.tab_7.repaint()
            try:
                if self.combox_list[7].currentText()!="-":
                    filenam = self.filename_dict[self.combox_list[7].currentText()]

                    #filenam=filenam.replace(".step","")
                    #self.aCompound = self.boll_SCcrew.Create_shape(filename=filenam)
                    filenam=filenam.replace(".\\","")
                    self.output_filename =filenam
                    Show3D(self=self,mode=0,file=filenam)
                    self.canva._display.Repaint()
                    self.filename=filenam
                    self.statusbar.showMessage("数据生成成功")

            except:
                self.statusbar.showMessage("此零件官方未提供3D，生成失败")


        except:
            pass




def Show3D(self, mode=0, file=None, aCompound=None):  # 生成3D mode控制显示模式
        try:
            self.canva._display.EraseAll()
            self.canva._display.hide_triedron()
            self.canva._display.display_triedron()
            self.canva._display.Repaint()
            self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
            self.New_Compound = TopoDS_Compound()  # 定义一个复合体
            self.new_build.MakeCompound(self.New_Compound)  # 生成一个复合体DopoDS_shape
            if mode == 0:
                file=os.path.join(os.getcwd(),file)
                shapes_labels_colors = read_step_file_with_names_colors(file)
                self.statusbar.showMessage("数据生成中请梢后......")
                self.aCompound=shapes_labels_colors
                for shpt_lbl_color in shapes_labels_colors:
                    label, c = shapes_labels_colors[shpt_lbl_color]
                    for e in TopologyExplorer(shpt_lbl_color).solids():
                        self.new_build.Add(self.New_Compound, e)
                        self.canva._display.DisplayColoredShape(e, color=Quantity_Color(c.Red(),
                                                                                        c.Green(),
                                                                                        c.Blue(),
                                                                                   Quantity_TOC_RGB))
                    self.aCompound=self.New_Compound
            elif mode == 1:

                self.show = self.canva._display.DisplayColoredShape(aCompound, color="WHITE", update=True)
            self.canva._display.FitAll()


        except Exception as e:
            pass
            print(e)
            self.statusbar.showMessage("没有此零件")
            
def combox_refresh_function(self):#根据comcox改变combox
    if self.ButtonId in ["KBR系列(1-1)", "KBR系列(1-2)","KB系列"]:
        Reduction_ratio = self.boll_SCcrew.lever[self.combox_list[2].currentText()]
        self.combox_list[3].clear()
        self.combox_list[3].addItems(Reduction_ratio)  # 根据选项变换combox里的内容




def show_technical_information(self):
    ButtonId=self.ButtonId
    if ButtonId in ["KS系列(孔输出)", "KS系列(孔输出法兰)", "KS系列(轴输出)", "KS系列(轴输出法兰)"]:
        pix_name_1 = "KS_1"
        pix_name_2 = "KS_2"
    elif ButtonId in ["KBR系列(1-1)","KBR系列(1-2)"]:
        series = "KBR" + self.combox_list[1].currentText()  # 机座号
        if series in ["KBR60","KBR90"]:
            pix_name_1 = "KBR-1"
            pix_name_2 = "KBR-1"
        elif series in ["KBR115","KBR142"]:
            pix_name_1 = "KBR-2"
            pix_name_2 = "KBR-2"
        elif series in ["KBR180","KBR220"]:
            pix_name_1 = "KBR-3"
            pix_name_2 = "KBR-3"
        elif series in ["KBR280","KBR340"]:
            pix_name_1 = "KBR-4"
            pix_name_2 = "KBR-4"
    elif ButtonId in ["KB系列"]:
        series = "KB" + self.combox_list[1].currentText()  # 机座号
        if series in ["KB60","KB90"]:
            pix_name_1 = "KB-1"
            pix_name_2 = "KB-1"
        elif series in ["KB115","KB142"]:
            pix_name_1 = "KB-2"
            pix_name_2 = "KB-2"
        elif series in ["KB180","KB220"]:
            pix_name_1 = "KB-3"
            pix_name_2 = "KB-3"
        elif series in ["KB280","KB340"]:
            pix_name_1 = "KB-4"
            pix_name_2 = "KB-4"
    # ----------2D显示图片操作 技术资料（1）----------------
    try:
        pix_name = ButtonId  # 2D
        #self.pix = QPixmap('Pic\\' + pix_name + ".PNG")
        self.graphicsView = GraphicsView(self.pix_dict[ButtonId], self.tab_8)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461 * self.width_scal, 581 * self.height_scal))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.scale(0.4, 0.4)  # 显示比例
        self.graphicsView.repaint()
        self.graphicsView.update()
        self.graphicsView.show()
        self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
        self.scene.addItem(self.item)

    except Exception as e:
        print(e)
        pass

    # ----------2D显示图片操作 技术资料（2）----------------
    try:
        self.graphicsView = GraphicsView(self.pix_dict[pix_name_1], self.tab_3)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461 * self.width_scal, 581 * self.height_scal))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.scale(0.4, 0.4)  # 显示比例
        self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
        self.scene.addItem(self.item)
        self.graphicsView.repaint()
        self.graphicsView.update()
        self.graphicsView.show()
    except:
        pass
        # ----------2D显示图片操作 技术资料（3）----------------
    try:
        self.graphicsView = GraphicsView(self.pix_dict[pix_name_2], self.tab_4)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461 * self.width_scal, 581 * self.height_scal))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.scale(0.4, 0.4)  # 显示比例
        self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
        self.scene.addItem(self.item)
        self.graphicsView.repaint()
        self.graphicsView.update()
        self.graphicsView.show()
    except:
        pass



def Create_pix_naime_dict_fun(pix_name,return_queue):
    app = QtWidgets.QApplication(sys.argv)
    #widget = QtWidgets.QWidget()
    pix_dict = {}
    for i in pix_name:
        try:
            pix_dict[i] = QPixmap("./"+'Pic/' + i + ".png")
        except Exception as e:
            print(e)
    #return_queue.put(pix_dict)
    print(return_queue)



def Create_pix_name_dict(self,path=".\\Pic"):#--------------------------------------------------- 资料图片加载

    try:
        self.pix_dict = {}
        index=0
        all_number=0
        compplete_percent=0
        pix_list=[]
        start_time = time.time()
        for root, dirs, files in os.walk(".\\Pic", topdown=False):
            if root == ".\\Pic":
                all_number=len(files)
                for i in files:
                    if i.lower().endswith("jpg"):
                        continue
                    pix_name = i.replace(".png", "")
                    pix_list.append(pix_name)
                    self.pix_dict[pix_name] = QPixmap("./"+'Pic/' + pix_name + ".png")
                    index+=1
                    compplete_percent=str(int(index/all_number*100))+"%"
                    self.splash.showMessage("资源加载中:"+compplete_percent+"  "+i)
                break

        '''
        尝试多进程失败
        queue=Queue()
        return_queue=Queue()
        queue.put(pix_list)
        manager=Manager()
        pix_dict=manager.list()
        new_speed=FuctionModule.speed_processing()
        new_speed.Create_multi_process(Create_pix_naime_dict_fun,queue,return_queue)
        '''
        end_time = time.time()
        print(end_time - start_time)
        self.splash.showMessage("资源加载中:" + "100%"+" 完成")
    except Exception as e:
        print(e)
        pass

def canvan_click(self):
        pass

def order_code_copy(series,self):
    clipboard = QApplication.clipboard()
    clipboard.setText(series)
    self.statusbar.showMessage("复制成功")

