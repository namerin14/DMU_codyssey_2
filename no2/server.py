#!/usr/bin/env python3
# coding: utf-8
"""
멀티스레드 채팅 서버 (TCP)
- 여러 클라이언트 동시 접속 처리
- 접속시 전체 알림: '~~님이 입장하셨습니다.'
- '/종료' 명령으로 연결 종료
- 귓속말: '/귓속말 target message'
"""

import socket
import threading


HOST = '0.0.0.0'
PORT = 5000
ENCODING = 'utf-8'
ADDR = (HOST, PORT)


class ClientInfo:
    """연결된 클라이언트 정보를 담는 간단한 클래스."""
    def __init__(self, conn, addr, nickname):
        self.conn = conn
        self.addr = addr
        self.nickname = nickname


clients_lock = threading.Lock()
clients = {}  # nickname -> ClientInfo


def broadcast(message, exclude_nick=None):
    """모든 클라이언트에게 메시지 전송. exclude_nick이 있으면 해당 사용자 제외."""
    with clients_lock:
        for nick, info in list(clients.items()):
            if nick == exclude_nick:
                continue
            try:
                info.conn.sendall(message.encode(ENCODING))
            except Exception:
                # 전송 실패 시 해당 클라이언트 제거
                remove_client(nick)


def send_private(sender_nick, target_nick, message_body):
    """특정 사용자에게만 메시지를 보냄. 실패하면 발신자에게 에러 메시지 전송."""
    with clients_lock:
        target = clients.get(target_nick)
        sender = clients.get(sender_nick)
        if not target:
            if sender:
                try:
                    sender.conn.sendall(
                        ('서버> 해당 닉네임을 찾을 수 없습니다: {}\n'.format(target_nick)).encode(
                            ENCODING))
                except Exception:
                    remove_client(sender_nick)
            return
        # 귓속말 형식: 발신자(귓속말)> 메시지
        try:
            target.conn.sendall(
                ('{}(귓속말)> {}\n'.format(sender_nick, message_body)).encode(ENCODING))
        except Exception:
            remove_client(target_nick)


def remove_client(nickname):
    """클라이언트 리스트에서 제거하고 소켓 닫기."""
    with clients_lock:
        info = clients.pop(nickname, None)
    if info:
        try:
            info.conn.close()
        except Exception:
            pass
        # 나감 알림을 전체에 전송
        broadcast('{}님이 나가셨습니다.\n'.format(nickname))


def handle_client(conn, addr):
    """클라이언트별 스레드 함수."""
    try:
        conn.sendall('닉네임을 입력하세요: '.encode(ENCODING))
        nick_bytes = conn.recv(1024)
        if not nick_bytes:
            conn.close()
            return
        nickname = nick_bytes.decode(ENCODING).strip()
        if not nickname:
            conn.sendall('서버> 유효한 닉네임이 아닙니다. 연결을 종료합니다.\n'.encode(ENCODING))
            conn.close()
            return

        # 닉네임 중복 처리: 중복이면 숫자 붙여 변형
        with clients_lock:
            base_nick = nickname
            counter = 1
            while nickname in clients:
                nickname = '{}_{}'.format(base_nick, counter)
                counter += 1
            clients[nickname] = ClientInfo(conn, addr, nickname)

        # 입장 알림
        broadcast('{}님이 입장하셨습니다.\n'.format(nickname))
        conn.sendall('서버> 환영합니다, {} 님. /종료 로 나가실 수 있습니다.\n'.format(nickname).encode(ENCODING))

        # 메시지 수신 루프
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode(ENCODING).rstrip('\n')
            if not message:
                continue

            # 종료 명령 처리
            if message == '/종료':
                try:
                    conn.sendall('서버> 연결을 종료합니다.\n'.encode(ENCODING))
                except Exception:
                    pass
                break

            # 귓속말 처리: '/귓속말 target message...'
            if message.startswith('/귓속말 '):
                parts = message.split(' ', 2)
                if len(parts) >= 3:
                    target_nick = parts[1].strip()
                    body = parts[2].strip()
                    if target_nick and body:
                        send_private(nickname, target_nick, body)
                        continue
                # 잘못된 형식
                conn.sendall('서버> 귓속말 사용법: /귓속말 받는사람닉네임 메시지\n'.encode(ENCODING))
                continue

            # 일반 메시지: 전체 브로드캐스트
            full_msg = '{}> {}\n'.format(nickname, message)
            broadcast(full_msg)
    except Exception:
        pass
    finally:
        # 연결 종료 처리
        remove_client(nickname)


def start_server():
    """서버 소켓 생성 및 접속 수락 루프."""
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(ADDR)
    server_sock.listen(5)
    print('서버 시작: {}:{}'.format(HOST, PORT))
    try:
        while True:
            conn, addr = server_sock.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print('\n서버 종료 중...')
    finally:
        # 모든 클라이언트 닫기
        with clients_lock:
            for info in list(clients.values()):
                try:
                    info.conn.close()
                except Exception:
                    pass
            clients.clear()
        server_sock.close()
        print('서버 종료 완료.')


if __name__ == '__main__':
    start_server()
