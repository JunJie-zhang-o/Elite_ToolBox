from PyQt5.QtCore import  QThread,pyqtSignal
from loguru import logger
from merry import Merry
from paramiko import ssh_exception
import time

import paramiko
from Class_excel import Excel_read_write
from inc.Class_sftp import MySftp
import inc.global_value as glo_value




class Up_load(QThread):
    """多线程：上载按钮触发，从机器人远端下载文件，并解析至UI界面
    """
    
    pgbar_percent = pyqtSignal(int) 
    comment_var = pyqtSignal(list)
    exception_sign = pyqtSignal(str)

    merry = Merry()
    merry.logger.disabled = True


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
        global parm
        parm = self


    @merry._try
    def run(self):
        self.exception_sign.emit("btn handle start")
        logger.info("upload btn handle start")
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
                time.sleep(0.005)

                   
    def get_key(self,i,j):
        var = ["B","I","D","P","V"]
        return var[i]+str(j)


    @merry._except(ssh_exception.SSHException)
    def except_SSHException(e):
        global parm
        logger.error("ssh连接错误")
        logger.error(e)
        parm.exception_sign.emit("ssh connect error")

        
    @merry._except(IOError)
    def except_SSHException(e):
        global parm
        logger.error("remote No such file错误")
        logger.error(e)
        parm.exception_sign.emit("No such file")

        
    @merry._finally
    def merry_finally():
        global parm
        logger.info("upload btn handle end")
        parm.exception_sign.emit("btn handle end")
        del parm
        
    
class Download(QThread):
    """多线程：保存按钮触发，从界面中生成xml文件，并将本地文件下载至机器人
    """    
    pgbar_var = pyqtSignal(int)
    exception_sign = pyqtSignal(str)
    
    merry = Merry()
    merry.logger.disabled = True

    
    def __init__(self,data_list: list,xml_obj: object):
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
        global parm
        parm = self
        
        
    @merry._try
    def run(self):
        self.exception_sign.emit("btn handle start")
        logger.info("download btn handle start")
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
        # self.robot.close()
        self.pgbar_var.emit(100)

            
    @merry._except(ssh_exception.SSHException)
    def except_SSHException(e):
        global parm
        logger.error("ssh连接错误")
        logger.error(e)
        parm.exception_sign.emit("ssh connect error")
        

    @merry._except(IOError)
    def except_IOException(e):
        global parm
        logger.error("remote No such file错误")
        logger.error(e)
        parm.exception_sign.emit("No such file")
        
    
    @merry._finally
    def merry_finally(*args):
        global parm
        logger.info("download btn handle end")
        parm.exception_sign.emit("btn handle end")
        del parm


class LoadExcel(QThread):
    """加载指令格式Excel文件
    """
    sign_load_error = pyqtSignal(int)       #错误提示
    sign_comment_var = pyqtSignal(list)     #读取到的注释
    sign_pgbar_percent = pyqtSignal(int)    #当前的读取进度
    sign_loading = pyqtSignal(bool)
    
    
    def __init__(self,filepath,language=0):
        super().__init__()
        self.excel_obj = Excel_read_write()
        self.filepath = filepath
        self.language = language 


    def run(self):
        self.sign_loading.emit(True)
        self.sign_pgbar_percent.emit(0)
        self.excel_obj.creat_read_wbook(self.filepath)
        self.sign_pgbar_percent.emit(20)
        # 逐sheet读取并检查，格式正确的显示界面，否则提示
        if self.check_excel_sheet_name():
            self.sign_pgbar_percent.emit(20)
            pgbar_num = 40
            for i in range(self.excel_obj.read_sheet_objects.__len__()):
                print(i)
                if self.check_title(self.excel_obj.read_sheet_objects[i]):

                    comment_lists = self.excel_obj.read_all_coment(self.excel_obj.read_sheet_objects[i])
                    
                    # 解释注释，以字典形式发送
                    for j in range(comment_lists[self.language].__len__()):
                        self.sign_comment_var.emit([self.get_key(i,j),comment_lists[self.language][j]])
                        self.sign_pgbar_percent.emit( pgbar_num + 12*i + 12*j/255 )
                        time.sleep(0.005)
                else:
                    self.sign_pgbar_percent.emit( pgbar_num + 12*(i+1) )
                    continue
        self.sign_loading.emit(False)

            
            
    def check_excel_sheet_name(self):
        """检查sheet name是否正确
        """
        sheet_name = ["B变量注释","I变量注释","D变量注释","P变量注释","V变量注释"]
        for i in range(self.excel_obj.read_sheet_numbers):
            if self.excel_obj.read_sheet_names[i] != sheet_name[i]:
                    self.sign_load_error.emit(1)    #sign_load_error = 1 为表格表单名匹配错误
                    return False
        return True
    

    def check_title(self,sheet:object):
        """检查第一行和第一列的数据是否为标准数据
        """
        mark = sheet.name[:1]
        first_line = ["变量序号","中文注释","英文注释","日文注释","韩文注释","其他注释"]
        coment_list = [mark+"%03d"%i for i in range(256)]
        read_column_list = sheet.col_values(0,1,257)
        read_first_line = sheet.row_values(0,0,5)
        for i in range(coment_list.__len__()):
            if i < 5:
                if first_line[i] != read_first_line[i]:
                    self.sign_load_error.emit(2)    #sign_load_error = 2 为表格第一行title错误
                    return False
            if coment_list[i] != read_column_list[i]:
                self.sign_load_error.emit(3)        #sign_load_error = 3 为表格第一列序号错误
                return False
        return True
    
    def get_key(self,i,j):
        var = ["B","I","D","P","V"]
        return var[i]+str(j)
        
class CreatExcel(QThread):
    
    sign_creating = pyqtSignal(bool)
    sign_create_except = pyqtSignal(int)
    sign_pg_bar = pyqtSignal(int)
    
    merry = Merry()
    merry.logger.disabled = True
    
    def __init__(self,filepath,excel_data_list,language=0,) -> None:
        super().__init__()
        self.file_path = filepath
        self.language = language
        self.Creat_excel = Excel_read_write()
        self.excel_data_list = excel_data_list
        global parm
        parm = self
        
    @merry._try
    def run(self,*args):
        self.sign_pg_bar.emit(0)
        self.sign_creating.emit(True)
        self.Creat_excel.creat_write_wbook(self.Creat_excel.sheet_name)
        self.sign_pg_bar.emit(10)
        comment_num=["B","I","D","P","V"]
        for i in range(len(self.excel_data_list)):
            print(i)
            self.Creat_excel.write_row_sheet(self.Creat_excel.write_sheet_list[i],0,0,["变量序号","中文注释","英文注释","日文注释","韩文注释","其他注释"])
            self.Creat_excel.write_column_sheet(self.Creat_excel.write_sheet_list[i],1,0,[comment_num[i]+"%03d"%j for j in range(256)])
            self.Creat_excel.write_column_sheet(self.Creat_excel.write_sheet_list[i],1,self.language+1,self.excel_data_list[i])
            self.sign_pg_bar.emit(10+(i+1)*15)
        # 保存
        self.Creat_excel.save_wbook(self.file_path)
        self.sign_pg_bar.emit(100)
        self.sign_creating.emit(False)
        pass
    
    
    @merry._except(PermissionError)
    def except_PermissionError(e):
        global parm
        logger.error("PermissionError错误")
        logger.error(e)
        parm.sign_create_except.emit(1) 
        
        
    @merry._finally
    def merry_finally(*args):
        global parm
        logger.info("Creat btn handle end")
        parm.sign_creating.emit(False)
        del parm