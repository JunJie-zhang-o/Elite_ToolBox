from os import truncate
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QQuaternion
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QScrollArea, QPushButton, QVBoxLayout, QWidget
import sys

from loguru import logger
from inc.Class_xml import Comment_xml_parse
from inc.xml_widget.Qthread_xml import Up_load,Download,LoadExcel,CreatExcel
import inc.global_value as glo




class CommentWidget(QWidget):
    """注释修改页面
    """
    
    def __init__(self):
        super().__init__()
        
        self.layout_init()          #创建布局
        self.var_init()             #创建需要的变量
        self.layout_setting()       # 布局调整
        
        self.connect_init()
        glo._init_window_var()
        glo.set_main_widget(self)
        self.resize(1111, 690)
#------------------------------------UI处理--------------------------------------#

    def layout_init(self):
         # 创建主要布局为垂直布局
        self.Main_layout = QVBoxLayout()
        # 创建顶层水平布局, 下方的水平布局
        self.top_layout = QHBoxLayout()
        self.top_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.down_layout = QHBoxLayout()
        self.down_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        # 创建5个滚动条区域
        self.list_scroll = [QScrollArea() for i in range(5)]
        # 创建5个空间容器
        self.list_scroll_widget = [QWidget() for i in range(5)]
        # 创建5个表单布局
        self.list_formlayout = [QFormLayout(self.list_scroll_widget[i]) for i in range(5) ]
        # 创建变量名列表
        
        
    def layout_setting(self):
        """布局调整
        """
        for i in range(5):
            # 取消横向的滚动条
            self.list_scroll[i].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # 设置滚动条区域的布局
            self.list_scroll[i].setWidget(self.list_scroll_widget[i])
            # 下方水平布局添加滚动条容器
            self.down_layout.addWidget(self.list_scroll[i])
                    
        self.top_layout_setting()
        # 设置主布局
        self.Main_layout.addLayout(self.top_layout)
        self.Main_layout.addLayout(self.down_layout)
        self.Main_layout.setStretch(0,1)
        self.Main_layout.setStretch(1,1)
        # 将主布局应用到界面
        self.setLayout(self.Main_layout)
    
    
    def top_layout_setting(self):
        """顶部水平布局
        """
        self.pgrBar = QProgressBar()

        self.upload_btn = QPushButton("上载",toolTip="从机器人上载数据")
        self.download_btn = QPushButton("保存",toolTip="将注释保存至机器人")
        self.load_btn = QPushButton("加载Excel",toolTip="从指定格式的Excel文件中读取数据")
        self.creat_btn = QPushButton("生成Excel",toolTip="生成指定格式的Excel文件")
        self.clear_btn = QPushButton("清空",toolTip="清空所有输入框内容")
        self.comobo_box = QComboBox()
        self.comobo_box.addItems(["中文","英文","日文","韩文","其他"])
        
        self.upload_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        
        self.Vline_1 = self.spilt_line_V()
        self.Vline_2 = self.spilt_line_V()
        self.Vline_3 = self.spilt_line_V()        
        self.Vline_4 = self.spilt_line_V()

        self.top_layout.addWidget(QLabel("进度:"))
        self.top_layout.addWidget(self.pgrBar)
        self.top_layout.addStretch(0.05)
        self.top_layout.addWidget(self.Vline_1)
        self.top_layout.addWidget(self.clear_btn)
        self.top_layout.addWidget(self.Vline_2)
        self.top_layout.addWidget(self.upload_btn)
        self.top_layout.addWidget(self.download_btn)
        self.top_layout.addWidget(self.Vline_3)

        self.top_layout.addWidget(self.comobo_box)       
        self.top_layout.addWidget(self.load_btn) 
        self.top_layout.addWidget(self.Vline_4)
        self.top_layout.addWidget(self.creat_btn) 

        
#------------------------------------业务处理--------------------------------------#

    def var_init(self):
        self.xml_obj = Comment_xml_parse()                      
        self.str_b = [ "B"+str(li) for li in range(256)]
        self.str_i = [ "I"+str(li) for li in range(256)]
        self.str_d = [ "D"+str(li) for li in range(256)]
        self.str_p = [ "P"+str(li) for li in range(256)]
        self.str_v = [ "V"+str(li) for li in range(256)]
        self.list_str = [self.str_b, self.str_i, self.str_d, self.str_p, self.str_v]
        self.dict_line_edit={}
        # 向表单布局中添加label和输入框
        for i in range(len(self.list_formlayout)):
            for j in range(256):      
                self.dict_line_edit[self.list_str[i][j]]=QLineEdit("",objectName=self.list_str[i][j])
                self.list_formlayout[i].addRow(QLabel(self.list_str[i][j]), self.dict_line_edit[self.list_str[i][j]])
                self.dict_line_edit[self.list_str[i][j]].textChanged.connect(self.slot_text_2_dict)
        self.dict_line_edit_key ={i:None for i in self.dict_line_edit.keys()}


    def connect_init(self):
        """绑定信号与槽
        """
        self.clear_btn.clicked.connect(self.slot_btn_clear)
        self.upload_btn.clicked.connect(self.slot_btn_upload)
        self.download_btn.clicked.connect(self.slot_btn_save)
        self.load_btn.clicked.connect(self.slot_btn_load)
        self.language = 0
        self.comobo_box.currentIndexChanged.connect(self.slog_combox)
        self.creat_btn.clicked.connect(self.slot_btn_create)
        pass
    
    def slot_btn_clear(self):
        """清空按钮
        """
        logger.info("CommentWidget clear btn clicked")
        for i in self.dict_line_edit.values():
            i.clear()
        pass
        

    def slot_btn_upload(self,):
        """槽函数：上载按钮触发
        """
        logger.info("CommentWidget upload btn clicked")
        self.xml_obj = Comment_xml_parse()
        self.up_load = Up_load(self.xml_obj)
        self.up_load.pgbar_percent.connect(self.slot_pgbar)
        self.up_load.comment_var.connect(self.slot_comment_show)
        self.up_load.exception_sign.connect(self.slot_exception)
        self.up_load.start()
        
    
    
    def slot_pgbar(self,var:int):
        """进度条显示

        Args:
            var (int): 百分比
        """
        self.pgrBar.setValue(var)
        if self.pgrBar.value() == 99:
            pass
            # self.pgrBar.setValue(0)
            
            
    def slot_comment_show(self,comment: list):
        """将注释解析至界面

        Args:
            comment (list): 注释信息，0为key，1为value
        """
        line_edit_obj =self.findChild(QLineEdit,comment[0])
        line_edit_obj.setText(comment[1])
        # print(FindLE)
        
        
    def all_btn_enable(self,state):
        """控制按钮是否启用
        """
        self.sign_loading_state = state
        if state == True:
            self.load_btn.setEnabled(False)
            self.creat_btn.setEnabled(False)
            self.clear_btn.setEnabled(False)
            self.download_btn.setEnabled(False)
            self.upload_btn.setEnabled(False)
        elif state == False:
            self.load_btn.setEnabled(True)
            self.creat_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
            del self.sign_loading_state
        
        
    def slot_exception(self,exception_sign):
        """异常信号
        """
        self.except_signal=exception_sign
        if exception_sign[:10] == "btn handle":
            if exception_sign == "btn handle start":
                btn_enable = False
            elif exception_sign == "btn handle end":
                btn_enable = True
            self.upload_btn.setEnabled(btn_enable)
            self.download_btn.setEnabled(btn_enable)
            self.load_btn.setEnabled(btn_enable)
            self.creat_btn.setEnabled(btn_enable)
            self.clear_btn.setEnabled(btn_enable)
        else:    
            if exception_sign == "ssh connect error" :
                title = "连接失败"
                text = "请检查网络连接是否通畅,\n请检查用户名和密码是否正确"

            elif exception_sign == "No such file" :
                title = "文件解析失败"
                text = "请在示教器上修改任意一个B、I、D、P、V变量注释，\n并在修改后重新点击上载按钮"
                
            QMessageBox.warning(self,title,text)

        
    @logger.catch()
    def btn_clicked(self,*args):
        """测试代码，如何知道是哪个控件发送信号过来
        """
        sender = self.sender()
        print(sender.text())
        print(sender.objectName())
        var_sign = ["B","I","D","P","V"]
        # head_sender = sender.objectName()[0]
        # foot_sender = int(sender.objectName()[1:])
        # print(self.dict_line_edit)
        # FindLE=self.findChild(QLineEdit,'B5')
        # print(FindLE)
        
        
    def slot_text_2_dict(self):
        """对每个输入框进行处理，使用objectName与dict的key值进行对比，
        将值写入dict中
        """
        sender = self.sender()
        # print(sender)
        name = sender.objectName()
        text = sender.text()
        self.dict_line_edit_key[name] = text
        
    
    @logger.catch
    def slot_btn_save(self,*args):
        """保存按钮的槽函数
        """
        logger.info("CommentWidget save btn clicked")
        dict_line_edit_text = list(self.dict_line_edit_key.values())
        list_line_edit_text = [dict_line_edit_text[0:256],dict_line_edit_text[256:512],
                               dict_line_edit_text[512:768],dict_line_edit_text[768:1024],
                               dict_line_edit_text[1024:1279]]
        self.download = Download(list_line_edit_text,self.xml_obj)
        self.download.pgbar_var.connect(self.slot_pgbar)
        self.download.exception_sign.connect(self.slot_exception)
        self.download.start()
        
        
    def slog_combox(self):
        """下拉框按钮
        """
        logger.info("CommentWidget combox index changed")
        self.language = self.comobo_box.currentIndex() 
        print(self.language)
        
    
    def slot_btn_load(self):
        """加载按钮槽函数
        """
        logger.info("CommentWidget load btn clicked")
        file_path,l = QFileDialog.getOpenFileName(self,"加载Excel","C://","*.xls")
        if file_path != None and file_path != "":
            self.load_excel = LoadExcel(file_path,self.language)
            self.load_excel.sign_comment_var.connect(self.slot_comment_show)
            self.load_excel.sign_pgbar_percent.connect(self.slot_pgbar)
            self.load_excel.sign_load_error.connect(self.slot_exception_btn_load)
            self.load_excel.sign_loading.connect(self.all_btn_enable)
            self.load_excel.start()
            pass
        
        
    def slot_exception_btn_load(self,except_sign):
        msg = ("表格中有sheetname匹配失败\n请使用生成功能生成标准格式表格",
               "表格第一行有标题匹配失败\n请使用生成功能生成标准格式表格",
               "表格中有序号匹配失败\n请使用生成功能生成标准格式表格")

        QMessageBox.warning(self,"表格解析失败",msg[except_sign-1])

    @logger.catch()
    def slot_btn_create(self,*args):
        """生成Excel槽函数
        """
        logger.info("CommentWidget create btn clicked")
        file_path,l = QFileDialog.getSaveFileName(self,"生成Excel","C://","*.xls")
        if file_path !="" :
            dict_line_edit_text = list(self.dict_line_edit_key.values())
            list_line_edit_text = [dict_line_edit_text[0:256],dict_line_edit_text[256:512],
                                dict_line_edit_text[512:768],dict_line_edit_text[768:1024],
                                dict_line_edit_text[1024:1279]]
            self.Creat_excel = CreatExcel(file_path,list_line_edit_text,self.language)
            self.Creat_excel.sign_creating.connect(self.all_btn_enable)
            self.Creat_excel.sign_create_except.connect(self.slot_exception_btn_create)
            self.Creat_excel.start()
        

    def slot_exception_btn_create(self,except_sign):
        msg = ("该文件已经被打开或被其他程序占用\n请更改文件路径或文件名后重新生成",
        )
        QMessageBox.warning(self,"表格生成失败",msg[except_sign-1])


    def spilt_line_V(self):
        """返回一个竖直分割线对象
        """
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        return line
    
    
    def qss_style(self, file_name):
        with open(file_name, "r") as f:
            return f.read()
        
        
        
def main():
    app = QApplication(sys.argv)
    main = CommentWidget()
    main.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":

    main()