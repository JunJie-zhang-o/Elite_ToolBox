# coding:utf-8
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QStackedWidget
from loguru import logger
from inc.framelesswindow import FramelessWindow
from inc.UI_LeftTabWidget import LeftTabWidget
from inc.xml_widget.UI_XmlWidget import CommentWidget
from inc.packageAngle.UI_packageAngle import PackageAngle
from inc.port_8056.UI_8056 import UI_8056
import inc.global_value as glo


class Window(FramelessWindow):
    """ 测试无边框窗口 """

    def __init__(self, parent=None): 
        super().__init__(parent=parent)
        self.frameless_init()
        self.left_widgets_init()
        self.right_widgets_init()
        self.down_style_init()
        self.logger_init()
        self.connect_ping_sign()
        
    def frameless_init(self):
        # 设置层叠样式
        self.setStyleSheet('background:white')
        # 标题栏置顶
        # self.titleBar.raise_()
        # 设置标题
        self.setWindowTitle('ELite ToolBoxs')
        # 设置图标
        self.setWindowIcon(QIcon("src\icon\ToolBox.ico"))


    def left_widgets_init(self):
        left_tab_lists=["注释修改","8056","装箱程序","Plot","变量监视"]
        self.left_widget=LeftTabWidget(left_tab_lists)
        # self.left_widget.setParent(self)
        self.down_layout.addWidget(self.left_widget)
        self.left_widget.setCurrentRow(0)       #默认选择第一行
        
        
    def right_widgets_init(self):
        self.right_widget=QStackedWidget(objectName="right_widget")
        self.down_layout.addWidget(self.right_widget)
        self.comment_widget = CommentWidget()
        self.right_widget.addWidget(self.comment_widget)
        self.widget_8056 = UI_8056()
        self.right_widget.addWidget(self.widget_8056)
        self.package_angle_window = PackageAngle()
        self.right_widget.addWidget(self.package_angle_window)
        self.right_widget.addWidget(QLabel("已经在做啦，进度0%"))
        self.right_widget.addWidget(QLabel("已经在做啦，进度0%"))


    def down_style_init(self):
        # 左侧list与右侧stack关联
        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)
        # 去掉左侧list的边框
        self.left_widget.setFrameShape(QListWidget.NoFrame)
        # 去掉滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 设置下方布局的比例
        self.down_layout.setStretch(1,2)


    def logger_init(self):
        """日志记录初始化
        """
        logger.add('log/{time:YYYYMMDD}.log', format = "{time:YYYY-MM-DD HH:mm} : {message}", encoding = "utf-8", rotation = "1 days", retention = "30 days")


    def connect_ping_sign(self):
        """在主文件里定义 ping信号，方便后续其他页面的按钮互锁
        """
        self.titleBar.connect_info_widget.ping.ping_signal.connect(self.slot_ping_sign)

    @logger.catch()
    def slot_ping_sign(self,ping_signal,*args):
        # pass
        """ping信号的槽函数，网络没有联通的情况下，部分按钮不能点击
        """
        # 注释界面按钮控制
        if ping_signal :
            # 上载按钮
            self.comment_widget.upload_btn.setEnabled(True)
            self.comment_widget.download_btn.setEnabled(True)
            if hasattr(self.comment_widget,"up_load") and self.comment_widget.except_signal == "btn handle start":

                self.comment_widget.upload_btn.setEnabled(False)
                self.comment_widget.download_btn.setEnabled(False)

            elif  hasattr(self.comment_widget,"load_excel") and hasattr(self.comment_widget,"sign_loading_state") and self.comment_widget.sign_loading_state == True:
                self.comment_widget.upload_btn.setEnabled(False)
                self.comment_widget.download_btn.setEnabled(False)
                
            elif  hasattr(self.comment_widget,"Creat_excel") and hasattr(self.comment_widget,"sign_loading_state") and self.comment_widget.sign_loading_state == True:
                self.comment_widget.upload_btn.setEnabled(False)
                self.comment_widget.download_btn.setEnabled(False)
        else:
            self.comment_widget.upload_btn.setEnabled(ping_signal)
            self.comment_widget.download_btn.setEnabled(ping_signal)
        # 8056界面控制
        if ping_signal :
            self.widget_8056.btn_start_recv.setEnabled(True)
        else:
            self.widget_8056.btn_start_recv.setEnabled(False)
        # 打包界面按钮控制
        if ping_signal :
            self.package_angle_window.btn_download_Ec63.setEnabled(True)
            self.package_angle_window.btn_download_Ec66.setEnabled(True)
            self.package_angle_window.btn_download_Ec612.setEnabled(True)
            if hasattr(self.package_angle_window,"package") and hasattr(self.package_angle_window,"processing_state") and self.package_angle_window.processing_state == True:
                self.package_angle_window.btn_download_Ec63.setEnabled(False)
                self.package_angle_window.btn_download_Ec66.setEnabled(False)
                self.package_angle_window.btn_download_Ec612.setEnabled(False)
        else:
            self.package_angle_window.btn_download_Ec63.setEnabled(False)
            self.package_angle_window.btn_download_Ec66.setEnabled(False)
            self.package_angle_window.btn_download_Ec612.setEnabled(False)

        
def is_cerate_file(name:str):
    """检查当前工作目录是否存在某个文件夹，没有的话自动创建,
    防止某些写文件出错
    Args:
        name (str): 目录名称
    """
    if not os.path.isdir(name):
        os.mkdir(name)



def high_dpi_setting():
    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)



if __name__ == "__main__":
    
    logger.info("")
    is_cerate_file("temp")
    # print(sys.path)
    # print(os.getcwd())
    # high_dpi_setting()
    app = QApplication(sys.argv)
    demo = Window()
    logger.info("ToolBox Open")
    demo.show()
    sys.exit(app.exec_())
    