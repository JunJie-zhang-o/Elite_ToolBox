from PyQt5.QtWidgets import QMessageBox, QWidget
from loguru import logger
from inc.ui2py.packageAngle import Ui_PackageAngleWindow
from inc.packageAngle.Qthread_package import PackageAngleDownload

class PackageAngle(Ui_PackageAngleWindow,QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect_init()

    def connect_init(self):
        """按钮信号初始化
        """
        self.btn_download_Ec63.clicked.connect(lambda:self.slot_package_angle("63"))
        self.btn_download_Ec66.clicked.connect(lambda:self.slot_package_angle("66"))
        self.btn_download_Ec612.clicked.connect(lambda:self.slot_package_angle("612"))
        pass

    
    def slot_package_angle(self,type):
        """按钮触发事件
        """
        logger.info("PackageAngle download clicked param="+type)
        self.package = PackageAngleDownload(type)
        self.package.sign_processing.connect(self.slot_btn_enable)
        self.package.sign_pgbar.connect(self.slot_pgbar)
        self.package.sign_except.connect(self.slot_except)
        self.package.start()

        
    def slot_except(self,sign_except):
        """异常处理
        """
        if sign_except == "ssh connect error":
            title = "连接失败"
            text = "请检查网络连接是否通畅,\n请检查用户名和密码是否正确"
            
        QMessageBox.warning(self,title,text)



    def slot_pgbar(self,sign_pgbar):
        """进度条
        """
        self.progressBar.setValue(sign_pgbar)
        
    
    def slot_btn_enable(self,sign_processing):
        """按钮控制
        """
        self.processing_state = sign_processing
        if sign_processing:
            self.btn_download_Ec63.setEnabled(not sign_processing)
            self.btn_download_Ec66.setEnabled(not sign_processing)
            self.btn_download_Ec612.setEnabled(not sign_processing)
        if sign_processing == False:
            # self.package.terminate()
            pass