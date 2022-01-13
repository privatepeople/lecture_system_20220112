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
    
def sign_up(params):
    
    # 이메일이 중복이면 가입 불허 예정
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"
    
    already_user_data = db.executeOne(sql)
    
    # 이미 가입한 사람이 있다? 400 중복.
    if already_user_data:
        return {
            'code': 400,
            'message': '이미 사용중인 이메일 입니다.'
        }, 400
    
    sql = f"INSERT INTO users (email, password, name) VALUES ('{params['email']}', '{params['pw']}', '{params['name']}')"
    
    db.insertAndCommit(sql)
    
    return {
        'code': 200,
        'message': '회원가입 성공'
    }

# 이메일 받아서 사용자 정보 조회
def find_user_by_email(params):
    
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"
    find_user_data = db.executeOne(sql)
    if find_user_data:
        find_user = Users(find_user_data)
        return {
            'code': 200,
            'message': '사용자를 찾았습니다.',
            'data': {
                'user': find_user.get_data_object()
            }
        }
        # 해당 이메일의 사용자가 발견된 경우
    else:
        # 검색이 되지 않은 경우
        return {
            'code': 400,
            'message': '해당 이메일의 사용자는 없습니다.'
        }, 400