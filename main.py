from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
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


@app.get("/notes", response_model=List[Note])
def get_all_notes():
    return notes_db

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


@app.get("/notes{note_id}", response_model=Note, responses={ 404: { "detail": "Note not found" } })
def get_note_by_id(note_id: int):
    for note in notes_db:
        if note.id == note_id:
            return note 
    raise HTTPException(status_code=404, detail="Note not found")