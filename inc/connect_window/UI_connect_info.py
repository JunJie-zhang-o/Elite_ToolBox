from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from loguru import logger
from inc.ui2py.connect_info import Ui_connect_param
import re
from inc.Class_json import login_info
from inc.connect_window.Qthread_ping import NetWorkPing
import inc.global_value as glo_value


class connect_info(Ui_connect_param,QDialog):
    
    def __init__(self) -> None:
        super().__init__() 
        QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.ping = NetWorkPing()   #先创建Qthread对象
        self.btn_enable_change(False)
        self.btn_connect.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_delate.setEnabled(False)
        self.comboBox_init()
        self.connect_init()
        self.pass_init()
        
        
        
    def pass_init(self):
        """#todo暂时隐藏不需要的控件，后续做功能不全
        """
        self.label_name_result1.setHidden(True)
        self.label_name_result2.setHidden(True)
        self.label_pass_result1.setHidden(True)
        self.label_pass_result2.setHidden(True)

        
    def connect_init(self):
        """槽函数连接初始化
           #!槽函数用lamda表达式表达，可以进行额外的传参
        """
        self.btn_defalt.clicked.connect(self.connect_btn_defalt)    
        self.lineEdit.textChanged.connect(lambda: self.connect_ip_input("0"))
        self.lineEdit_7.textChanged.connect(lambda: self.connect_ip_input("1"))
        self.btn_cancel.clicked.connect(self.connect_cancel_clear)
        self.comboBox_history1.currentIndexChanged.connect(lambda: self.connect_comboBox_history("0"))
        self.comboBox_histroy2.currentIndexChanged.connect(lambda: self.connect_comboBox_history("1"))
        self.btn_connect.clicked.connect(self.connect_btn_connect)
        self.btn_disconnect.clicked.connect(self.connect_dis_connect)
        self.lineEdit.textChanged.connect(self.connect_connect_state)
        self.lineEdit_2.textChanged.connect(self.connect_connect_state)
        self.lineEdit_3.textChanged.connect(self.connect_connect_state)
        # 历史记录修改页面
        self.lineEdit_7.textChanged.connect(self.connect_btn_history_state)
        self.lineEdit_8.textChanged.connect(self.connect_btn_history_state)
        self.lineEdit_9.textChanged.connect(self.connect_btn_history_state)
        self.comboBox_histroy2.currentIndexChanged.connect(self.connect_btn_history_state)
        
        self.btn_save.clicked.connect(self.slot_btn_save_setting)
        self.btn_delate.clicked.connect(self.slot_btn_delete_setting)
    
    
    def btn_enable_change(self,state:bool):
        """该方法用于根据连接状态修改控件状态

        Args:
            state (bool): 连接状态
        """
        # 以下状态全为未连接时的状态
        self.btn_disconnect.setEnabled(state)
        self.btn_connect.setEnabled(not state)
        self.lineEdit.setEnabled(not state)
        self.lineEdit_2.setEnabled(not  state)
        self.lineEdit_3.setEnabled(not state)
        self.btn_defalt.setEnabled(not state)
        self.comboBox_history1.setEnabled(not state)
        self.btn_cancel.setEnabled(not state)
        if state :
            self.label_connect_state.setText("已连接")
        else:
            self.label_connect_state.setText("未连接")
        # pass
        
        
    def connect_btn_defalt(self):
        """默认按钮的绑定
        """
        self.lineEdit.setText("192.168.1.200")
        self.lineEdit_2.setText("root")
        self.lineEdit_3.setText("elite2014")


    @pyqtSlot()
    @logger.catch()
    def connect_ip_input(self,strr: str):
        """正则ip输入的结果
        """
        if strr == "0":
            line_edit=self.lineEdit
            label_result=self.label_ip_result1
        elif strr == "1":
            line_edit=self.lineEdit_7
            label_result=self.label_ip_result2
        if line_edit.text() != "" :
            result = self.is_ipv4(line_edit.text())
            if result:
                label_result.setText("格式正确")
            else:
                label_result.setText("格式错误")
        else:
            label_result.setText("请输入")
        
        
    def is_ipv4(self,ip: str) -> bool:
        """
        检查ip是否合法
        :param: ip ip地址
        :return: True 合法 False 不合法
        """
        return True  if [1] * 4 == [x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")] else False
    
    
    def connect_cancel_clear(self):
        """清空输入框的内容
        """
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        
        
    def comboBox_init(self,mode=0):
        """从json文件中加载对应的参数
        """
        self.login_obj = login_info("./config/login_info.json")
        self.login_data = self.login_obj.read_from_json()
        
        if mode == 0:
            self.comboBox_history1.addItem("请选择")
            self.comboBox_histroy2.addItem("请选择")
        
            if  self.login_data != None :
                for i in range(len(self.login_obj.ip)):
                    self.comboBox_history1.addItem(self.login_obj.ip[i])
                    self.comboBox_histroy2.addItem(self.login_obj.ip[i])
        elif mode == 1:
            if  self.login_data != None :
                for i in range(len(self.login_obj.ip)):
                    if self.comboBox_history1.findText(self.login_obj.ip[i]) == -1:
                        self.comboBox_history1.addItem(self.login_obj.ip[i])
                        self.comboBox_histroy2.addItem(self.login_obj.ip[i])
            
        
                
    # @pyqtSlot()
    @logger.catch()
    def connect_comboBox_history(self,strr:str):
        """下拉框选项
        """
        if strr == "0":
            combobox = self.comboBox_history1
            line_ip=self.lineEdit
            line_user=self.lineEdit_2
            line_pass=self.lineEdit_3
        elif strr == "1":
            combobox = self.comboBox_histroy2
            line_ip=self.lineEdit_7
            line_user=self.lineEdit_8
            line_pass=self.lineEdit_9
        if combobox.currentIndex() > 0:
            line_ip.setText(self.login_obj.ip[combobox.currentIndex()-1])
            line_user.setText(self.login_obj.username[combobox.currentIndex()-1])
            line_pass.setText(self.login_obj.password[combobox.currentIndex()-1])
        elif combobox.currentIndex() == 0 :
            line_ip.setText("")
            line_user.setText("")
            line_pass.setText("")
            
            
    def connect_btn_connect(self):
        """连接按钮
        """
        glo_value._init()
        glo_value.set_value("ip",self.lineEdit.text())
        glo_value.set_value("username",self.lineEdit_2.text())
        glo_value.set_value("password",self.lineEdit_3.text())
        
        self.ping.ping_signal.connect(self.connect_sign_ping)
        self.ping.start()
        
        
    def connect_sign_ping(self,ping_signal: bool):
        """连接状态信号实时处理

        Args:
            ping_signal (bool): ping ip的信号
        """
        if ping_signal:
            self.btn_enable_change(ping_signal)
            curr_ip_input = self.lineEdit.text()
            curr_username_input = self.lineEdit_2.text()
            curr_pass_input = self.lineEdit_3.text()
            
            if self.login_obj.ip.count(curr_ip_input) == 0:
                self.login_obj.ip.append(curr_ip_input)
                self.login_obj.username.append(curr_username_input)
                self.login_obj.password.append(curr_pass_input)
                self.login_obj.write_json()
        else:
            self.btn_enable_change(True)
            self.btn_connect.setText("连接中")            
            self.label_connect_state.setText("连接中")            

        
    def connect_dis_connect(self):
        """断开连接按钮
        """
        self.ping.stop()
        self.btn_enable_change(False)
        self.label_connect_state.setText("未连接")  
        self.btn_connect.setText("连接")       
        
        
    def connect_connect_state(self):
        """根据输入信息的内容判断连接按钮是否启用
        """
        ip_input = self.label_ip_result1.text()
        username_input = self.lineEdit_2.text().__len__()
        pass_input = self.lineEdit_3.text().__len__()
        
        if ip_input=="格式正确" and username_input>0 and pass_input> 0:
            self.btn_connect.setEnabled(True)
        else:
            self.btn_connect.setEnabled(False)
            
            
    def connect_btn_history_state(self):
        """历史记录修改页面保存和删除按钮的启用和关闭
        """
        index_comboBox = self.comboBox_histroy2.currentIndex()
        ip_input = self.label_ip_result2.text()
        username_input = self.lineEdit_8.text().__len__()
        pass_input = self.lineEdit_9.text().__len__()
        
        if index_comboBox > 0 and ip_input=="格式正确" and username_input>0 and pass_input> 0:
            self.btn_save.setEnabled(True)
            self.btn_delate.setEnabled(True)
        elif index_comboBox > 0:
            self.btn_delate.setEnabled(True)
        else:
            self.btn_save.setEnabled(False)
            self.btn_delate.setEnabled(False)
     
            
    @logger.catch()
    def slot_btn_save_setting(self,*args):
        """修改保存配置
        """
        index_comboBox = self.comboBox_histroy2.currentIndex()
        ip_input = self.lineEdit_7.text()
        username_input = self.lineEdit_8.text()
        pass_input = self.lineEdit_9.text()
        
        self.login_obj.ip[index_comboBox-1] = ip_input
        self.login_obj.username[index_comboBox-1] = username_input
        self.login_obj.password[index_comboBox-1] = pass_input
        # 配置写入
        self.login_obj.write_json()
        QMessageBox.about(self,"参数修改","    修改成功        ")
        
        
    @logger.catch()
    def slot_btn_delete_setting(self,*args):
        """删除配置
        """
        index_comboBox = self.comboBox_histroy2.currentIndex()
        self.login_obj.ip.pop(index_comboBox-1)
        self.login_obj.username.pop(index_comboBox-1)
        self.login_obj.password.pop(index_comboBox-1)
        # 配置写入
        self.login_obj.write_json()
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.comboBox_histroy2.removeItem(index_comboBox)
        self.comboBox_history1.removeItem(index_comboBox)
        self.comboBox_histroy2.setCurrentIndex(0)
        QMessageBox.about(self,"参数删除","    删除成功        ")
        
        
