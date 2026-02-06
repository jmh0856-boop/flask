from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)

########
# DB 설정
########
BASE_DIR = os.path.dirname(__file__)
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(INSTANCE_DIR, "todos.db")}"
engine = create_engine(DATABASE_URL, echo=True)
# "sqlite:///instance/todos.db"

SessionLocal = sessionmaker(bind=engine)


#########
# 모델 정의
#########
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)

    def __repr__(self):
        return f"<Todo id={self.id}, task='{self.task}'>"

Base.metadata.create_all(bind=engine)


#######
# CRUD
#######



# READ: 전체 항목 조회
@app.route("/todos", methods=["GET"])
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return jsonify([{"id": t.id, "task": t.task} for t in todos])


# READ: 특정 항목 조회
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    db = SessionLocal()

    todo = db.query(Todo).get(todo_id)
    db.close()

    if not todo:
        return jsonify({"error": "해당 할 일이 없습니다"}), 404
    return jsonify({"id": todo.id, "task": todo.task})


# CREATE: 새로운 항목 조회
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    db = SessionLocal()
    todo = Todo(task=data["task"])
    db.add(todo)
    db.commit()
    db.refresh(todo) # commit 후 자동 생성된 id 불러오기
    db.close()

    return jsonify({"id": todo.id, "task": todo.task}), 201


# UPDATE: 특정 항목 수정
@app.route("/todos/<int:todo_id>", methods=["put"])
def update_todo(todo_id):
    db = SessionLocal()
    
    todo = db.query(Todo).get(todo_id)
    if  todo:
        db.close()
        return jsonify({"error": "해당 항목이 없습니다"}), 404

    data = request.get_json()
    todo.task = data["task"]
    db.commit()

    updated = {"id": todo.id, "task": todo.task}
    db.close()
    return jsonify(updated)


# DELETE: 특정 항목 삭제
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = SessionLocal()
    
    todo = db.query(Todo).get(todo_id)
    if  todo:
        db.close()
        return jsonify({"error": "해당 항목이 없습니다"}), 404

    db.delete(todo)
    db.commit()
    db.close()
    return jsonify({"deleted": todo_id})


if __name__ == "__main__":
    app.run(debug=True, port = 8000)
