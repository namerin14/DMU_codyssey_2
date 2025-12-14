from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

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

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question = Question(subject=_question_create.subject,
                        content=_question_create.content,
                        create_date=datetime.now())
    db.add(question)
    db.commit()
