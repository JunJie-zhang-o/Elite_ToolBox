from PyQt5.QtCore import QThread, pyqtSignal
from merry import Merry
from loguru import logger
import inc.global_value as glo_value
import socket
import time

# todo:接收数据不全，需要排查一下问题，尝试一下QSocket
# *:接收数据不全，问题已经排查，需要循环读取，机器人发送的字节超出1024字节

# todo:接收格式出现部分不正确
# todo:已经排查，接收时并未达到对应的缓存区大小就已经接收

# *解决方法：
# *等待缓存器满，是否会存在一直等待的情况
# *中间加延时解决
# *textedit 追加显示会自己换行


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

    @merry._try       
    def run(self):
        self.state.emit(False)
        ip = glo_value.get_value("ip")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)
        self.s.connect((ip,8058))
        self.s.send("all\n".encode())
        self.data = ""
        while True:
            try :
                time.sleep(0.01)
                self.data = self.s.recv(1024)
                
                self.text_log.emit(self.data.decode())


            except (socket.timeout) as e :
                logger.info("log 读取完成")
                break
            
        self.state.emit(True)
        self.s.close()
    
    
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
    
    
    @merry._except(Exception)
    def except_(e):
        global parm
        logger.error(e)
        pass
    
    
    @merry._finally
    def finally_():
        global parm
        parm.state.emit(True)
        parm.s.close()
        
        
        
        
        
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