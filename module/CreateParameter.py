# -*- coding: utf-8 -*-
import os

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeChamfer
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Builder, TopoDS_Compound, topods_CompSolid
from OCC.Extend.DataExchange import read_step_file, write_step_file
from OCC.Core.ChFi2d import ChFi2d_ChamferAPI
from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir




class Create_Speed_reducer_ks_axle_output(object):
    def __init__(self):
        pass
        D_r_dict={}#Deceleration_ratio_dict
        self.path_list=[]
        self.path_dict={}
        self.T2N={"7.5":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "10":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "15":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "20":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "25":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "30":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "40":{"KS40":35,"KS50":65,"KS63":120,"KS75":230,"KS90":350,"KS110":600,"KS130":1000,"KS150":1600},
                  "50":{"KS40":35,"KS50":55,"KS63":120,"KS75":200,"KS90":310,"KS110":560,"KS130":900,"KS150":1500},
                  "60":{"KS40":35,"KS50":55,"KS63":120,"KS75":200,"KS90":310,"KS110":560,"KS130":900,"KS150":1500},
                  "80":{"KS40":30,"KS50":50,"KS63":110,"KS75":180,"KS90":260,"KS110":450,"KS130":800,"KS150":1300},
                  "100":{"KS40":25,"KS50":40,"KS63":100,"KS75":160,"KS90":220,"KS110":400,"KS130":700,"KS150":1200}}
        self.output_radial_force=\
                {"7.5":{"KS40":1325,"KS50":1829,"KS63":2378,"KS75":2799,"KS90":3089,"KS110":3908,"KS130":5112,"KS150":7668},
                  "10":{"KS40":1454,"KS50":2007,"KS63":2609,"KS75":3072,"KS90":3400,"KS110":4288,"KS130":5610,"KS150":8415},
                  "15":{"KS40":1665,"KS50":2298,"KS63":2988,"KS75":3518,"KS90":3893,"KS110":4810,"KS130":6424,"KS150":9636},
                  "20":{"KS40":1829,"KS50":2525,"KS63":3283,"KS75":3865,"KS90":4277,"KS110":5395,"KS130":7075,"KS150":10612},
                  "25":{"KS40":1981,"KS50":2735,"KS63":3556,"KS75":4187,"KS90":3633,"KS110":5844,"KS130":7645,"KS150":11467},
                  "30":{"KS40":2037,"KS50":2661,"KS63":3745,"KS75":4410,"KS90":4880,"KS110":6155,"KS130":8052,"KS150":12078},
                  "40":{"KS40":2309,"KS50":3188,"KS63":4145,"KS75":4880,"KS90":5401,"KS110":6812,"KS130":8912,"KS150":13368},
                  "50":{"KS40":2485,"KS50":3431,"KS63":4461,"KS75":5252,"KS90":5812,"KS110":7331,"KS130":95090,"KS150":14385},
                  "60":{"KS40":2649,"KS50":3658,"KS63":4756,"KS75":5599,"KS90":6169,"KS110":7815,"KS130":10224,"KS150":15336},
                  "80":{"KS40":2907,"KS50":4014,"KS63":5218,"KS75":6144,"KS90":6799,"KS110":8578,"KS130":11219,"KS150":16828},
                  "100":{"KS40":3142,"KS50":4338,"KS63":5639,"KS75":6639,"KS90":7348,"KS110":8268,"KS130":12124,"KS150":18186}}

        self.arcmin = {"7.5": "≤8弧分", "10": "≤8弧分", "15": "≤10弧分", "20": "≤10弧分", "25": "≤10弧分", "30": "≤10弧分",
                       "40": "≤12弧分", "50": "≤12弧分", "60": "≤12弧分", "80": "≤12弧分", "100": "≤12弧分"}
        self.self_lock={"7.5":"否","10":"否","15":"否","20":"否","25":"否","30":"是","40":"是","50":"是","60":"是","80":"是",
                        "100":"是"}

        self.KS40_dict = {"性能参数表":"","额定承载扭矩T2N(Nm)":35,"箱体材料":"铝材","最大承载扭矩T2B(Nm)":0 ,
                          "额定输转速n1N(rpm)":"2000","最大输转速n1N(rpm)":"2500","背隙":0,"输出轴许可径向力":1325,
                          "输入轴许可径向力":350,"传动效率(%)":"72%","噪音(DB)":"≤68","重量(Kg)":2.5,"使用温度":"-5℃-60℃",
                          "制锁":"是","使用寿命(h)":10000,"使用维护(h)":"2500小时更换涡轮机油",
                          "尺寸参数表":"","A1":100,"A2":71.5,"A3":50,"A4":70,"A5":6.5,"A6":"M6","A7":75,"A8":15,
                          "B1":78,"B2":55,"B3":35,"B4":60,"B5":60,"B6":40,"B7":6.5,
                           "F1":26,"F2":18,"F3":20.8,"F4":6,"C1":60,"C2":"M4M5","C3":70,"C4":40,"C5":14,"C6":50,"C7":6,
                          "C8":5,"C9":16.3}  #

        self.KS50_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 490, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 3.5, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 120, "A2": 84, "A3": 60, "A4": 80, "A5": 7, "A6": "M8", "A7": 85,
                          "A8": 25,
                          "B1": 92, "B2": 64, "B3": 40, "B4": 70, "B5": 70, "B6": 50, "B7": 8.5,
                          "F1": 30, "F2": 25, "F3": 28.3, "F4": 8, "C1": 80, "C2": "M5M6", "C3": "70 90", "C4": 45, "C5": "14 19",
                          "C6": "50 70", "C7": 6,
                          "C8": "5 6", "C9": "16.3 21.8"}  #

        self.KS63_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "", "最大输转速n1N(rpm)": "", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 700, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 6.5, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 144, "A2": 102, "A3": 72, "A4": 100, "A5": 8, "A6": "M8", "A7": 95,
                          "A8": 25,
                          "B1": 112, "B2": 80, "B3": 50, "B4": 85, "B5": 80, "B6": 63, "B7": 8.5,
                          "F1": 36, "F2": 25, "F3": 28.3, "F4": 8, "C1": 90, "C2": "M6M8", "C3": "70 90", "C4": 45,
                          "C5": "14 19",
                          "C6": "50 70", "C7": "6 8",
                          "C8": "5 6", "C9": "16.3 21.8"}  #
        self.KS75_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 980, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 10, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 172, "A2": 119, "A3": 86, "A4": 120, "A5": 10, "A6": "M8", "A7": 115,
                          "A8": 25,
                          "B1": 120, "B2": 93, "B3": 60, "B4": 90, "B5": 95, "B6": 75, "B7": 11,
                          "F1": 40, "F2": 28, "F3": 31.3, "F4": 8, "C1": "110 130", "C2": "M8", "C3": "90 115", "C4": 65,
                          "C5": "19 22 24",
                          "C6": "70 110", "C7": "6",
                          "C8": "6 8", "C9": "21.8 24.8"}  #

        self.KS90_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 1270, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 16, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 206, "A2": 135, "A3": 103, "A4": 140, "A5": 11, "A6": "M10", "A7": 130,
                          "A8": 30,
                          "B1": 140, "B2": 102, "B3": 70, "B4": 100, "B5": 110, "B6": 90, "B7": 13,
                          "F1": 45, "F2": 35, "F3": 38.3, "F4": 10, "C1": "130", "C2": "M8", "C3": "145 165",
                          "C4": 65,
                          "C5": "22 24 32",
                          "C6": "110 130", "C7": "6",
                          "C8": "8 10", "C9": "24.8 35.3"}  #

        self.KS110_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材/铸铁", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "200", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 1700, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": "25/40", "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 252.5, "A2": 167.5, "A3": 127.5, "A4": 170, "A5": 14, "A6": "M10", "A7": 165,
                          "A8": 30,
                          "B1": 155, "B2": 125, "B3": 85, "B4": 115, "B5": 130, "B6": 110, "B7": 14,
                          "F1": 50, "F2": 42, "F3": 45.3, "F4": 12, "C1": "150 180", "C2": "M12", "C3": "165 200",
                          "C4": 82,
                          "C5": "32 25 38",
                          "C6": "130 114.3", "C7": "6",
                          "C8": "10 12", "C9": "35.3 38.3"}  #

        self.KS130_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铸铁", "最大承载扭矩T2B(Nm)": 0,
                           "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "2000", "背隙": 0, "输出轴许可径向力": 1325,
                           "输入轴许可径向力": 2100, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 60, "使用温度": "-5℃-60℃",
                           "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                           "尺寸参数表": "", "A1": 292.5, "A2": 187.5, "A3": 147.5, "A4": 200, "A5": 15, "A6": "M12",
                           "A7": 215,
                           "A8": 30,
                           "B1": 170, "B2": 140, "B3": 100, "B4": 120, "B5": 180, "B6": 130, "B7": 16,
                           "F1": 60, "F2": 45, "F3": 48.3, "F4": 14, "C1": "180 190", "C2": "M12", "C3": "200 215",
                           "C4": 116,
                           "C5": "35 28 42",
                           "C6": "114.3 180", "C7": "6",
                           "C8": "10 12", "C9": "38.3 45.3"}  #

        self.KS150_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铸铁", "最大承载扭矩T2B(Nm)": 0,
                           "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "2000", "背隙": 0, "输出轴许可径向力": 1325,
                           "输入轴许可径向力": 2600, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 80, "使用温度": "-5℃-60℃",
                           "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                           "尺寸参数表": "", "A1": 340, "A2": 230, "A3": 170, "A4": 240, "A5": 18, "A6": "M12",
                           "A7": 215,
                           "A8": 30,
                           "B1": 200, "B2": 180, "B3": 120, "B4": 145, "B5": 180, "B6": 150, "B7": 18,
                           "F1": 72.5, "F2": 50, "F3": 53.8, "F4": 14, "C1": "180 190", "C2": "M12", "C3": "200 215",
                           "C4": 116,
                           "C5": "35 28 42",
                           "C6": "114.3 180", "C7": "6",
                           "C8": "10 12", "C9": "38.3 45.3"}  #


        self.KS_series_dict = {"KS40":self.KS40_dict,"KS50":self.KS40_dict,"KS63":self.KS63_dict,"KS75":self.KS75_dict,"KS90":self.KS90_dict,
                                "KS110":self.KS110_dict,"KS130":self.KS110_dict,"KS150":self.KS150_dict
                                }
        self.series = self.KS_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath=filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath =filename+".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        self.Get_resourcr_list()
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        all_combox_list.append(["机型代号", "KS"])
        dict_combox = {"机座号": combox_list}  #
        all_combox_list.append(dict_combox)  # 机型代号
        all_combox_list.append({"减速比": ["  ", "7.5", "10", "15","20","25","30","40","50","60","80","100"]})
        all_combox_list.append({"轴型": ["  ", "S1:附键实心轴", "S2:附键空心轴", "S3:双输出实心轴"]})
        all_combox_list.append({"有无法兰": ["  ", "F:法兰","N:无法兰"]})
        all_combox_list.append({"安装方式": ["","M1","M2","M3","M4","M5","M6"]})
        all_combox_list.append({"电机型号": ["  ", "P:无电机", "T:台达伺服电机", "Y:安川伺服电机", "M:三菱伺服电机""p:松下伺服电机","S:西门子伺服电机"]})
        all_combox_list.append({"可选模型": ["-"]})
        all_combox_list.append(["订购码", "-"])

        return all_combox_list

    def Get_resourcr_list(self):
        path_list=[]
        for root, dirs, files in os.walk(".\\resource", topdown=False):
            for i in files:
                path=os.path.join(root,i)
                path_list.append(path)
            path_list.insert(0,"-")
            self.path_list.append(path_list)
            path_list=[]
        for j in self.path_list:
            for i in j:
                ls_kind = i.split("\\")[-1]
                ls_kind =ls_kind.split("-")[0]
            self.path_dict[ls_kind]=j

class Create_Speed_reducer_ks_hole_flank_output(Create_Speed_reducer_ks_axle_output):
    def __init__(self):
        self.KS40_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 350, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 2.5, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 100, "A2": 71.5, "A3": 50, "A4": 70, "A5": 6.5, "A6": "M6", "A7": 75,
                          "A8": 15,
                          "B1": 78, "B2": 55, "B3": 35, "B4": 60, "B5": 60, "B6": 40, "B7": 6.5,
                          "F1": 26, "F2": 18, "F3": 20.8, "F4": 6, "C1": 60, "C2": "M4M5", "C3": 70, "C4": 40, "C5": 14,
                          "C6": 50, "C7": 6,
                          "C8": 5, "C9": 16.3}  #

        self.KS50_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 490, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 3.5, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 120, "A2": 84, "A3": 60, "A4": 80, "A5": 7, "A6": "M8", "A7": 85,
                          "A8": 25,
                          "B1": 92, "B2": 64, "B3": 40, "B4": 70, "B5": 70, "B6": 50, "B7": 8.5,
                          "F1": 30, "F2": 25, "F3": 28.3, "F4": 8, "C1": 80, "C2": "M5M6", "C3": "70 90", "C4": 45,
                          "C5": "14 19",
                          "C6": "50 70", "C7": 6,
                          "C8": "5 6", "C9": "16.3 21.8"}  #

        self.KS63_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "", "最大输转速n1N(rpm)": "", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 700, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 6.5, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 144, "A2": 102, "A3": 72, "A4": 100, "A5": 8, "A6": "M8", "A7": 95,
                          "A8": 25,
                          "B1": 112, "B2": 80, "B3": 50, "B4": 85, "B5": 80, "B6": 63, "B7": 8.5,
                          "F1": 36, "F2": 25, "F3": 28.3, "F4": 8, "C1": 90, "C2": "M6M8", "C3": "70 90", "C4": 45,
                          "C5": "14 19",
                          "C6": "50 70", "C7": "6 8",
                          "C8": "5 6", "C9": "16.3 21.8"}  #
        self.KS75_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 980, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 10, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 172, "A2": 119, "A3": 86, "A4": 120, "A5": 10, "A6": "M8", "A7": 115,
                          "A8": 25,
                          "B1": 120, "B2": 93, "B3": 60, "B4": 90, "B5": 95, "B6": 75, "B7": 11,
                          "F1": 40, "F2": 28, "F3": 31.3, "F4": 8, "C1": "110 130", "C2": "M8", "C3": "90 115",
                          "C4": 65,
                          "C5": "19 22 24",
                          "C6": "70 110", "C7": "6",
                          "C8": "6 8", "C9": "21.8 24.8"}  #

        self.KS90_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材", "最大承载扭矩T2B(Nm)": 0,
                          "额定输转速n1N(rpm)": "2000", "最大输转速n1N(rpm)": "2500", "背隙": 0, "输出轴许可径向力": 1325,
                          "输入轴许可径向力": 1270, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 16, "使用温度": "-5℃-60℃",
                          "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                          "尺寸参数表": "", "A1": 206, "A2": 135, "A3": 103, "A4": 140, "A5": 11, "A6": "M10", "A7": 130,
                          "A8": 30,
                          "B1": 140, "B2": 102, "B3": 70, "B4": 100, "B5": 110, "B6": 90, "B7": 13,
                          "F1": 45, "F2": 35, "F3": 38.3, "F4": 10, "C1": "130", "C2": "M8", "C3": "145 165",
                          "C4": 65,
                          "C5": "22 24 32",
                          "C6": "110 130", "C7": "6",
                          "C8": "8 10", "C9": "24.8 35.3"}  #

        self.KS110_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铝材/铸铁", "最大承载扭矩T2B(Nm)": 0,
                           "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "200", "背隙": 0, "输出轴许可径向力": 1325,
                           "输入轴许可径向力": 1700, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": "25/40", "使用温度": "-5℃-60℃",
                           "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                           "尺寸参数表": "", "A1": 252.5, "A2": 167.5, "A3": 127.5, "A4": 170, "A5": 14, "A6": "M10",
                           "A7": 165,
                           "A8": 30,
                           "B1": 155, "B2": 125, "B3": 85, "B4": 115, "B5": 130, "B6": 110, "B7": 14,
                           "F1": 50, "F2": 42, "F3": 45.3, "F4": 12, "C1": "150 180", "C2": "M12", "C3": "165 200",
                           "C4": 82,
                           "C5": "32 25 38",
                           "C6": "130 114.3", "C7": "6",
                           "C8": "10 12", "C9": "35.3 38.3"}  #

        self.KS130_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铸铁", "最大承载扭矩T2B(Nm)": 0,
                           "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "2000", "背隙": 0, "输出轴许可径向力": 1325,
                           "输入轴许可径向力": 2100, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 60, "使用温度": "-5℃-60℃",
                           "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                           "尺寸参数表": "", "A1": 292.5, "A2": 187.5, "A3": 147.5, "A4": 200, "A5": 15, "A6": "M12",
                           "A7": 215,
                           "A8": 30,
                           "B1": 170, "B2": 140, "B3": 100, "B4": 120, "B5": 180, "B6": 130, "B7": 16,
                           "F1": 60, "F2": 45, "F3": 48.3, "F4": 14, "C1": "180 190", "C2": "M12", "C3": "200 215",
                           "C4": 116,
                           "C5": "35 28 42",
                           "C6": "114.3 180", "C7": "6",
                           "C8": "10 12", "C9": "38.3 45.3"}  #

        self.KS150_dict = {"性能参数表": "", "额定承载扭矩T2N(Nm)": 35, "箱体材料": "铸铁", "最大承载扭矩T2B(Nm)": 0,
                           "额定输转速n1N(rpm)": "1500", "最大输转速n1N(rpm)": "2000", "背隙": 0, "输出轴许可径向力": 1325,
                           "输入轴许可径向力": 2600, "传动效率(%)": "72%", "噪音(DB)": "≤68", "重量(Kg)": 80, "使用温度": "-5℃-60℃",
                           "制锁": "是", "使用寿命(h)": 10000, "使用维护(h)": "2500小时更换涡轮机油",
                           "尺寸参数表": "", "A1": 340, "A2": 230, "A3": 170, "A4": 240, "A5": 18, "A6": "M12",
                           "A7": 215,
                           "A8": 30,
                           "B1": 200, "B2": 180, "B3": 120, "B4": 145, "B5": 180, "B6": 150, "B7": 18,
                           "F1": 72.5, "F2": 50, "F3": 53.8, "F4": 14, "C1": "180 190", "C2": "M12", "C3": "200 215",
                           "C4": 116,
                           "C5": "35 28 42",
                           "C6": "114.3 180", "C7": "6",
                           "C8": "10 12", "C9": "38.3 45.3"}  #

        self.KS_series_dict = {"KS40": self.KS40_dict, "KS50": self.KS40_dict, "KS63": self.KS63_dict,
                               "KS75": self.KS75_dict, "KS90": self.KS90_dict,
                               "KS110": self.KS110_dict, "KS130": self.KS110_dict, "KS150": self.KS150_dict
                               }
        self.series = self.KS_series_dict
