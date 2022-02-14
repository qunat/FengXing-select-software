# -*- coding: UTF-8 -*-
import os,sys,shutil
def OutPut_all_file_path():
    path = os.getcwd()
    stp_move_to_path="J:\\EBaiduNetdiskDownload\\resource\\EDA75\\3D\\"
    dwg_move_to_path = "J:\\EBaiduNetdiskDownload\\resource\\EDA75\DWG\\"
    file_path_list = []
    path="J:\\EBaiduNetdiskDownload\\EDA75"
    with open("FilePath.ini", "w+") as f:
        for dir, folder, file in os.walk(path):
            for i in file:
                t = "%s\%s" % (dir, i)
                file_path_list.append(t)
        for j in file_path_list:
            if j.endswith("step") or j .endswith("STEP"):
                dis_path=j.split("\\")
                dis_path=stp_move_to_path+dis_path[-1]
                shutil.move(j,dis_path)
            if j.endswith("dwg") or j.endswith("DWG"):
                dis_path = j.split("\\")
                dis_path = dwg_move_to_path + dis_path[-1]
                shutil.move(j, dis_path)
                print(dis_path)

        f.close()

if __name__ == "__main__":
    OutPut_all_file_path()
    print("列表更新完成")
    a1=input("请按任意键结束")
    sys.exit()