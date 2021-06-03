# coding:utf-8

from ctypes import resize
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QToolButton, QWidget
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture
from loguru import logger

from .title_bar_buttons import MaximizeButton, ThreeStateToolButton
from inc.UI_connect_info import connect_info


class TitleBar(QWidget):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(1360, 40)
        # 创建记录下标的列表，里面的每一个元素为元组，第一个元素为stackWidget名字，第二个为Index
        self.stackWidgetIndex_list = []
        # 连接对话框初始化
        self.connect_info_init()
        # 实例化小部件
        self.__createButtons()
        # 初始化界面
        self.__initWidget()
        self.__adjustButtonPos()


    def __createButtons(self):
        """ 创建各按钮 """
        self.minBt = ThreeStateToolButton(
            {'normal': r'inc\resource\images\title_bar\最小化按钮_normal_57_40.png',
             'hover': r'inc\resource\images\title_bar\最小化按钮_hover_57_40.png',
             'pressed': r'inc\resource\images\title_bar\最小化按钮_pressed_57_40.png'}, (57, 40), self)
        self.closeBt = ThreeStateToolButton(
            {'normal': r'inc\resource\images\title_bar\关闭按钮_normal_57_40.png',
             'hover': r'inc\resource\images\title_bar\关闭按钮_hover_57_40.png',
             'pressed': r'inc\resource\images\title_bar\关闭按钮_pressed_57_40.png'}, (57, 40), self)
        self.maxBt = MaximizeButton(self)
        self.button_list = [self.minBt, self.maxBt, self.closeBt]
       
        # 窗口图标和标题
        self.icon_and_title_bar_init()
        # 设置和log图标设置
        self.settingbtn_and_logbtn_init()
        # 连接按钮
        self.connect_btn_init()





    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(50)
        self.setAttribute(Qt.WA_StyledBackground)
        self.__setQss()
        # 将按钮的点击信号连接到槽函数
        self.minBt.clicked.connect(self.window().showMinimized)
        self.maxBt.clicked.connect(self.__showRestoreWindow)
        self.closeBt.clicked.connect(self.window().close)


    def __adjustButtonPos(self):
        """ 初始化小部件位置 """
        self.closeBt.move(self.width() - 57, 0)
        self.maxBt.move(self.width() - 2 * 57, 0)
        self.minBt.move(self.width() - 3 * 57, 0)
        self.set_btn.move(self.width()-4*57-1,0)
        self.log_btn.move(self.width()-5*57-1,0)
        self.title_line.move(self.width()-3*57-3,0)


    def resizeEvent(self, e: QResizeEvent):
        """ 尺寸改变时移动按钮 """
        self.__adjustButtonPos()
        

    def mouseDoubleClickEvent(self, event):
        """ 双击最大化窗口 """
        self.__showRestoreWindow()


    def mousePressEvent(self, event):
        """ 移动窗口 """
        # 判断鼠标点击位置是否允许拖动
        if self.__isPointInDragRegion(event.pos()):
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            event.ignore()


    def __showRestoreWindow(self):
        """ 复原窗口并更换最大化按钮的图标 """
        if self.window().isMaximized():
            self.window().showNormal()
            # 更新标志位用于更换图标
            self.maxBt.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxBt.setMaxState(True)


    def __isPointInDragRegion(self, pos) -> bool:
        """ 检查鼠标按下的点是否属于允许拖动的区域 """
        x = pos.x()
        # 如果最小化按钮看不见也意味着最大化按钮看不见
        right = self.width() - 57 * 3 if self.minBt.isVisible() else self.width() - 57
        return (0 < x < right)


#------------------------------------------------------------#


    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'inc\resource\qss\title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


    def spilt_line_V(self,parent):
        """返回一个竖直分割线对象
        """
        line =QFrame(parent)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Plain)
        return line
    
    
    def icon_and_title_bar_init(self):
         # 图标和标题栏
        self.icon=QPixmap(r"inc\resource\images\title_bar\logo-single.png")
        self.icon_lable=QLabel("icon",self,objectName="icon_lable")
        self.icon_lable.setPixmap(self.icon)
        self.icon_lable.setScaledContents(True)     #图标大小自适应lable
        self.appName=QLabel("Elite ToolBoxs",self,objectName="appName")
        self.appName.resize(80,50)
        self.appName.move(65,0)
    
    
    def settingbtn_and_logbtn_init(self):
        """设置按钮和日志按钮 
        """
        self.set_btn = ThreeStateToolButton(
            {'normal': r'inc\resource\images\title_bar\setting.png',
             'hover': r'inc\resource\images\title_bar\setting1.png',
             'pressed': r'inc\resource\images\title_bar\setting1.png'}, (57, 40), self)

        self.log_btn = ThreeStateToolButton(
            {'normal': r'inc\resource\images\title_bar\log.png',
             'hover': r'inc\resource\images\title_bar\log1.png',
             'pressed': r'inc\resource\images\title_bar\log1.png'}, (57, 40), self)
        # 分割线
        self.title_line= self.spilt_line_V(self)
        self.title_line.setObjectName("title_line")
        # 切换悬浮的鼠标样式
        self.set_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.log_btn.setCursor(QCursor(Qt.PointingHandCursor))
    
    
    def connect_btn_init(self):
        """创建两种状态的连接按钮，分别对应已连接和未连接的装填
        """
        self.connected_btn = ThreeStateToolButton(
        {'normal': r'src\icon\connected1.png',
            'hover': r'src\icon\connected0.png',
            'pressed': r'src\icon\connected0.png'}, (57, 40), self)
        self.connected_btn.move(350,0)
        self.connected_btn.setHidden(True)
        self.connected_btn.setToolTip("连接状态：已连接")
        self.connected_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.connected_btn.clicked.connect(self.connect_connect_info)

        self.disconnect_btn=ThreeStateToolButton(
        {'normal': r'src\icon\disconnect1.png',
            'hover': r'src\icon\disconnect0.png',
            'pressed': r'src\icon\disconnect0.png'}, (57, 40), self)
        self.disconnect_btn.move(350,0)
        self.disconnect_btn.setHidden(False)
        self.disconnect_btn.setToolTip("连接状态：未连接")
        self.disconnect_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.disconnect_btn.clicked.connect(self.connect_connect_info)
        

    def connect_info_init(self):
        """初始化连接界面，并将连接状态连接至两个按钮的显示
        """
        self.connect_info_widget = connect_info()
        self.connect_info_widget.ping.ping_signal.connect(self.connect_connect_icon_change)


    def connect_connect_icon_change(self,ping_signal: bool):
        """槽函数：切换两个连接按钮
        """
        self.connected_btn.setHidden(not ping_signal)
        self.disconnect_btn.setHidden(ping_signal)
        

    @logger.catch()
    def connect_connect_info(self,*args):
        """连接界面展示，每次点击读取一次配置文件
        """
        self.connect_info_widget.show()
        self.connect_info_widget.comboBox_init(1)
        