import os

# 프로젝트 루트 경로 (app 폴더의 상위 폴더)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# instance 폴더 경로 설정 (프로젝트 루트/instance)
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# 폴더가 없으면 생성
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    """환경 설정 (로컬 SQLite 기본값)"""
    
    # DB 파일의 절대 경로 지정 (instance/reviews.db)
    DB_PATH = os.path.join(INSTANCE_DIR, "reviews.db")
    
    # SQLAlchemy 데이터베이스 URI 설정
    # os.getenv를 통해 환경 변수가 있으면 사용하고, 없으면 로컬 SQLite를 사용합니다.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    
    # 객체 변경 추적 기능 비활성화 (메모리 절약 및 성능 향상)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 디버깅 모드 설정 (개발 환경용)
    DEBUG = True