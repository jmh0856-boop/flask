from sqlalchemy import Column, Integer, String, Text
from . import Base

# Review 모델 클래스 정의
class Review(Base):
    __tablename__ = 'reviews'  # 데이터베이스 내 테이블 이름 설정

    # id: 기본 키 (Primary Key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # title: 책/영화 이름 (최대 100자, 비어있을 수 없음)
    title = Column(String(100), nullable=False)
    
    # content: 리뷰 내용 (긴 텍스트, 비어있을 수 없음)
    content = Column(Text, nullable=False)
    
    # rating: 별점 (1~5 정수, 비어있을 수 없음)
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Review {self.title} - ⭐{self.rating}>'