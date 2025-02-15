import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def upload_file(f: any, path: str):
    response = supabase.storage.from_("avatars").upload(
        file=f,
        path=path,
        file_options={"cache-control": "3600", "upsert": "false"},
    )
    return response