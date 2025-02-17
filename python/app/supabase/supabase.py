import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

bucket_name: str = os.environ.get("BUCKET_NAME")

async def upload_file_supabase(f: any, path: str):
    contents = f.read()
    response = supabase.storage.from_(bucket_name).upload(
        file=contents,
        path=path,
        file_options={"cache-control": "3600", "upsert": "true"},
    )
    return response