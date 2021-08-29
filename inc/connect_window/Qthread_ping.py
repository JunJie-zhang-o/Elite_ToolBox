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
        logger.info("NetWorkPing init")


    # @logger.catch()
    def run(self):
        logger.info("NetWorkPing run")
        ip = glo_value.get_value("ip")


        # *当使用subprocess.Popen时，如果打包时不包含cmd窗口，该子进程的输入和输出流异常导致报错，需要将对应的stdin、stdout、stderr进行重定向，同时shell=True可以防止自动弹出cmd黑色窗口
        self.proc1 = subprocess.Popen("ping %s -t"%ip, shell=True ,stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
        logger.info("ping start")
        logger.info(ip)
        while 1:
            # logger.info("reading")
            ping_result = self.proc1.stdout.readline().decode("gbk")
            if  "TTL=" in ping_result:
                # 在线
                self.ping_signal.emit(True)    #反馈信号出去
                # logger.info("true")
            else:
                # 离线
                self.ping_signal.emit(False) #反馈信号出去
                # logger.info("false")


    def stop(self):
        # self.proc1.kill()
        # self.proc1.terminate()
        glo_value.set_value("ip",None)
        glo_value.set_value("username",None)
        glo_value.set_value("password",None)
        self.ping_signal.emit(False)
        self.terminate()
        
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.proc1.pid),stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.STDOUT,shell=True)


