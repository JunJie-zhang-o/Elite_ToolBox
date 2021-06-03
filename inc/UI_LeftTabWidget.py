from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,QScrollArea,QPushButton, QStackedWidget,QVBoxLayout,QWidget

import sys




class LeftTabWidget(QListWidget):
    
    def __init__(self,item_lists):
        super().__init__()
        # self.resize(,)
        self.list_str=item_lists
        
        self.__UI_init__()
        self.setStyleSheet(self.qss_style("src\QSS_LeftTabWidget.qss"))
        
        
    def __UI_init__(self):
        # self.currentRowChanged.connect(self.right_widget.setCurrentIndex)   #；list和右侧窗口的index对应
        self.setFrameShape(QListWidget.NoFrame) #去掉边框
        # self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  #去掉滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        for i in range(len(self.list_str)):
            self.item=QListWidgetItem(self.list_str[i],self)
            self.item.setSizeHint(QSize(30,60)) #设置尺寸
            self.item.setTextAlignment(Qt.AlignCenter)  #居中显示
                                
        
    def qss_style(self,file_name):
        with open(file_name,"r") as f:
            return f.read()
        
def main():
    app = QApplication(sys.argv)
    
    main = LeftTabWidget()
    main.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":

    main()