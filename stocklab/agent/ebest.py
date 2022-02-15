import configparser
import win32com.client
import pythoncom

class XASession:
    #로그인 상태를 확인하기 위한 클래스 변수
    login_state = 0
    
    def OnLogin(self, code, msg):
        """로그인 시도 후 호출되는 이벤트.
        code가 0000이면 로그인 성공
        """
        
        if code == "0000":
            print(code,msg)
            XASession.login_state = 1
            
        else:
            print(code, msg)
            
    def OnDisconnect(self):
        """서버와 연결이 끊어지면 발생하는 이벤트.
        """
        print ("Session disconnected.")
        XASession.login_state = 0   
        
class EBest:
    
    def __init__(self, mode=None):
        """config.ini  파일을 로드해 사용자, 서버 정보 저장
        Query_cnt는 10분당 200개의 TR 수행을 관리하기 위한 리스트 
        xa_session_client는 XASession 객체
        :param mode:str - 모의서버는 DEMO 실서버는 PROD로 구분
        """      
        if mode not in ["PROD", "DEMO"]:
            raise Exception("Need to run mode(PROD or DEMO)")
        
        run_mode = "EBEST_"+mode #EBEST_PROD or DEMO 로 결합한다. 
        config = configparser.ConfigParser() ##config parser로 config.ini 파일을 불러온다 
        config.read('conf/config.ini')
        self.user = config[run_mode]['user']
        self.passwd= config[run_mode]['password']
        self.cert_passwd[run_mode]['cert_passwd']
        self.host =[run_mode]['host']
        self.port = [run_mode]['port']
        self.account = config[run_mode]['account']
        
        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession",XASession)
    
    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()
            
     
    def logout(self):
        #result = self.xa_session_client.Logout()
        #if result:
        XASession.login_state = 0
        self.xa_session_client.DisconnectServer()        
        
        
        