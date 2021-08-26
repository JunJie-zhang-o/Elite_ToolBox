from os import stat
from PyQt5.QtCore import QThread, pyqtSignal
from merry import Merry
from loguru import logger
import inc.global_value as glo_value
import socket

# todo:接收数据不全，需要排查一下问题，尝试一下QSocket


class Get_Log(QThread):
    
    text_log = pyqtSignal(str)
    state = pyqtSignal(bool)
    sign_except = pyqtSignal(str)
    
    merry = Merry()
    merry.logger.disabled = True
    
    def __init__(self) -> None:
        super().__init__()
        global parm
        parm = self

        
    def run(self):
        self.state.emit(False)
        self.sock_connect()
        print(self.data.decode())
        self.text_log.emit(self.data.decode())
        self.state.emit(True)
        self.s.close()
    
    
    @merry._try
    def sock_connect(self):
        ip = glo_value.get_value("ip")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        self.s.connect((ip,8058))
        self.s.send("all\n".encode())
        self.data = self.s.recv(1024)
        print(self.data)
    
    
    @merry._except(ConnectionRefusedError)
    def except_(e):
        global parm
        logger.error("8058 ConnectionRefusedError")
        logger.error(e)
        parm.sign_except.emit("ConnectionRefusedError")
        pass
    
    @merry._except(ConnectionResetError)
    def except_(e):
        global parm
        logger.error("8058 ConnectionResetError")
        logger.error("远程主机强迫关闭了一个现有的连接")
        logger.error(e)
        parm.sign_except.emit("ConnectionResetError")
        pass
    
    @merry._except(socket.timeout)
    def except_(e):
        global parm
        logger.error("8058 recv timeout")
        logger.error(e)
        parm.sign_except.emit("8058 recv timeout")
        pass
    
    
    @merry._finally
    def finally_():
        global parm
        parm.state.emit(True)
        
        
        
        
        
class Save_Log(QThread):
    
    state = pyqtSignal(bool)
    
    def __init__(self,path,text) -> None:
        super().__init__()
        self.path = path
        self.text = text
        
        
    def run(self):
        self.state.emit(False)
        with open(self.path,"w+") as f:
            f.write(self.text)
        self.state.emit(True)
        pass