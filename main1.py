# Transtalor
from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from typing import Dict
from googletrans import Translator

app = FastAPI()
translator = Translator()

class TranslationResponse(BaseModel):
    translated_text: str

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(text: str = Form(...), dest_language: str = Form(...)) -> Dict[str, str]:
    try:
        translation = translator.translate(text, dest=dest_language)
        return {"translated_text": translation.text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))