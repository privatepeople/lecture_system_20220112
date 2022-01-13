# 플라스크 자체를 로딩.

from flask import Flask, request

from server.db_connector import DBConnector

from .api.user import login, sign_up, find_user_by_email
from .api.lecture import lecture_test

# DB 연결 정보를 관리하는 클래스 생성 => 객체를 변수에 담아두자.
# db = DBConnector()

def create_app():
    app = Flask(__name__)
    
    # 기본 로그인
    @app.post("/user")
    def user_post():
        # args : 쿼리파라미터들이 들어있는 데이터들 ( GET / DELETE )
        # form : 폼데이터에 담겨있는 데이터들 ( POST / PUT / PATCH )
        return login(request.form.to_dict())
    
    # 회원가입
    @app.put("/user")
    def user_put():
        return sign_up(request.form.to_dict())
    
    # 사용자 조회
    @app.get("/user")
    def user_get():
        return find_user_by_email(request.args.to_dict())
    
    @app.post("/lecture")
    def lecture_post():
        return lecture_test()
    
    return app