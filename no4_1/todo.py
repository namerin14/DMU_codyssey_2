# todo.py

import csv
import os
from typing import Dict, List

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

# === 설정 ===
# 데이터 저장을 위한 CSV 파일 이름
CSV_FILE_NAME = 'todo_data.csv'

# FastAPI의 입출력 Dict 타입을 위한 Pydantic 모델 정의
# 클래스 이름은 CapWord 방식 준수
class TodoItem(BaseModel):
    """
    할 일 항목의 구조를 정의하는 Pydantic 모델.
    """
    id: int
    task: str
    is_completed: bool = False


# === 데이터 관리 함수 (CSV 파일 관련) ===

def load_todo_list() -> List[Dict]:
    """
    CSV 파일에서 할 일 목록을 불러와 리스트[Dict] 형태로 반환합니다.
    파일이 없으면 빈 리스트를 반환합니다.
    """
    todo_list = []
    if not os.path.exists(CSV_FILE_NAME):
        return todo_list

    # '을 기본으로 사용
    with open(CSV_FILE_NAME, mode = 'r', newline = '', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # CSV에서 읽은 값은 문자열이므로 타입 변환
            row['id'] = int(row['id'])
            row['is_completed'] = row['is_completed'].lower() == 'true'
            todo_list.append(row)

    return todo_list


def save_todo_list(todo_list: List[Dict]):
    """
    현재 할 일 목록을 CSV 파일에 저장합니다.
    """
    if not todo_list:
        # todo_list가 비어있으면 파일 삭제 (혹은 빈 파일로 저장)
        if os.path.exists(CSV_FILE_NAME):
            os.remove(CSV_FILE_NAME)
        return

    # 첫 번째 항목의 키를 헤더로 사용
    fieldnames = list(todo_list[0].keys())

    # '을 기본으로 사용, 부득이한 경우 " "
    with open(CSV_FILE_NAME, mode = 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(todo_list)


# === 라우터 정의 ===

# APIRouter 클래스 사용
router = APIRouter()

# 리스트 객체를 todo_list라는 이름으로 추가 (초기 데이터는 파일에서 로드)
todo_list = load_todo_list()


@router.post('/add_todo')
def add_todo(item: TodoItem) -> Dict:
    """
    todo_list에 새로운 항목을 추가하고 저장합니다. (POST 방식)
    입력되는 Dict 타입(TodoItem)이 빈값이면 경고(HTTPException)를 돌려줍니다.
    """
    # 보너스 과제: 입력 Dict 타입이 빈 값이면 경고를 돌려준다.
    # Pydantic 모델을 사용하므로, item 객체 자체의 유효성은 보장되지만,
    # Dict로 변환하여 key/value 존재 여부를 확인
    item_dict = item.model_dump()
    if not item_dict or not any(item_dict.values()):
        # " " 사용 (경고 메시지)
        raise HTTPException(status_code = 400, detail = "입력된 할 일 항목이 비어있습니다.")

    # 새로운 항목 추가
    todo_list.append(item_dict)
    save_todo_list(todo_list)

    # 입출력은 Dict 타입으로 한다.
    return {'message': '할 일 항목이 성공적으로 추가되었습니다.', 'new_item': item_dict}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    """
    todo_list를 가져옵니다. (GET 방식)
    """
    # 현재 todo_list를 파일에서 다시 로드하여 최신 상태 확인 (선택 사항)
    # todo_list = load_todo_list() # 메모리 상태를 유지하므로 이 부분은 생략
    
    # 입출력은 Dict 타입으로 한다.
    return {'todo_list': todo_list, 'count': len(todo_list)}


# === FastAPI 애플리케이션 생성 및 라우터 포함 ===

# 클래스의 이름은 CapWord 방식 준수
app = FastAPI()
app.include_router(router)
