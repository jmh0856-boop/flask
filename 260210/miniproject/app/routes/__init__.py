from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# DB 객체를 외부에서 사용할 수 있도록 생성
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 1. 설정 로드 (app/config.py의 Config 클래스 사용)
    app.config.from_object('app.config.Config')

    # 2. DB 초기화 (객체와 앱 연결)
    db.init_app(app)

    # 3. 블루프린트 등록 (URL 처리 로직 연결)
    # 반드시 db.init_app 이후에 등록해야 합니다.
    from app.routes.review_routes import review_bp
    app.register_blueprint(review_bp)

    # 4. DB 테이블 생성
    # 애플리케이션 컨텍스트 안에서 모델을 바탕으로 테이블을 만듭니다.
    with app.app_context():
        from app import models  # 모델을 임포트해야 테이블이 생성됩니다.
        db.create_all()

    return app