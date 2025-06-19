# app/query_routes.py

from fastapi import APIRouter, Depends, HTTPException
from app.embeddings import index_documents
from app.auth import get_current_user
from app.models import User
from pydantic import BaseModel
from app.crew.crew_runner import run_crew_question  # Import the function from your Crew setup

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query_user_docs(payload: QueryRequest, current_user: User = Depends(get_current_user)):
    try:
        user_id = current_user.id

        # Step 1: Index documents first (in case new ones were uploaded)
        index_documents(user_id=user_id)

        # Step 2: Run the Crew AI agent workflow
        answer = run_crew_question(user_id, payload.question)

        # Extract only the final answer (the last 'raw' field in 'tasks_output', if present)
        if isinstance(answer, dict) and 'tasks_output' in answer and isinstance(answer['tasks_output'], list):
            tasks = answer['tasks_output']
            if tasks and isinstance(tasks[-1], dict) and 'raw' in tasks[-1]:
                answer_text = tasks[-1]['raw']
            else:
                answer_text = answer.get('raw', str(answer))
        elif isinstance(answer, dict) and 'raw' in answer:
            answer_text = answer['raw']
        else:
            answer_text = str(answer)

        return {"answer": answer_text, "context": []}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
