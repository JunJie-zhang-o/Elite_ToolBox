# from tqdm import tqdm
# from merry import Merry
import paramiko
import time
from loguru import logger
# from inc.Class_merry import MyMerry


class MySftp:
    """提取paramiko模块并封装为sftp模块使用

    Returns:
        object: 根据传入信息已经初始化的sftp对象
    """
    # *测试无线局域网下传输速度大概为2M/s
    # todo:将一些常用有用的ssh指令封装
    # todo:比如创建文件夹，创建文件，修改文件夹和文件的命名
    def __init__(self, hostname: str, port: int, name: str, pawd: str):
        """sftp初始化

        Args:
            hostname (str): 远程主机IP
            port (int): ssh端口号
            name (str): 远程主机名
            pawd (str): 远程主机密码
        """
        self.hostname = hostname
        self.port = port
        self.username = name
        self.password = pawd
        
        
    @logger.catch
    # @MyMerry.merry._try
    def connect(self):
        """创建一个已经连接的sftp
        对象

        Returns:
            object: 已经连接远程主机的sftp对象
        """
        # 创建一个ssh连接会话
        transport = paramiko.Transport((self.hostname, self.port))
        self.__transport = transport
        # 连接远程主机
        transport.connect(username = self.username, password = self.password)
        # 从ssh连接中创建一个sftp对象并返回
        self.sftp = paramiko.SFTPClient.from_transport(transport)


    # 进度条
    # def __mytqdm(self, text):
    #     pgbar = tqdm(range(0, 100), ncols = 100)
    #     for each in pgbar:
    #         pgbar.set_description(str(time.strftime("  %Y-%m-%d %H:%M  : ", time.localtime())+text))
    #         time.sleep(0.005)
    #     pgbar.close()
        

    def __get_file_name(self, path_name: str):

        match_chars = "/"
        return path_name.split(match_chars)[-1]
        

    @logger.catch
    def upload(self, local_path: str, remote_path: str):
        """将本地文件上载至远程主机

        Args:
            local_path (str): 本地文件路径
            remote_path (str): 远程主机文件路径
        """
        # 将本地文件上载至远程主机
        self.sftp.put(local_path, remote_path)
        
        
    @logger.catch
    def upload_time(self, local_path: str, remote_path: str):
        """将本地文件上载至远程主机, 并输出传输时间

        Args:
            local_path (str): 本地文件路径
            remote_path (str): 远程主机文件路径
        """
        # 将本地文件上载至远程主机
        t1 = time.time()
        self.sftp.put(local_path, remote_path)
        logger.info("")
        self.__mytqdm("Upload")
        t2 = time.time()
        logger.info(self.__get_file_name(remote_path)+"的传输时长为%.2fs"%float(t2-t1))
    
    
    # @logger.catch
    def download(self, local_path: str, remote_path: str):
        """将远程主机的文件下载至本地

        Args:
            local_path (str): 本地文件路径
            remote_path (str): 远程主机文件路径
        """
        # 将远程主机下载至本地
        self.sftp.get(remote_path, local_path)
 
 
    # @logger.catch
    def download_time(self, local_path, remote_path):
        """将远程主机的文件下载至本地, 并显示传输时间

        Args:
            local_path (str): 本地文件路径
            remote_path (str): 远程主机文件路径
        """
        t1 = time.time()
        # 将远程主机下载至本地
        self.sftp.get(remote_path, local_path)
        logger.info("")
        self.__mytqdm("Download")
        t2 = time.time()
        logger.info(self.__get_file_name(remote_path)+"的传输时长为%.2fs"%float(t2-t1))
        
    @logger.catch
    def close(self):
        # 关闭ssh连接
        self.__transport.close()
 
if __name__ == "__main__":

    pi = MySftp("172.19.2.82", 22, "pi", "raspberry")
    pi.connect()
    local_file = "01.txt"
    remote_file = "/home/pi/Public/demo01.txt"

    pi.upload_time(local_file, remote_file)
    # logger.info("上载完成")
    pi.close()