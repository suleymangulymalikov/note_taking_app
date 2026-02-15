from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

notes_db = []

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[list[str]] = None


class Note(NoteCreate):
    id: int
    created_at: datetime
    updated_at: datetime


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    new_id = 1 if not notes_db else max(note.id for note in notes_db) + 1
    created_at = datetime.now()
    updated_at = datetime.now()

    new_note = Note(
        title = note.title,
        content = note.content,
        tags = note.tags,
        id = new_id,
        created_at = created_at,
        updated_at = updated_at        
    )
    
    notes_db.append(new_note)

    return new_note