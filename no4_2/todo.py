# todo.py

import csv
import os
from typing import Dict, List, Optional

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

# model.py에서 정의한 모델들을 import
from model import TodoItem, UpdateTodoItem # <-- model.py 파일에서 import


# === 설정 ===
CSV_FILE_NAME = 'todo_data.csv'

# === 데이터 관리 함수 (CSV 파일 관련) ===
# 이전 과제에서 작성한 함수와 동일
def load_todo_list() -> List[Dict]:
    """
    CSV 파일에서 할 일 목록을 불러와 리스트[Dict] 형태로 반환합니다.
    """
    # 함수 이름은 소문자, 언더라인(_) 사용
    todo_list = []
    if not os.path.exists(CSV_FILE_NAME):
        return todo_list

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
        if os.path.exists(CSV_FILE_NAME):
            os.remove(CSV_FILE_NAME)
        return

    # 첫 번째 항목의 키를 헤더로 사용
    fieldnames = list(todo_list[0].keys())

    with open(CSV_FILE_NAME, mode = 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader()
        writer.writerows(todo_list)


# === 라우터 정의 ===

router = APIRouter()
todo_list = load_todo_list()


# 이전 과제 함수: 항목 추가
@router.post('/add_todo')
def add_todo(item: TodoItem) -> Dict:
    # item_dict = item.model_dump()
    # (FastAPI 0.100.0 이상에서는 model_dump() 사용)
    item_dict = item.dict()
    if not item_dict or not any(item_dict.values()):
        raise HTTPException(status_code = 400, detail = "입력된 할 일 항목이 비어있습니다.")

    todo_list.append(item_dict)
    save_todo_list(todo_list)

    return {'message': '할 일 항목이 성공적으로 추가되었습니다.', 'new_item': item_dict}


# 이전 과제 함수: 전체 조회
@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    return {'todo_list': todo_list, 'count': len(todo_list)}


# --- 📌 개별 조회 기능 추가 ---
@router.get('/retrieve_todo/{todo_id}')
def get_single_todo(todo_id: int) -> Dict:
    """
    경로 매개변수(todo_id)를 이용해 개별 항목을 조회합니다. (GET 방식)
    """
    for item in todo_list:
        if item['id'] == todo_id:
            # 입출력은 Dict 타입으로 한다.
            return {'message': f'ID {todo_id} 항목을 성공적으로 조회했습니다.', 'item': item}

    # 항목을 찾지 못한 경우
    raise HTTPException(status_code = 404, detail = f"ID {todo_id}인 할 일 항목을 찾을 수 없습니다.")


# --- 📌 수정 기능 추가 ---
@router.put('/update_todo/{todo_id}')
def update_todo(todo_id: int, updated_item: UpdateTodoItem) -> Dict:
    """
    경로 매개변수(todo_id)를 이용해 할 일 항목을 수정합니다. (PUT 방식)
    """
    item_found = False
    
    # updated_data = updated_item.model_dump(exclude_unset = True) 
    updated_data = updated_item.dict(exclude_unset = True) # 필수가 아닌 필드만 업데이트
    
    if not updated_data:
        raise HTTPException(status_code = 400, detail = '수정할 내용이 제공되지 않았습니다.')

    for item in todo_list:
        if item['id'] == todo_id:
            item_found = True
            
            # 업데이트할 필드만 수정
            for key, value in updated_data.items():
                # 'is_completed'는 bool 타입으로 명시적으로 변환 (Pydantic이 이미 처리)
                item[key] = value

            save_todo_list(todo_list)
            
            # 입출력은 Dict 타입으로 한다.
            return {'message': f'ID {todo_id} 항목이 성공적으로 수정되었습니다.', 'updated_item': item}

    # 항목을 찾지 못한 경우
    if not item_found:
        raise HTTPException(status_code = 404, detail = f"ID {todo_id}인 할 일 항목을 찾을 수 없습니다.")


# --- 📌 삭제 기능 추가 ---
@router.delete('/delete_single_todo/{todo_id}')
def delete_single_todo(todo_id: int) -> Dict:
    """
    경로 매개변수(todo_id)를 이용해 개별 항목을 삭제합니다. (DELETE 방식)
    """
    global todo_list
    
    # 삭제할 항목을 찾아서 인덱스를 저장
    initial_len = len(todo_list)
    todo_list = [item for item in todo_list if item['id'] != todo_id]
    
    if len(todo_list) < initial_len:
        save_todo_list(todo_list)
        # 입출력은 Dict 타입으로 한다.
        return {'message': f'ID {todo_id} 항목이 성공적으로 삭제되었습니다.', 'deleted_id': todo_id}
    else:
        # 항목을 찾지 못한 경우
        raise HTTPException(status_code = 404, detail = f"ID {todo_id}인 할 일 항목을 찾을 수 없습니다.")


# === FastAPI 애플리케이션 생성 및 라우터 포함 ===

app = FastAPI()
app.include_router(router)
