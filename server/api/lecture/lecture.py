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