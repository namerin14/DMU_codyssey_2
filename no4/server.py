#!/usr/bin/env python3
# coding: utf-8
"""
HTTP 서버 과제
- http.server 모듈 활용
- 8080 포트에서 index.html 제공
- 접속 시간, 클라이언트 IP 출력
- 200 OK 헤더 전달
- 보너스: IP 기반 위치 확인 (설명 주석 포함)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


HOST = '0.0.0.0'
PORT = 8080
ENCODING = 'utf-8'
INDEX_FILE = 'index.html'


class MyRequestHandler(BaseHTTPRequestHandler):
    """HTTP 요청을 처리하는 핸들러 클래스."""

    def do_GET(self):
        """GET 요청을 처리한다."""
        # 접속 시간과 클라이언트 IP 출력
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        print('접속 시간: {}, 접속 클라이언트 IP: {}'.format(now, client_ip))

        # index.html 파일 읽기
        try:
            with open(INDEX_FILE, 'r', encoding=ENCODING) as f:
                content = f.read()
            content_bytes = content.encode(ENCODING)

            # 성공 응답 (200 OK)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset={}'.format(ENCODING))
            self.send_header('Content-Length', str(len(content_bytes)))
            self.end_headers()
            self.wfile.write(content_bytes)

        except FileNotFoundError:
            # index.html 없을 경우 404 반환
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset={}'.format(ENCODING))
            self.end_headers()
            self.wfile.write('404 Not Found: index.html 파일이 없습니다.'.encode(ENCODING))

        # --- 보너스 과제 (위치 확인) ---
        # 여기서는 외부 API를 호출해야 하므로 실제 구현 불가.
        # 실제라면 'ip-api.com' 같은 무료 API를 활용:
        # 예: requests.get('http://ip-api.com/json/' + client_ip).json()
        # 단, 본 과제에서는 외부 라이브러리 사용 금지 → 주석으로 가이드만 제공.


def run_server():
    """HTTP 서버 실행."""
    httpd = HTTPServer((HOST, PORT), MyRequestHandler)
    print('HTTP 서버 시작: {}:{}'.format(HOST, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버 종료 중...')
    finally:
        httpd.server_close()
        print('서버 종료 완료.')


if __name__ == '__main__':
    run_server()
