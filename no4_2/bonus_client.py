# client.py

import http.client
import json
from typing import Dict, Any

# === 설정 ===
HOST = '127.0.0.1'
PORT = 8000
HEADERS = {'Content-Type': 'application/json'}


def print_response(response: http.client.HTTPResponse, title: str):
    """
    HTTP 응답을 읽고 JSON 형식으로 출력합니다.
    """
    print(f"\n--- {title} ---")
    data = response.read().decode('utf-8')
    try:
        print(json.dumps(json.loads(data), indent = 4, ensure_ascii = False))
    except json.JSONDecodeError:
        print(f"오류 발생: 응답 본문이 JSON 형식이 아닙니다.\n{data}")
    print(f"Status: {response.status} {response.reason}")
    print("-" * (len(title) + 8))


def make_request(method: str, path: str, body: Optional[Dict[str, Any]] = None) -> http.client.HTTPResponse:
    """
    FastAPI 서버로 요청을 보내고 응답 객체를 반환합니다.
    """
    conn = http.client.HTTPConnection(HOST, PORT)
    
    encoded_body = json.dumps(body, ensure_ascii = False).encode('utf-8') if body else None
    
    conn.request(method, path, body = encoded_body, headers = HEADERS)
    response = conn.getresponse()
    conn.close()
    return response


def run_client_app():
    """
    구현된 CRUD 기능을 순서대로 호출하여 동작을 확인합니다.
    """
    print("FastAPI Todo List 클라이언트 앱 시작")
    
    # 1. POST: 항목 2개 추가
    add_item_1 = {"id": 10, "task": "클라이언트 앱 개발", "is_completed": False}
    response_1 = make_request('POST', '/add_todo', add_item_1)
    print_response(response_1, '1. 항목 10 추가 (POST)')
    
    add_item_2 = {"id": 11, "task": "클라이언트 테스트", "is_completed": False}
    response_2 = make_request('POST', '/add_todo', add_item_2)
    print_response(response_2, '2. 항목 11 추가 (POST)')
    
    # 2. GET: 개별 조회
    response_3 = make_request('GET', '/retrieve_todo/10')
    print_response(response_3, '3. ID 10 개별 조회 (GET)')
    
    # 3. PUT: 항목 수정
    update_data = {"is_completed": True, "task": "클라이언트 앱 개발 완료"}
    response_4 = make_request('PUT', '/update_todo/10', update_data)
    print_response(response_4, '4. ID 10 수정 (PUT)')
    
    # 4. GET: 전체 조회 (수정 확인)
    response_5 = make_request('GET', '/retrieve_todo')
    print_response(response_5, '5. 전체 항목 조회 (GET)')
    
    # 5. DELETE: 항목 삭제
    response_6 = make_request('DELETE', '/delete_single_todo/11')
    print_response(response_6, '6. ID 11 삭제 (DELETE)')
    
    # 6. GET: 전체 조회 (삭제 확인)
    response_7 = make_request('GET', '/retrieve_todo')
    print_response(response_7, '7. 최종 전체 항목 조회 (GET)')


if __name__ == '__main__':
    run_client_app()
