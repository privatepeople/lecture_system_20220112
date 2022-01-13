# 플라스크 자체를 로딩.

from flask import Flask, request

from server.db_connector import DBConnector

# DB 연결 정보를 관리하는 클래스 생성 => 객체를 변수에 담아두자.
db = DBConnector()

def create_app():
    app = Flask(__name__)
    
    # API 로직 함수/클래스 들은, create_app 함수에서만 필요함.
    # 함수 내부에서 import 실행
    from .api.user import login, sign_up, find_user_by_email
    from .api.lecture import get_all_lectures
    
    # 기본 로그인
    @app.post("/user")
    def user_post():
        # args : 쿼리파라미터들이 들어있는 데이터들 ( GET / DELETE )
        # form : 폼데이터에 담겨있는 데이터들 ( POST / PUT / PATCH )
        # cf) json body 첨부하는 경우도 있음
        return login(request.form.to_dict())
    
    # 회원가입
    @app.put("/user")
    def user_put():
        return sign_up(request.form.to_dict())
    
    # 사용자 조회
    @app.get("/user")
    def user_get():
        return find_user_by_email(request.args.to_dict())
    
    # 모든 강의 목록 조회
    @app.get("/lecture")
    def lecture_get():
        return get_all_lectures(request.args.to_dict())
    
    return app