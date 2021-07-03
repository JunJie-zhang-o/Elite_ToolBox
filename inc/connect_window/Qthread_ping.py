from PyQt5.QtCore import  QThread,pyqtSignal
import subprocess

from loguru import logger
import inc.global_value as glo_value


class NetWorkPing(QThread):
    """多线程用ping命令实时检测网络状态，使连接图标实时更改
    """
    ping_signal = pyqtSignal(bool) 

    
    def __init__(self):
        super().__init__()


    # @logger.catch()
    def run(self):
        ip = glo_value.get_value("ip")
        self.proc1 = subprocess.Popen("ping %s -t"%ip,stdout=subprocess.PIPE)
        logger.info("ping start")
        logger.info(ip)
        while 1:
            # logger.info("reading")
            ping_result = self.proc1.stdout.readline().decode("gbk")
            if  "TTL" in ping_result:
                # 在线
                self.ping_signal.emit(True)    #反馈信号出去
                # logger.info("true")
            else:
                # 离线
                self.ping_signal.emit(False) #反馈信号出去
                # logger.info("false")


    def stop(self):
        self.proc1.kill()
        glo_value.set_value("ip",None)
        glo_value.set_value("username",None)
        glo_value.set_value("password",None)
        self.ping_signal.emit(False)
        self.terminate()


