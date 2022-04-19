import sys
from kiwoom.auto.Kiwoom import *
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print('메인클래스 입니다')

        self.app = QApplication(sys.argv)
        self.app = Kiwoom()
        self.app.exec_() # 이벤트 루프 실행.

if __name__== "__main__":
    Main()



########################################################################################################################
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
