#coding=utf-8
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Extend.TopologyUtils import TopologyExplorer
from PyQt5.QtWidgets import QApplication, QComboBox, QTableView
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QFont, QBrush, QPixmap, QMovie
from graphics import GraphicsView, GraphicsPixmapItem
from module.CreateParameter import *
import copy
from ui import Process_message
from module import source


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

def Create_product_parameter_table_and_show_3d(self, QClor=1, dict={}, start=0, ):  # 生成/更新产品参数表格
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
        if self.ButtonId in ["KS系列(孔输出) "]:
            self.combox_list[7].clear()  # 清楚原来的combobox选项
            series = self.combox_current_text_list[0]  # 机座号
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
                    Show3D(self=self,mode=0,file=filenam)
                    self.canva._display.Repaint()
                    self.filename=filenam
                    self.statusbar.showMessage("数据生成成功")

            except:
                self.statusbar.showMessage("此零件官方未提供3D，生成失败")


        except:
            pass

def Ceate_combox_table(self, ButtonId=None):  # 生成选项卡表格
        '''
        1.建立选型列表名称
        2.获取各个选项的值
        3.
        '''
        self.ButtonId = ButtonId
        try:
            pass
            # ----------2D显示图片操作 技术资料（1）----------------
            try:
                pix_name = ButtonId  # 2D
                # print(pix_name)
                self.pix = QPixmap('Pic\\' + pix_name + ".PNG")
                self.graphicsView = GraphicsView(self.pix, self.tab_8)
                self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461*self.width_scal, 581*self.height_scal))
                self.graphicsView.setObjectName("graphicsView")
                self.graphicsView.scale(0.4, 0.4)  # 显示比例
                self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
                self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
                self.scene.addItem(self.item)
            except:
                pass

            # ----------2D显示图片操作 技术资料（2）----------------
            try:
                pix_name = ButtonId  # 2D
                # print(pix_name)
                self.pix = QPixmap('Pic\\' + "KS枫信_3" + ".PNG")
                self.graphicsView = GraphicsView(self.pix, self.tab_3)
                self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461*self.width_scal, 581*self.height_scal))
                self.graphicsView.setObjectName("graphicsView")
                self.graphicsView.scale(0.4, 0.4)  # 显示比例
                self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
                self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
                self.scene.addItem(self.item)
            except:
                pass
                # ----------2D显示图片操作 技术资料（3）----------------
            try:
                pix_name = ButtonId  # 2D
                # print(pix_name)
                self.pix = QPixmap('Pic\\' + "KS枫信_4" + ".PNG")
                self.graphicsView = GraphicsView(self.pix, self.tab_4)
                self.graphicsView.setGeometry(QtCore.QRect(0, 0, 461*self.width_scal, 581*self.height_scal))
                self.graphicsView.setObjectName("graphicsView")
                self.graphicsView.scale(0.4, 0.4)  # 显示比例
                self.item = GraphicsPixmapItem(self.pix)  # 创建像素图元
                self.scene = QtWidgets.QGraphicsScene()  # 创建场景显示比例
                self.scene.addItem(self.item)
            except:
                pass
            # ------------------------------------------------------------
            if "KS系列(孔输出) " in ButtonId:
                self.boll_SCcrew = Create_Speed_reducer_ks_axle_output()#建立类

            all_combox_list = self.boll_SCcrew.Create_combox_list()
            self.order_code_position = len(all_combox_list) - 1  # 订购吗的位置
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
                file=os.path.join(os.getcwd(),file)
                print(file)
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

        except Exception as e:
            pass
            print(e)
            self.statusbar.showMessage("没有此零件")