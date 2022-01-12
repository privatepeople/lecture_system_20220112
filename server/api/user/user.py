# 로그인 / 회원가입 등, 사용자 정보 관련 기능 모아두는 모듈
# DB 연결정보 보관 변수를 import
from server.db_connector import DBConnector
from server.model import Users

db = DBConnector()

def test():
    
    # DB의 모든 users 조회 쿼리
    sql = "SELECT * FROM users"
    db.cursor.execute(sql)
    all_list = db.cursor.fetchall()
    
    
    # 목록 for -> 한 줄 row로 추출 -> 추출된 row로 모델클래스로 가공 / dict로 재가공 한줄로 마무리
    
    # python for문을 list를 돌때 => comprehension
    all_users = [Users(row).get_data_object() for row in all_list]
    
    
    return {
        'users': 'all_users'
    }