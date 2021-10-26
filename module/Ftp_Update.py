# -*- coding: UTF-8 -*-

from ftplib import FTP  # 加载ftp模块
from ftplib import error_perm
import os
import zipfile
# ftp.connect("182.92.199.226") #连接的ftp sever和端口
# ftp.login("user","12345")#连接的用户名，密码如果匿名登录则用空串代替即可
# print(ftp.getwelcome()) # 获得欢迎信息
# ftp.dir() #显示目录下文件信息
# file_handler = open("D:\\共享\\bbb.stp", 'wb')
# ftp.retrbinary('RETR ' + 'QEH30CA.stp', file_handler.write)

class Ftp_Update():
    def __init__(self, ip="39.102.63.131", user="user", passport="12345",vision="1.0.1"):
        pass
        self.ftp = FTP()  # 设置FTP类
        uesr_list=[{"ip":"39.102.63.131","user":"user","passport":"12345"},
                   {"ip":"122.247.241.215","user":"user","passport":"12345"},
                   {"ip":"39.102.63.131","user":"user","passport":"12345"}]
        for i in uesr_list:
            try:
                pass
                self.ftp.connect(i["ip"])
                self.ftp.login(i["user"], i["passport"])
                self.ftp.encoding = 'utf-8'
                self.ftp.set_pasv(False)#关闭被动链接
                print("登录成功")
                error=0
                break
            except:
                error=1
        try:#启用备选ip
            if error == 1:
                with open("./serve/serve.ini", "r") as f:
                    words = f.readlines()
                    self.now_vision=words[0].replace("vision=","").strip("\n")
                    ip=words[1].replace("ip=","").strip("\n")
                    uesr=words[2].replace("user=","").strip("\n")
                    passport=words[3].replace("passport=","").strip("\n")
                    i={"ip":ip,"user":user,"passport":passport}
                    self.ftp.connect(i["ip"])
                    self.ftp.login(i["user"], i["passport"])
                    self.ftp.encoding = 'utf-8'
                    self.ftp.set_pasv(False)  # 关闭被动链接
                    f.close()
        except:
            pass



    def get_now_vision(self):
        with open("./serve/serve.ini", "r") as f:
            words = f.readlines()
            self.now_vision = words[0].replace("vision=", "").strip("\n")
            f.close()
        return self.now_vision

    def Down_load_file(self,path):
        try:
            pass
            download_fiml=os.getcwd()
            bufsize = 4096  # 设置缓冲块大小
            #download_fiml = download_fiml + "\\" + path
            download_fiml = "c:\\3Dsource" + "\\" + path
            print(download_fiml)
            fp = open(path, 'wb')  # 以写模式在本地打开文件
            # 下载文件
            command_result = self.ftp.retrbinary('RETR ' + path, fp.write, bufsize)
            self.ftp.set_debuglevel(0)  # 关闭调试
            fp.close()
        except:
            pass


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
                file_date = str(os.path.getatime(j))#获取文件最后保存时间
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


    def Check_dir(self):
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
                file=file.split("!")
                new_file=path+'\\'+file[0]#在用户计算机对应的文件的路径
                if "Ftp_Update.py" in new_file:
                    continue
                if os.path.exists(new_file):
                    pass
                    if str(os.path.getatime(new_file))==file[2] and str(os.path.getsize(new_file))==file[1]:
                        pass
                        print("无需更新")
                    else:
                        try:#需要更新已经有的文件
                            new_file = file[0]
                            #self.Down_load_file(new_file)
                        except:
                            pass
                else:#更新没有的文件
                    pass
                    try:
                        new_file =file[0].split("\\")
                        new_file.reverse()
                        start=len(file[0])-len(new_file[0])
                        new_file=file[0][0:start]
                        down_load_file=file[0]
                        os.makedirs(new_file)  # 可生成多层递归目录

                        download_fiml="c:\\3Dsource\\"+download_fiml
                        print(down_load_file)
                        self.Down_load_file(down_load_file)

                    except:
                        pass
                        download_fiml=".\\"+file[0]
                        print(download_fiml)
                        self.Down_load_file(file[0])




        except:
            pass




if __name__ == "__main__":
    pass
    new_ftp = Ftp_Update()
    new_ftp.get_now_vision()
    #new_ftp.Check_dir()


