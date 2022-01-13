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

# 특정항목을 지정해서, 해당 항목만 수정
def modify_reviews(params):
    
    # 파라미터 정리
    # field : 어느 항목을 바꿀지 알려주는 역할
    # value : 해당 항목에 실제로 넣어줄 값
    # user_id : 이 변경을 시도하는 사람이 누구인지? 고유번호
    # review_id : 변경해줄 리뷰의 id
    
    # field라는 이름표로, 어느 항목을 바꾸고 싶은지? 받아오자.
    column_name = params['field']
    
    # 파라미터 검증
    # 검증0. 받아온 리뷰아이디에 해당하는 리뷰가 실존하는가?
    # 검증1. 수정하려는 리뷰가 본인이 작성한 리뷰가 맞는지?
    
    sql = f"SELECT * FROM lecture_review WHERE id = {params['review_id']}"
    
    review_data = db.executeOne(sql)
    
    if review_data == None:
        return {
            'code': 400,
            'message': '해당 리뷰는 존재하지 않습니다.'
        }, 400
        
    # DB에서 가져온 user_id : int로 받아옴
    # 파라미터에서 가져온 user_id : 파라미터는 일단 모든 데이터를 str로 받아옴. : str로 받아옴
    # 둘다 int로 바꿔놓고 비교
    if int(review_data['user_id']) != int(params['user_id']):
        return {
            'code': 400,
            'message': '본인이 작성한 리뷰만 수정할 수 있습니다.'
        }, 400
    
    # 검증2. 점수 수정인 경우 -> 입력값 1 ~ 5 사이인지?
    
    # 제목 변경?
    
    if column_name == 'title':
        sql = f"UPDATE lecture_review SET title = '{params['value']}' WHERE id = {params['review_id']}"
        
        # DB에 변경 발생 -> 쿼리실행 / commit
        db.cursor.execute(sql)
        db.db.commit()
        
        # 제목 변경 성공 리턴.
        return {
            'code': 200,
            'message': '제목을 수정했습니다.'
        }
    
    # 내용 변경
    
    if column_name == 'content':
        sql = f"UPDATE lecture_review SET content = '{params['value']}' WHERE id = {params['review_id']}"
        
        db.cursor.execute(sql)
        db.db.commit()
        
        return {
            'code': 200,
            'message': '내용을 수정했습니다.'
        }
    
    # 점수 변경
    
    if column_name == 'score':
        
        # 파라미터로 들어온 점수가 1 ~ 5인지?
        
        score = float(params['value'])
        
        if not (1 <= score and score <= 5):
            return {
                'code': 400,
                'message': '변경할 점수는 1~5 사이값이어야 합니다.'
            }, 400
        
        sql = f"UPDATE lecture_review SET score = score WHERE id = {params['review_id']}"
        
        db.cursor.execute(sql)
        db.db.commit()
        
        return {
            'code': 200,
            'message': '점수를 수정했습니다.'
        }
        
    # 여기까지 내려왔다? field 파라미터에 잘못된값이 들어갔으므로 -> 수정 분기로 들어가지 않았다.
    
    return {
        'code': 400,
        'message': 'field에 잘못된 값이 입력되었습니다.'
    }, 400