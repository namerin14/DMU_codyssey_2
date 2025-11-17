# models.py

from sqlalchemy import Column, Integer, String, DateTime, text
from database import Base
from datetime import datetime

# 클래스의 이름은 CapWord 방식 준수
class Question(Base):
    """
    질문 데이터 모델 (게시판 글)
    """
    # 질문 데이터의 고유번호 (primary key)
    id = Column(Integer, primary_key = True)
    
    # 질문 제목
    subject = Column(String, nullable = False)
    
    # 질문 내용
    content = Column(String, nullable = False)
    
    # 질문 작성일시
    create_date = Column(DateTime, nullable = False, default = datetime.now)
