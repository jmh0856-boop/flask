from flask_smorest import Blueprint, abort
from schemas import BookSchema
from flask.views import MethodView

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 데이터 저장소
books = [
    {"id": 1, "title": "제목1","author": "저자1"},
    {"id": 2, "title": "제목2","author": "저자2"},
    {"id": 3, "title": "제목3","author": "저자3"},
    {"id": 4, "title": "제목4","author": "저자4"}
]

# 엔드포인트 구현...
@book_blp.route("/")
class BookList(MethodView):
    # GET: 전체 책 목록 조회
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books
    
    # POST: 새로운 책 추가
    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        # ID 생성
        new_data["id"] = max((book["id"] for book in books), default=0) + 1
        books.append(new_data)
        return new_data
    
@book_blp.route('/<int:book_id>')
class Book(MethodView):
    # GET: 특정 책 조회
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="해당 책을 찾을 수 없습니다.")
        return book

    # PUT: 특정 책 수정
    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="해당 책을 찾을 수 없습니다.")
        book.update(new_data)
        return book

    # DELETE: 특정 책 삭제
    @book_blp.response(204)
    def delete(self, book_id):
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="해당 책을 찾을 수 없습니다.")
        books = [book for book in books if book['id'] != book_id]
        return ""
