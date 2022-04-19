from PyQt5.QAxContainer import *
from kiwoom.auto.omsg import outputmsg

class Kiwoom():
    def __init__(self):
        super().__init__()
        print('키움클래스 입니다')

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.CommConnect()
        self.set_signal_slot()

    def handler_msg(self, err_code):
        if err_code == 0:
            print("로그인 성공", outputmsg(err_code)[1])

        else:
            print("로그인 실패", outputmsg(err_code)[1])

    # signal
    def set_signal_slot(self):
        self.ocx.OnEventConnect.connect(self.handler_msg)

    # method
    def CommConnect(self, block=True):
        self.ocx.dynamicCall("CommConnect()")