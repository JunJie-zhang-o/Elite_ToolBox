from loguru import logger
from merry import Merry
from paramiko import ssh_exception
from PyQt5.QtWidgets import QMessageBox

class BasicException():
    merry = Merry()
    merry.logger.disabled = True
    
    def __init__(self,widget) -> None:
        self.widget=widget
        pass
    
    @classmethod
    @merry.except_(ssh_exception.SSHException)
    def except_SSHException(self,e):
        logger.error(e)
        QMessageBox.warning(self.widget,"demo_title","demo_main")
    pass
