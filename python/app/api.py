from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, Response

import os
from urllib.parse import quote_plus
from app.gemini.gemini import generate_text_content, generate_audio_content
import asyncio

router = APIRouter()

@router.get("/test/")
async def test():
    return {"status": "Tested"}


# Post route to generate content from gemini
@router.post("/generate-text-content")
async def generate_content(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    content = generate_text_content(prompt)

    return {"message": "Content generated", "content": content}

# Post route to generate content from gemini
@router.post("/generate-audio-content")
async def generate_content(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    file_path = await generate_audio_content(prompt)

    # return "File path: {}".format(file_path)

    # Return file with appropriate headers
    try:
        return Response(
            content=open(file_path, "rb").read(),
            media_type="audio/wav",  # Adjust content type based on your file type
            headers={
                "Content-Disposition": f"attachment; filename=audio_{prompt[:30]}.wav"
            }
        )
    finally:
        # Clean up the file after sending
        if os.path.exists(file_path):
            os.remove(file_path)