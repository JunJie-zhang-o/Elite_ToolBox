# coding:utf-8
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QStackedWidget
from loguru import logger
from inc.framelesswindow import FramelessWindow
from inc.UI_LeftTabWidget import LeftTabWidget
from inc.UI_XmlWidget import CommentWidget
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
        # glo._init_window_var()
        # glo.set_main_widget()
        
    def frameless_init(self):
        # 设置层叠样式
        self.setStyleSheet('background:white')
        # 标题栏置顶
        # self.titleBar.raise_()
        # 设置标题
        self.setWindowTitle('PyQt Frameless Window')


    def left_widgets_init(self):
        left_tab_lists=["注释修改","8056","轨迹在线提取","轨迹速度规划"]
        self.left_widget=LeftTabWidget(left_tab_lists)
        # self.left_widget.setParent(self)
        self.down_layout.addWidget(self.left_widget)
        self.left_widget.setCurrentRow(0)       #默认选择第一行
        
        
    def right_widgets_init(self):
        self.right_widget=QStackedWidget(objectName="right_widget")
        self.down_layout.addWidget(self.right_widget)
        self.right_widget.addWidget(CommentWidget())
        self.right_widget.addWidget(QLabel("2"))
        self.right_widget.addWidget(QLabel("3"))


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


def high_dpi_setting():
    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)



if __name__ == "__main__":
    
    # print(sys.path)
    print(os.getcwd())
    high_dpi_setting()
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())
