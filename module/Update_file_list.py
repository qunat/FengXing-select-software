# -*- coding: UTF-8 -*-
import os,sys
def OutPut_all_file_path():
    path = os.getcwd()
    file_path_list = []
    with open("FilePath.ini", "w+") as f:
        for dir, folder, file in os.walk(path):
            for i in file:
                t = "%s\%s" % (dir, i)
                file_path_list.append(t)
        for j in file_path_list:
            file_size = str(os.path.getsize(j))  # 获取文件大小
            file_date = str(os.path.getmtime(j))  # 获取文件最后保存时间
            j = j.split('\\')
            ls_path = path.split("\\")
            ls_path.reverse()
            start = j.index(ls_path[0]) + 1  # 去除最初级目录
            end = len(j)
            path_1 = ""

            for k in range(start, end):
                if k == end - 1:
                    path_1 = path_1 + j[k]
                else:
                    path_1 = path_1 + j[k] + "\\"

            f.write(path_1)
            f.write("!")
            f.write(file_size)
            f.write("!")
            f.write(file_date)
            f.write(",")
        f.close()

if __name__ == "__main__":
    OutPut_all_file_path()
    print("列表更新完成")
    a1=input("请按任意键结束")
    sys.exit()