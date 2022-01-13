from server.model import Lectures
from server import db

def get_all_lectures(params):
    # 모든 강의 목록을 이름순으로 내려주자. => 당장은 params 활용 X
    
    sql = f"SELECT * FROM lectures ORDER BY name"
    
    db_list = db.executeAll(sql)
    
    lectures = [Lectures(row).get_data_object() for row in db_list]
    
    return {
        'code': 200,
        'message': '모든 강의목록 조회',
        'data': {
            'lectures': lectures
        }
    }

# 수강신청 기능
def apply_lecture(params):
    
    # 같은 과목에 같은사람이 신청은 불가.
    sql = f"SELECT * FROM lecture_user WHERE lecture_id = {params['lecture_id']} and user_id = {params['user_id']}"
    
    already_apply = db.executeOne(sql)
    
    if already_apply:
        return {
            'code': 400,
            'message': '이미 수강신청이 완료되었습니다.'
        }, 400
    
    # lecture_user 테이블에 한줄 추가. (INSERT INTO)
    
    sql = f"INSERT INTO lecture_user VALUES({params['lecture_id']}, {params['user_id']})"
    
    db.insertAndCommit(sql)
    
    return {
        'code': 200,
        'message': '수강신청을 성공했습니다.'
    }