# model.py

from pydantic import BaseModel
from typing import Optional

# 클래스의 이름은 CapWord 방식으로 정의
class TodoItem(BaseModel):
    """
    할 일 항목의 구조를 정의하는 Pydantic 모델.
    전체 항목을 받음.
    """
    id: int
    task: str
    is_completed: bool = False


class UpdateTodoItem(BaseModel):
    """
    할 일 항목의 수정을 위한 Pydantic 모델.
    일부 필드만 선택적으로 수정할 수 있도록 Optional을 사용.
    """
    # Optional을 사용하면 request body에 해당 필드가 없어도 오류가 발생하지 않음
    task: Optional[str] = None
    is_completed: Optional[bool] = None
