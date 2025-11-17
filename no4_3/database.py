# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 이름 (프로젝트 루트에 저장)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./myboard.db'

# connect_args는 SQLite를 사용할 때만 필요하며,
# 기본적으로 하나의 스레드만 데이터베이스와 통신하도록 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False}
)

# SessionLocal 클래스 정의: 데이터베이스 세션을 생성하는 클래스
# autocommit은 False 로 설정 (제약조건 준수)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Base 클래스 정의: 모델들이 상속받아 사용
# ORM 클래스가 테이블과 매핑될 때 사용
Base = declarative_base()

# 데이터베이스 세션 의존성 주입 함수 (FastAPI에서 사용)
def get_db():
    """
    데이터베이스 세션을 생성하고 요청 처리가 완료된 후 닫는 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
