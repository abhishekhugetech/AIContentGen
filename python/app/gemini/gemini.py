# Import all utils
import asyncio
import base64
import contextlib
import datetime
import os
import json
import wave
import itertools
import uuid
# Import all gemini utils
from google import genai
from google.genai import types


# Set the model
MODEL = "gemini-2.0-flash-exp"

# Make async enumerate
async def async_enumerate(it):
  n = 0
  async for item in it:
    yield n, item
    n +=1

# Generate text content
def generate_text_content(content: str):
    # Initialize the client
    client = genai.Client(http_options= {'api_version': 'v1alpha'}, api_key=os.getenv("GEMINI_API_KEY"))
    # Generate the content
    response = client.models.generate_content(
        model=MODEL, contents=content
    )
    # Extract the text from the response
    return response.text

# Make wave file
@contextlib.contextmanager
def wave_file(filename, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        yield wf

# Generate audio content
async def generate_audio_content(message: str):
    # Initialize the client
    client = genai.Client(http_options= {'api_version': 'v1alpha'}, api_key=os.getenv("GEMINI_API_KEY"))

    config={"generation_config": {"response_modalities": ["AUDIO"]}, "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Aoede"}}}}

    async with client.aio.live.connect(model=MODEL, config=config) as session:
        file_name = 'audio_{}.wav'.format(uuid.uuid4())
        with wave_file(file_name) as wav:
            print("> ", message, "\n")
            await session.send(input=message, end_of_turn=True)

            turn = session.receive()
            async for n,response in async_enumerate(turn):
                if response.data is not None:
                    wav.writeframes(response.data)
                    if n==0:
                        print(response.server_content.model_turn.parts[0].inline_data.mime_type)
                        print('.', end='')

    print("Audio content generated")
    return file_name