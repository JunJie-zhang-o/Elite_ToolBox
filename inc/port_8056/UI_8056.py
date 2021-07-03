from PyQt5.QtWidgets import QWidget
from inc.ui2py.port_8056 import Ui_Widget_8056


class UI_8056(Ui_Widget_8056,QWidget):

    
    def __init__(self) -> None:
        super().__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)