from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema
from models import Question

router = APIRouter(
    prefix='/api/question',
)

@router.get('/list', response_model=List[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).all()
    return _question_list
