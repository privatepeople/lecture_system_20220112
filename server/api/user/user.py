# 로그인 / 회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결정보 보관 변수를 import
from server.db_connector import DBConnector
from server.model import Users

db = DBConnector()

def login(params):
    sql = f"SELECT * FROM users WHERE email = '{params['email']}' AND password = '{params['pw']}'"
    
    login_user = db.executeOne(sql) # 있다면 인스턴스, 없다면 None
    
    if login_user == None:
        return {
            'code': 400,
            'message': '이메일 또는 비밀번호가 잘못되었습니다.'
        }, 400
    
    
    return {
        'code': 200,
        'message': '로그인 성공',
        'data': {
            'users': Users(login_user).get_data_object()
        }
    }