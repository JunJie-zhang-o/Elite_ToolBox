from PyQt5.QtCore import  QThread,pyqtSignal
import time
from PyQt5.QtWidgets import QMessageBox

from loguru import logger
import paramiko
from inc.Class_sftp import MySftp
import inc.global_value as glo_value




class Up_load(QThread):
    """多线程：上载按钮触发，从机器人远端下载文件，并解析至UI界面
    """
    
    pgbar_percent = pyqtSignal(int) 
    comment_var = pyqtSignal(list)
    exception_sign = pyqtSignal(int)

    def __init__(self,xml_obj):
        super().__init__()
        
        self.ip = glo_value.get_value("ip")
        self.port = 22
        self.username = glo_value.get_value("username")
        self.password = glo_value.get_value("password")
        self.remote_path = r"/rbctrl/var_note.xml"
        self.local_path = r"temp/var_note.xml"
        
        self.xml_obj = xml_obj
        
        self.robot = MySftp(self.ip,self.port,self.username,self.password)
        



    def run(self):
        try:
            self.robot.connect()
            self.pgbar_percent.emit(0)
            time.sleep(2)
            # 从机器人中下载对应的文件
            self.robot.download(self.local_path,self.remote_path)
            self.pgbar_percent.emit(18)
            time.sleep(2)
            self.robot.close()
            self.pgbar_percent.emit(20)
            # 解析
            self.xml_obj.read_xml(self.local_path)
            self.pgbar_percent.emit(36)
            pgbar_num = 0
            for i in range(self.xml_obj.comment_lists.__len__()):
                for j in range(self.xml_obj.comment_lists[i].__len__()):
                    self.comment_var.emit([self.get_key(i,j),self.xml_obj.comment_lists[i][j]])
                    pgbar_num = pgbar_num + 0.05
                    self.pgbar_percent.emit( 37 + pgbar_num )
                    # logger.info(pgbar_num+36)
                    time.sleep(0.005)
        except :
            self.exception_sign.emit(1)
            
                
    def get_key(self,i,j):
        var = ["B","I","D","P","V"]
        return var[i]+str(j)

    
class Download(QThread):
    """多线程：保存按钮触发，从界面中生成xml文件，并将本地文件下载至机器人
    """    
    pgbar_var = pyqtSignal(int)
    
    def __init__(self,data_list: list,xml_obj):
        self.data_list = data_list
        super().__init__()
        self.ip = glo_value.get_value("ip")
        self.port = 22
        self.username = glo_value.get_value("username")
        self.password = glo_value.get_value("password")
        self.remote_path = r"/rbctrl/var_note.xml"
        self.local_path = r"temp/var_note1.xml"
        
        self.xml_obj = xml_obj
        
        self.robot = MySftp(self.ip,self.port,self.username,self.password)
        
        
    def run(self):
        self.pgbar_var.emit(0)
        self.robot.connect()
        self.pgbar_var.emit(10)
        # 生成xml文件
        self.xml_obj.comment_lists = self.data_list.copy()
        self.pgbar_var.emit(20)
        time.sleep(0.5)
        self.xml_obj.comment_2_dom()
        self.pgbar_var.emit(30)
        self.xml_obj._xml_updata()
        self.pgbar_var.emit(40)
        self.xml_obj.xml_write(self.local_path)
        time.sleep(0.5)
        self.pgbar_var.emit(75)
        # 从本地上传至机器人远端
        self.robot.upload(self.local_path,self.remote_path)
        time.sleep(0.5)
        self.pgbar_var.emit(95)
        self.robot.close()
        self.pgbar_var.emit(100)