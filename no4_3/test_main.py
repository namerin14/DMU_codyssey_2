# main.py (테스트용)

from database import engine, Base, SessionLocal
from models import Question
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError

# Base.metadata.create_all(bind = engine) # Alembic을 사용하므로 이 코드는 사용하지 않습니다.

db_session = SessionLocal()

def check_table_exists(table_name):
    """
    inspect 객체를 사용해서 테이블이 존재하는지 확인합니다.
    """
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        return f"SUCCESS: '{table_name}' 테이블이 데이터베이스에 존재합니다."
    else:
        return f"ERROR: '{table_name}' 테이블을 찾을 수 없습니다."

if __name__ == '__main__':
    print(check_table_exists('question'))
    db_session.close()
