from tkinter import messagebox
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QMessageBox, QWidget
from merry import Merry
from loguru import logger
import paramiko
from paramiko import message
import inc.global_value as glo


class Message_box(QThread):
        
        def __init__(self,w,title="",msg=""):
            super().__init__()
            self.w =w
            self.title = title
            self.msg = msg
        
        def run(self):
            QMessageBox.information(self.w, self.title, self.msg)



class MyMerry():
    merry = Merry()
    merry.logger.disabled = True
    catch = merry._try
    


    @merry._except(paramiko.ssh_exception.SSHException)
    def process_ssh_exception(self,*args):
        msg = "远程连接失败，请检查网络连接、用户名及密码"
        logger.info(msg)
        w = glo.get_main_widget()
        self.t=Message_box(w)
        self.t.start()
        self.t.wait()
        logger.info("1212")
        pass
    
    
    # @staticmethod
    @merry._except(ZeroDivisionError)
    def process_zero_division_error(e):
        logger.info('zero_division_error')


    # @staticmethod
    @merry._except(FileNotFoundError)
    def process_file_not_found_error(e):
        logger.info('file_not_found_error')
        

    # @staticmethod
    @merry._except(Exception)
    def process_exception(e):
        logger.info('exception-----------------------------------------------------------------------------')
        
        
    @staticmethod
    @merry._except(AttributeError)    
    def process_attributeError(e):
        logger.info("该变量没有此属性")
        
        
    
        
        
        
    