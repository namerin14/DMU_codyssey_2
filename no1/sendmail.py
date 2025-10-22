# sendmail.py

import smtplib
from email.message import EmailMessage
import os


def send_email():
    """Gmail을 통해 이메일을 보내는 함수"""
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # 기본 SMTP 포트

    sender_email = input('보내는 사람(Gmail) 주소를 입력하세요: ')
    sender_password = input('비밀번호 또는 앱 비밀번호를 입력하세요: ')
    recipient_email = input('받는 사람 이메일 주소를 입력하세요: ')
    subject = input('메일 제목을 입력하세요: ')
    body = input('메일 본문을 입력하세요: ')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    try:
        attach = input('첨부할 파일 경로를 입력하세요 (없으면 Enter): ')
        if attach:
            with open(attach, 'rb') as file:
                filename = os.path.basename(attach)
                file_data = file.read()
                msg.add_attachment(file_data, maintype='application',
                                   subtype='octet-stream', filename=filename)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print('메일이 성공적으로 전송되었습니다.')

    except FileNotFoundError:
        print('첨부 파일을 찾을 수 없습니다.')
    except smtplib.SMTPAuthenticationError:
        print('로그인 인증에 실패했습니다. 이메일 주소나 비밀번호를 확인하세요.')
    except smtplib.SMTPException as e:
        print('SMTP 오류가 발생했습니다:', str(e))
    except Exception as e:
        print('예상치 못한 오류가 발생했습니다:', str(e))


if __name__ == '__main__':
    send_email()
