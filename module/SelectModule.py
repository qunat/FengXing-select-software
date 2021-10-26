#coding=utf-8
from OCC.Core.TopoDS import TopoDS_Compound
from PyQt5.QtWidgets import QApplication, QComboBox
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QFont, QBrush, QPixmap
import copy


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
                    self.Show3D(mode=0,file=filenam)
                    self.canva._display.Repaint()
                    self.filename=filenam
                    self.statusbar.showMessage("数据生成成功")

            except:
                self.statusbar.showMessage("此零件官方未提供3D，生成失败")


        except:
            pass
