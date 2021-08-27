
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QWidget
from inc.ui2py.log_8058 import Ui_log_8058
from inc.log_8058.Qthread_log_8058 import Get_Log,Save_Log
from loguru import logger




class Log_8058(Ui_log_8058,QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect_init()
        
        
    def connect_init(self):
        self.btn_getlog.clicked.connect(self.slot_get_log)
        self.btn_savelog.clicked.connect(self.slot_save_log)
        
        self.btn_getlog.setEnabled(False)
        self.btn_savelog.setEnabled(False)
        
        
    def slot_get_log(self):
        logger.info("btn_getlog clicked")
        self.textEdit_log.clear()
        self.thread_get = Get_Log()
        self.thread_get.text_log.connect(self.slot_text)
        self.thread_get.state.connect(self.slot_enable)
        self.thread_get.sign_except.connect(self.except_msgbox)
        self.thread_get.start()
        pass
    
    
    def slot_save_log(self):
        logger.info("btn_savelog clicked")
        text = self.textEdit_log.toPlainText()
        file_path,l  =  QFileDialog.getSaveFileName(self,"日志保存",'./', "*.txt")
        if file_path != "":
            self.thread_save = Save_Log(file_path,text)
            self.thread_save.state.connect(self.slot_enable)
            self.thread_save.start()
        pass
    
    
    def slot_text(self,text):
        # self.textEdit_log.setText(text)
        # 追加显示
        self.textEdit_log.moveCursor(QTextCursor.End)
        # self.textEdit_log.append(text)        #追加显示带换行
        self.textEdit_log.insertPlainText(text)     #追加显示不换行
        
    
    def slot_enable(self,state):
        self.btn_getlog.setEnabled(state)
        self.btn_savelog.setEnabled(state)
        
        
    def except_msgbox(self,except_sign):

        if except_sign == "ConnectionRefusedError":
            msg = "请检查网络连接及远程8058端口是否正常打开"
        if except_sign == "8058 recv timeout" or except_sign == "ConnectionResetError":
            msg = "请检查网络连接是否中断"
        QMessageBox.warning(self,"获取失败",msg)
        

        