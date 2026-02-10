from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from .config import Config

# DB 연결 엔진 생성
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# 세션(SessionLocal) 객체 생성 (Thread-safe한 scoped_session 사용)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base 클래스 생성 (모델들이 상속받을 기본 클래스)
Base = declarative_base()
Base.query = SessionLocal.query_property()

def create_app():
    """Flask 앱 생성 및 초기화"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # 모델 import (DB 테이블 생성을 위해 필요)
    from . import models

    # DB 테이블 생성
    Base.metadata.create_all(bind=engine)

    # 라우트 블루프린트 등록
    from .routes.review_routes import review_bp
    app.register_blueprint(review_bp)

    # 요청이 끝날 때마다 세션 닫기 (메모리 누수 방지)
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()

    return app