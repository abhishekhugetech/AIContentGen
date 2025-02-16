from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.security import APIKeyHeader

import os
from urllib.parse import quote_plus
from app.gemini.gemini import generate_text_content, generate_audio_content
import asyncio
from app.utils.auth import check_x_api_key
router = APIRouter()
api_key_header = APIKeyHeader(name="x-api-key")


@router.get("/test/")
async def test():
    return {"status": "Tested"}


# Post route to generate content from gemini
@router.post("/generate-text-content")
async def generate_content(request: Request, is_valid: dict = Depends(check_x_api_key)):
    data = await request.json()
    prompt = data.get("prompt")
    system_prompt = data.get("system_prompt")

    content = generate_text_content(prompt, system_prompt)

    return {"message": "Content generated", "content": content}

# Post route to generate content from gemini
@router.post("/generate-audio-content")
async def generate_content(request: Request, is_valid: dict = Depends(check_x_api_key)):
    data = await request.json()
    prompt = data.get("prompt")
    audio = data.get("audio")
    system_prompt = data.get("system_prompt")

    # valid audio names are : Aoede, Charon, Fenrir, Kore, and Puck
    valid_audio_names = ["Aoede", "Charon", "Fenrir", "Kore", "Puck"]
    if audio not in valid_audio_names:
        raise HTTPException(status_code=400, detail="Invalid or missing key 'audio', valid audio names are: {}".format(valid_audio_names))

    file_path = await generate_audio_content(prompt, audio, system_prompt)

    # return "File path: {}".format(file_path)

    # Return file with appropriate headers
    try:
        # get file name from file path
        file_name = file_path.split("/")[-1]
        return Response(
            content=open(file_path, "rb").read(),
            media_type="audio/wav",  # Adjust content type based on your file type
            headers={
                "Content-Disposition": f"attachment; filename={file_name}"
            }
        )
    finally:
        # Clean up the file after sending
        if os.path.exists(file_path):
            os.remove(file_path)