"""
서비스 계층 (Service Layer)
- 라우트에서 직접 DB 조작하지 않고
- 이 모듈을 거쳐서 DB CRUD 실행
"""

from app import SessionLocal
from app.models import Review


def get_all_reviews():
    """모든 리뷰 조회"""
    session = SessionLocal()
    try:
        # 모든 리뷰 데이터를 리스트 형태로 반환
        return session.query(Review).all()
    finally:
        session.close()


def create_review(title, content, rating):
    """리뷰 생성"""
    session = SessionLocal()
    try:
        # 새로운 Review 객체 생성 및 DB 추가
        new_review = Review(title=title, content=content, rating=rating)
        session.add(new_review)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_review_by_id(review_id):
    """ID로 리뷰 조회"""
    session = SessionLocal()
    try:
        # 특정 ID를 가진 리뷰 1건 조회
        return session.query(Review).filter(Review.id == review_id).first()
    finally:
        session.close()


def update_review(review_id, title, content, rating):
    """리뷰 수정"""
    session = SessionLocal()
    try:
        # 수정할 리뷰 조회
        review = session.query(Review).filter(Review.id == review_id).first()
        if review:
            review.title = title
            review.content = content
            review.rating = rating
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_review(review_id):
    """리뷰 삭제"""
    session = SessionLocal()
    try:
        # 삭제할 리뷰 조회
        review = session.query(Review).filter(Review.id == review_id).first()
        if review:
            session.delete(review)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()