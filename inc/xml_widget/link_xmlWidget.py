from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from loguru import logger
from inc.Func.excel import Excel_read_write
from inc.Func.xml import Comment_xml_parse
from PyQt5.QtCore import QObject, pyqtRemoveInputHook
from inc.UI.UI_XmlWidget import CommentWidget


class XmlWidgetLink(CommentWidget,Excel_read_write,Comment_xml_parse):
    
    def __init__(self):
        super().__init__()
        Comment_xml_parse.__init__(self)
        self.link()

    
    def link(self):
        for key,values in self.dict_line_edit.items():
            values.textChanged.connect(self.line_textChanged)
        self.upload_btn.clicked.connect(self.upload_clicked)

    
    def upload_clicked(self):
        filePath, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./","*.xml")
        if filePath != None:
            self.read_xml(filePath)
            self.lists_2_lineedit(self.comment_lists)
        pass

    def save_clicked(self):
        pass

    def load_clicked(self):
        pass
    
    def create_clicked(self):
        pass

    @logger.catch
    def line_textChanged(self):
        sender = self.sender()
        # print(sender.text())
        print(sender.objectName())
        obj_name = str(sender.objectName())
        if obj_name[:1] == "B":
            num=0
        elif obj_name[:1] == "I":
            num=1
        elif obj_name[:1] == "D":
            num=2
        elif obj_name[:1] == "D":
            num=3
        elif obj_name[:1] == "P":
            num=4
        self.comment_lists[num][int(obj_name[1:])]=sender.text()
        # print(self.comment_lists)
        
    @logger.catch
    def lists_2_lineedit(self,lists: list):
        print(self.dict_line_edit)
        i=0
        j=0
        for key,values in self.dict_line_edit.items():
            print(key,i,j-i*256)
            values.setText(lists[i][j-i*256])
            j=j+1
            i=j//256