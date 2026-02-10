"""
라우트 (Controller Layer)
- 사용자가 요청한 URL을 처리하고
- 서비스 계층을 호출해서 DB 조작
- 결과를 템플릿에 전달
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.services.review_service import (
    get_all_reviews, 
    create_review, 
    get_review_by_id,
    update_review, 
    delete_review
)

# 블루프린트 생성
review_bp = Blueprint("review", __name__)

@review_bp.route("/")
def index():
    """리뷰 목록 + 평균 별점"""
    # 리뷰 목록 가져오기
    reviews = get_all_reviews()
    
    # 평균 별점 계산 (리뷰가 있으면 평균 계산, 없으면 0.0)
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
    else:
        avg_rating = 0.0
        
    return render_template("index.html", reviews=reviews, avg_rating=avg_rating)


@review_bp.route("/new", methods=["GET", "POST"])
def new_review():
    """새 리뷰 작성"""
    if request.method == "POST":
        # form 데이터 받아오기
        title = request.form.get("title")
        content = request.form.get("content")
        rating = int(request.form.get("rating"))
        
        # 서비스 계층 호출하여 DB 저장
        create_review(title, content, rating)
        return redirect(url_for("review.index"))
        
    # GET 요청일 경우 작성 폼 렌더링
    return render_template("new.html")


@review_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_review(id):
    """리뷰 수정"""
    # 수정할 리뷰 가져오기
    review = get_review_by_id(id)
    
    if request.method == "POST":
        # 수정된 데이터 받기
        title = request.form.get("title")
        content = request.form.get("content")
        rating = int(request.form.get("rating"))
        
        # 서비스 계층 호출하여 업데이트 실행
        update_review(id, title, content, rating)
        return redirect(url_for("review.index"))
        
    # GET 요청일 경우 수정 폼 렌더링 (기존 데이터 전달)
    return render_template("edit.html", review=review)


@review_bp.route("/delete/<int:id>")
def delete_review_route(id):
    """리뷰 삭제"""
    # 서비스 계층 호출하여 리뷰 삭제
    delete_review(id)
    return redirect(url_for("review.index"))