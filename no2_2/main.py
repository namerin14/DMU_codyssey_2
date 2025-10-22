# send_bulk_html_mail.py

import smtplib
import csv
import os
from email.message import EmailMessage


def read_mail_targets(csv_filename):
    """CSV 파일에서 메일 대상자 정보를 읽어 리스트로 반환한다"""
    recipients = []
    try:
        with open(csv_filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    email = row[1].strip()
                    recipients.append((name, email))
    except FileNotFoundError:
        print('CSV 파일을 찾을 수 없습니다.')
    return recipients


def create_html_message(sender, recipient, subject, html_body, attachment_path=None):
    """HTML 이메일 메시지를 생성하고 반환한다"""
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content('이메일을 HTML 형식으로 보려면 HTML 지원 메일 클라이언트를 사용하세요.')
    msg.add_alternative(html_body, subtype='html')

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                filename = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype='application',
                                   subtype='octet-stream', filename=filename)
        except FileNotFoundError:
            print('첨부 파일을 찾을 수 없습니다. 첨부 없이 발송합니다.')

    return msg


def send_bulk_email():
    """메일을 여러 명에게 HTML 형식으로 전송하는 함수"""
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender_email = input('보내는 Gmail 주소를 입력하세요: ')
    sender_password = input('비밀번호 또는 앱 비밀번호를 입력하세요: ')
    subject = inp
