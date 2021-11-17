# -*- coding: UTF-8 -*-

from ftplib import FTP  # 加载ftp模块
from ftplib import error_perm
import os
import zipfile
import upyun,re
import copy,time
import shutil
from multiprocessing import queues


"""ZuSYm45YqESN7xas8Eng3C58v5gDDsN2"""#密码
class Ftp_Update():
    def __init__(self, service='cad-upyun', username='loujiandi', passport='ZuSYm45YqESN7xas8Eng3C58v5gDDsN2'):
        pass
        self.up= upyun.UpYun(service, username, passport,timeout=30, endpoint=upyun.ED_AUTO)
        try:
            with open("./serve/serve.ini", "r") as f:
                words = f.readlines()
                self.cloude_name = words[5].replace("cloude_name=", "").strip("\n")  # 获取云端文件夹名字
                f.close()
        except:
            pass
    def Rename_path(self,string=""):
        try:
            file_path=string.split("/")
            rename_file_path="remove_"+file_path[-1]
            path=string.replace(file_path[-1],rename_file_path)
            path="./"+path
            return path
        except:
            pass

    def move_debug(self, origin_path=""):
        try:
            file_path = origin_path.split("/")
            move_path ="./debug"+"/"+file_path[-1]
            #print(origin_path,move_path)
            shutil.move(origin_path, move_path)
        except:
            pass


    def get_now_vision(self):
        with open("./serve/serve.ini", "r") as f:
            words = f.readlines()
            self.now_vision = words[0].replace("vision=", "").strip("\n")
            f.close()
        return self.now_vision
    def get_download_document_num(self):
        pass
        try:
            self.Down_load_file("FilePath.ini")  # 从服务器上下载更新文件目录
            with open("FilePath.ini", "r") as f:
                all_path = f.read()
                FTP_file_path = all_path.split(",")
                f.close()
            return len(FTP_file_path)
        except:
            pass
            print("error")



    def Down_load_file(self,path):

        try:
            with open(path, 'wb') as f:
                filepath=self.cloude_name+path
                self.up.get(filepath, f)
        except Exception as e:
            print(e)


    def OutPut_all_file_path(self):
        path=os.getcwd()
        file_path_list=[]
        with open("FilePath.ini","w+") as f:
            for dir, folder, file in os.walk(path):
                for i in file:
                    t = "%s\%s" % (dir, i)
                    file_path_list.append(t)
            for j in file_path_list:
                file_size =str(os.path.getsize(j))#获取文件大小
                file_date = str(os.path.getmtime(j))#获取文件最后保存时间
                j=j.split('\\')
                ls_path=path.split("\\")
                ls_path.reverse()
                start=j.index(ls_path[0])+1#去除最初级目录
                end=len(j)
                path_1=""

                for k in range(start,end):
                    if k==end-1:
                        path_1 = path_1 + j[k]
                    else:
                        path_1=path_1+j[k]+"\\"

                f.write(path_1)
                f.write("!")
                f.write(file_size)
                f.write("!")
                f.write(file_date)
                f.write(",")
            f.close()


    def Check_dir(self,list=[],speed_list=[]):
        try:
            self.Delete_Document()
        except:
            pass

        try:
            # 获取服务器上所有的文件path
            self.Down_load_file("FilePath.ini")#从服务器上下载更新文件目录
            with open("FilePath.ini","r") as f:
                all_path=f.read()
                FTP_file_path=all_path.split(",")
                f.close()

            #获取本地文件夹所有文件的path
            path = os.getcwd()
            file_path_list = []
            for dir, folder, file in os.walk(path):
                for i in file:
                    t = "%s\%s" % (dir, i)
                    file_path_list.append(t)
            #遍历服务器上文件，判断文件是否为最新文件 是否需要更新
            for file in FTP_file_path:
                current_file=copy.deepcopy(file)
                file=file.split("!")
                new_file=path+'\\'+file[0]#在用户计算机对应的文件的路径
                if "Ftp_Update.py" in new_file or "Upyun_Update.py" in new_file :
                    continue
                if os.path.exists(new_file):
                    pass
                    try:
                        pass
                        if float(os.path.getmtime(new_file)) >float(file[2]) or float(
                                (os.path.getsize(new_file))) == float(file[1])  :
                            pass
                            speed=0
                            list.append(file)
                            speed_list.append(speed)
                            continue
                        else:
                            try:  # 需要更新已经有的文件
                                #-----------------------重命名 并删除文件--------------------------
                                new_file = file[0]
                                new_file = new_file.replace("\\", "/")
                                to_rename_filepath="./"+new_file#要被重命名的文件路径
                                try:
                                    new_name_path=self.Rename_path(new_file)
                                    if os.path.exists(new_name_path):
                                        self.move_debug(new_name_path)#如果有残余的文件则先移除

                                    os.rename(to_rename_filepath,new_name_path)
                                    self.move_debug(new_name_path)#将重命名文件移动到debug文件
                                except Exception as e:
                                    print(e)

                                start_time = time.time()#开始下载计时
                                self.Down_load_file(new_file)


                                speed=float(file[1])/(time.time()-start_time)/1024**2
                            except:
                                pass
                    except:
                        pass

                else:#更新没有的文件
                    pass
                    try:
                        new_file =file[0].split("\\")
                        new_file.reverse()
                        start=len(file[0])-len(new_file[0])
                        new_file=file[0][0:start]
                        os.makedirs(new_file)  # 可生成多层递归目录
                        download_file=file[0].replace("\\","/")
                        start_time=time.time()
                        self.Down_load_file(download_file)
                        speed = float(file[1]) / (time.time() - start_time) / 1024**2


                    except:
                        pass
                        download_file=file[0]
                        download_file=download_file.replace("\\", "/")
                        start_time=time.time()
                        self.Down_load_file(download_file)
                        speed = float(file[1]) / (time.time() - start_time) / 1024**2

                try:
                    #percent=FTP_file_path.index(current_file)/len(FTP_file_path)*100
                    #print("已完成：%2.2f%%,下载速度：%2.2fM/S"%(percent,speed),flush=True)
                    list.append(file)
                    speed_list.append(speed)
                except Exception as e:
                    pass
                    print(e)





        except:
            pass

    def Delete_Document(self,path="./Pic"):
        try:
            shutil.rmtree(path)
        except Exception as e:
            pass
            print(e)



if __name__ == "__main__":
    pass
    new_ftp = Ftp_Update()
    print(new_ftp.cloude_name)
    #new_ftp.Check_dir()
    #new_ftp.OutPut_all_file_path()


