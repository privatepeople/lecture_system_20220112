from server import db

# 강의의 리뷰에 대한 기능만 모아두는 별도의 파이썬 파일

def write_review(params):
    
    # 파라미터가 제대로 들어오는가? 검증
    # 1. 평점은 1~5 사이로만 가능.
    
    score = float(params['score']) # 파라미터들은 기본적으로 str 형태로 들어옴. -> flaot로 변환해두고 사용.
    
    if not (1 <= score and score <= 5):
        return {
            'code': 400,
            'message': '평점은 1~5 사이여야 합니다.'
        }, 400
    
    # 2. 제목의 길이는 최소 5자 이상. -> str의 길이. 파라미터 자체의 길이 체크.
    if len(params['title']) < 5:
        return {
            'code': 400,
            'message': '제목은 최소 5자 이상이어야 합니다.'
        }, 400
    
    # 3. 내용의 길이는 최소 10자 이상.
    if len(params['content']) < 10:
        return {
            'code': 400,
            'message': '내용은 최소 10자 이상이어야 합니다.'
        }, 400
    
    # DB내부 조회 결과 활용
    # 4. 수강을 했어야만 리뷰 작성 가능.
    
    sql = f"SELECT * FROM lecture_user WHERE lecture_id = {params['lecture_id']} AND user_id = {params['user_id']}"
    
    query_result = db.executeOne(sql)
    
    if not query_result:
        # 수강 안한 사람이 리뷰 등록
        return {
            'code': 400,
            'message': '수강을 한 인원만 리뷰 작성이 가능합니다.'
        }, 400
    
    # 5. 이미 리뷰를 등록했다면, 추가 등록 불가.\
    
    sql = f"SELECT * FROM lecture_review WHERE lecture_id = {params['lecture_id']} AND user_id = {params['user_id']}"
    
    already_review_data = db.executeOne(sql)
    
    if already_review_data:
        return {
            'code': 400,
            'message': '이미 리뷰를 등록한 강의입니다.'
        }, 400
    
    # 리뷰 실제 등록
    
    sql = f"""
    INSERT INTO lecture_review
    (lecture_id, user_id, title, content, score)
    VALUES
    ({params['lecture_id']}, {params['user_id']}, '{params['title']}', '{params['content']}', {score})
    """
    
    db.insertAndCommit(sql)
    
    return {
        'code': 200,
        'message': '리뷰 등록에 성공했습니다.'
    }