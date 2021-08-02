from PyQt5.QtCore import  QThread,pyqtSignal
from loguru import logger
from merry import Merry
import time

from paramiko import ssh_exception
import inc.global_value as glo
from inc.Class_sftp import MySftp

class PackageAngleDownload(QThread):
    
    sign_processing = pyqtSignal(bool)
    sign_except = pyqtSignal(str)
    sign_pgbar = pyqtSignal(int)
    
    merry = Merry()
    merry.logger.disabled = True
    
    def __init__(self,type) -> None:
        super().__init__()
        logger.info("PackageAngleDownload init")
        self.type = type
        
        packing_63 ="""C00000=89.9995,-90.0000,0.0000,-89.9992,0.0004,0.0008,0.0000,0.0000
C00001=89.9992,-89.9997,146.9994,-89.9996,0.0004,0.0008,0.0000,0.0000
NOP
//该程序为EC63及EC63M装箱角度运行程序，运行程序前必须确认以下两点：
//1,程序与机型匹配；2，机器归于正确零位且拆除负载
MOVJ VJ=100% PL=0
MOVJ VJ=100% PL=0
END"""

        packing_66 = """C00000=89.9997,-90.0000,0.0000,-89.9992,0.0008,0.0008,0.0000,0.0000
C00001=89.9995,-89.9997,148.0028,-89.9996,0.0012,0.0004,0.0000,0.0000
NOP
//该程序为EC66及EC66M装箱角度运行程序，运行程序前必须确认以下两点：
//1,程序与机型匹配；2，机器归于正确零位且拆除负载
MOVJ VJ=100% PL=0
MOVJ VJ=100% PL=0
END"""

        packing_612 ="""C00000=0.0000,-90.0000,0.0003,-90.0000,0.0000,0.0000,0.0000,0.0000
C00001=0.0003,-89.9995,160.0000,-79.9994,0.0003,-0.0003,0.0000,0.0000
C00002=0.0003,-169.9995,160.0000,-79.9997,0.0000,0.0000,0.0000,0.0000
NOP
//该程序为EC612及EC612M装箱角度运行程序，运行程序前必须确认以下两点：
//1,程序与机型匹配；2，机器归于正确零位且拆除负载
MOVJ VJ=100% PL=0
MOVJ VJ=100% PL=0
MOVJ VJ=100% PL=0
END
"""

        self.packing_angle = {"63":packing_63,"66":packing_66,"612":packing_612}
        self.file_name = {"63":"63_packing_angle.jbi","66":"66_packing_angle.jbi","612":"612_packing_angle.jbi"}
        self.ip = glo.get_value("ip")
        self.username = glo.get_value("username")
        self.password = glo.get_value("password")
        self.remote_path = r"/rbctrl/"+self.file_name[self.type]
        self.local_path = r"temp/"+self.file_name[self.type]
        self.robot = MySftp(self.ip,22,self.username,self.password)
        global parm
        parm = self


    @merry._try
    def run(self):
        logger.info("PackageAngleDownload run")
        self.sign_pgbar.emit(0)
        self.sign_processing.emit(True)
        self.sign_pgbar.emit(10)
        
        with open("temp/"+self.file_name[self.type],"w+",encoding="UTF-8") as f:
            f.write(self.packing_angle[self.type])
        
        self.sign_pgbar.emit(30)
        self.robot.connect()
        self.sign_pgbar.emit(50)
        self.robot.upload(self.local_path,self.remote_path)
        self.sign_pgbar.emit(70)

        # 删除本地文件

        time.sleep(1)
        self.sign_pgbar.emit(100)
        self.sign_processing.emit(False)
        
        
    @merry._except(ssh_exception.SSHException)
    def except_SSHException(e):
        global parm
        logger.error("ssh连接错误")
        logger.error(e)
        parm.sign_except.emit("ssh connect error")
               
        
    @merry._finally
    def merry_finally():
        global parm
        logger.info("Packing program process end")
        parm.sign_processing.emit(False)
