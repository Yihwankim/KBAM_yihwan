def outputmsg(msg_code):
    msgcode_dic = {0: ('OP_ERR_NONE', '정상처리'),
                   -100: ('OP_ERR_LOGIN', '사용자정보교환실패'),
                   -101: ('OP_ERR_CONNECT', '서버접속실패'),
                   -1-2: ('OP_ERR_VERSION', '버전처리실패')}

    printECode = msgcode_dic[msg_code]
    return printECode
