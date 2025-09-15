#!/usr/bin/env python3
# coding: utf-8
"""
간단한 TCP 채팅 클라이언트
- 서버에 접속 후 닉네임 입력
- 표준 입력으로 메시지 입력
- '/종료'로 연결 종료
- '/귓속말 닉네임 메시지' 형식으로 귓속말 사용 가능
"""

import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
ENCODING = 'utf-8'
ADDR = (SERVER_HOST, SERVER_PORT)


def receive_loop(sock):
    """서버로부터 오는 메시지를 계속 출력."""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print('서버와의 연결이 종료되었습니다.')
                break
            sys.stdout.write(data.decode(ENCODING))
            sys.stdout.flush()
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except Exception:
            pass
        # 프로그램 종료
        sys.exit(0)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(ADDR)
    except Exception as exc:
        print('서버에 연결할 수 없습니다:', exc)
        return

    # 서버에서 오는 메시지 수신 스레드 시작
    thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    thread.start()

    try:
        # 표준 입력으로부터 보내기
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            # 줄바꿈 포함 전달
            sock.sendall(line.encode(ENCODING))
            if line.strip() == '/종료':
                break
    except KeyboardInterrupt:
        try:
            sock.sendall('/종료\n'.encode(ENCODING))
        except Exception:
            pass
    finally:
        try:
            sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
